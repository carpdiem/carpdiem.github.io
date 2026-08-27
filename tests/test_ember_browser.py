from __future__ import annotations

import functools
import http.server
import json
import os
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import unittest
import urllib.parse
import urllib.request
from pathlib import Path

import websocket  # pyright: ignore[reportMissingImports]

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PHOTO_PAGE = (
    "/blog/2020-08-10-How-do-you-solve-a-puzzle-with-only-white-pieces-left.html"
)
CODE_PAGE = "/blog/2024-04-22-Python-decorators-for-fun-and-profit.html"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        del format, args


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request: object, client_address: object) -> None:
        pass


def find_chrome() -> Path | None:
    configured = os.environ.get("CHROME_BIN")
    candidates = [
        Path(configured) if configured else None,
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    playwright = sorted(
        Path.home().glob(
            "Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"
        ),
        reverse=True,
    )
    candidates.extend(playwright)
    for command in ("google-chrome", "chromium", "chromium-browser"):
        resolved = shutil.which(command)
        if resolved:
            candidates.append(Path(resolved))
    return next((path for path in candidates if path and path.is_file()), None)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class CDP:
    def __init__(self, websocket_url: str) -> None:
        self.socket = websocket.create_connection(websocket_url, timeout=15)
        self.next_id = 1
        self.events: list[dict] = []

    def call(self, method: str, params: dict | None = None) -> dict:
        call_id = self.next_id
        self.next_id += 1
        self.socket.send(
            json.dumps({"id": call_id, "method": method, "params": params or {}})
        )
        while True:
            message = json.loads(self.socket.recv())
            if message.get("id") == call_id:
                if "error" in message:
                    raise AssertionError(f"CDP {method} failed: {message['error']}")
                return message.get("result", {})
            self.events.append(message)

    def wait_event(self, method: str, timeout: float = 15) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            for index, event in enumerate(self.events):
                if event.get("method") == method:
                    return self.events.pop(index).get("params", {})
            self.socket.settimeout(max(0.05, deadline - time.monotonic()))
            message = json.loads(self.socket.recv())
            if message.get("method") == method:
                return message.get("params", {})
            self.events.append(message)
        raise TimeoutError(method)

    def evaluate(self, expression: str, *, await_promise: bool = False):
        result = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )["result"]
        if "exceptionDetails" in result:
            raise AssertionError(result["exceptionDetails"])
        return result.get("value")

    def navigate(self, url: str, *, settle: bool = True) -> None:
        self.events.clear()
        self.call("Page.navigate", {"url": url})
        self.wait_event("Page.loadEventFired")
        if settle:
            self.evaluate(
                "document.fonts.ready.then(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))))",
                await_promise=True,
            )

    def close(self) -> None:
        self.socket.close()


class EmberBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        chrome = find_chrome()
        if chrome is None:
            raise unittest.SkipTest("set CHROME_BIN to run browser behavior tests")
        if not SITE.is_dir():
            raise unittest.SkipTest(
                "run the Jekyll build before browser behavior tests"
            )

        handler = functools.partial(QuietHandler, directory=str(SITE))
        cls.httpd = QuietServer(("127.0.0.1", 0), handler)
        cls.server_thread = threading.Thread(
            target=cls.httpd.serve_forever, daemon=True
        )
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.httpd.server_port}"

        cls.debug_port = free_port()
        cls.profile = tempfile.TemporaryDirectory(prefix="ember-browser-")
        cls.chrome = subprocess.Popen(
            [
                str(chrome),
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                "--hide-scrollbars",
                "--remote-allow-origins=*",
                f"--remote-debugging-port={cls.debug_port}",
                f"--user-data-dir={cls.profile.name}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        version_url = f"http://127.0.0.1:{cls.debug_port}/json/version"
        deadline = time.monotonic() + 15
        while True:
            try:
                with urllib.request.urlopen(version_url, timeout=1) as response:
                    json.load(response)
                break
            except Exception:
                if time.monotonic() >= deadline:
                    cls.chrome.terminate()
                    raise
                time.sleep(0.05)

        target_url = f"http://127.0.0.1:{cls.debug_port}/json/new?{urllib.parse.quote('about:blank')}"
        request = urllib.request.Request(target_url, method="PUT")
        with urllib.request.urlopen(request, timeout=5) as response:
            target = json.load(response)
        cls.cdp = CDP(target["webSocketDebuggerUrl"])
        cls.cdp.call("Page.enable")
        cls.cdp.call("Runtime.enable")
        cls.cdp.call("Network.enable")

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "cdp"):
            cls.cdp.close()
        if hasattr(cls, "chrome"):
            cls.chrome.terminate()
            cls.chrome.wait(timeout=10)
        if hasattr(cls, "profile"):
            cls.profile.cleanup()
        if hasattr(cls, "httpd"):
            cls.httpd.shutdown()
            cls.httpd.server_close()

    def test_runtime_palette_images_sticky_and_responsive_contracts(self) -> None:
        self.cdp.call(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": 'localStorage.setItem("usuallypragmatic.ember-temperature", "1200k");',
            },
        )
        self.cdp.call(
            "Emulation.setEmulatedMedia",
            {"features": [{"name": "prefers-color-scheme", "value": "light"}]},
        )
        self.cdp.call(
            "Emulation.setDeviceMetricsOverride",
            {"width": 1280, "height": 720, "deviceScaleFactor": 1, "mobile": False},
        )
        self.cdp.navigate(self.base_url + PHOTO_PAGE)

        state = json.loads(
            self.cdp.evaluate(
                "JSON.stringify({palette:document.documentElement.dataset.emberPalette,temperature:document.documentElement.dataset.emberTemperature,paragraphLineHeight:getComputedStyle(document.querySelector('main p')).lineHeight,images:[...document.querySelectorAll('main .ember-js-content img')].map(img=>({src:img.getAttribute('src'),original:img.dataset.emberOriginalSrc,state:img.dataset.emberImageState,loaded:img.complete&&img.naturalWidth>0,width:img.getBoundingClientRect().width,height:img.getBoundingClientRect().height})),buttons:[...document.querySelectorAll('.ember-palette-switcher button')].map(button=>{const rect=button.getBoundingClientRect();return {width:rect.width,height:rect.height}})})"
            )
        )
        self.assertEqual(state["palette"], "1200k-dark")
        self.assertEqual(state["temperature"], "1200k")
        initial_roles = json.loads(
            self.cdp.evaluate(
                "JSON.stringify((()=>{const root=getComputedStyle(document.documentElement);return {link:root.getPropertyValue('--site-link').trim(),visited:root.getPropertyValue('--site-link-visited').trim(),hover:root.getPropertyValue('--site-link-hover').trim(),elevated:root.getPropertyValue('--site-link-elevated').trim(),elevatedVisited:root.getPropertyValue('--site-link-elevated-visited').trim(),elevatedHover:root.getPropertyValue('--site-link-elevated-hover').trim(),header:getComputedStyle(document.querySelector('.site-header')).backgroundColor,body:getComputedStyle(document.body).backgroundColor}})())"
            )
        )
        self.assertEqual(
            initial_roles,
            {
                "link": "#F68F96",
                "visited": "#B76270",
                "hover": "#FFFBEE",
                "elevated": "#F68F96",
                "elevatedVisited": "#F3AC74",
                "elevatedHover": "#FFFBEE",
                "header": "rgb(23, 19, 19)",
                "body": "rgb(5, 4, 4)",
            },
        )
        self.assertTrue(state["images"])
        self.assertTrue(
            all(
                image["state"] == "1200k" and image["loaded"]
                for image in state["images"]
            )
        )
        self.assertTrue(
            all("/images/ember-1200k/" in image["src"] for image in state["images"])
        )
        self.assertTrue(
            all(
                button["width"] >= 44 and 10 <= button["height"] <= 20
                for button in state["buttons"]
            )
        )
        header_geometry = json.loads(
            self.cdp.evaluate(
                "JSON.stringify((()=>{const header=document.querySelector('.site-header'),headerRect=header.getBoundingClientRect(),about=[...document.querySelectorAll('.page-link')].find(link=>link.textContent.trim()==='About'),active=document.querySelector('.ember-palette-switcher button[aria-pressed=\"true\"]'),separator=document.querySelector('.ember-palette-separator'),range=element=>{const value=document.createRange();value.selectNodeContents(element);return value.getBoundingClientRect()},aboutRect=range(about),controlRect=range(active),separatorRect=separator.getBoundingClientRect();return {headerBg:getComputedStyle(header).backgroundColor,bodyBg:getComputedStyle(document.body).backgroundColor,borderTop:getComputedStyle(header).borderTopWidth,top:aboutRect.top-headerRect.top,between:controlRect.top-aboutRect.bottom,bottom:headerRect.bottom-controlRect.bottom,separatorHeight:separatorRect.height,controlHeight:controlRect.height,separatorCenterDelta:Math.abs((separatorRect.top+separatorRect.bottom-controlRect.top-controlRect.bottom)/2)}})())"
            )
        )
        self.assertNotEqual(header_geometry["headerBg"], header_geometry["bodyBg"])
        self.assertEqual(header_geometry["borderTop"], "0px")
        self.assertLessEqual(
            abs(header_geometry["between"] - header_geometry["top"] / 2), 2.0
        )
        self.assertGreaterEqual(header_geometry["bottom"], header_geometry["between"])
        self.assertLessEqual(
            header_geometry["bottom"] - header_geometry["between"], 3.0
        )
        self.assertGreaterEqual(
            header_geometry["separatorHeight"], header_geometry["controlHeight"] * 0.75
        )
        self.assertLessEqual(
            header_geometry["separatorHeight"], header_geometry["controlHeight"]
        )
        self.assertLessEqual(header_geometry["separatorCenterDelta"], 1.0)

        requests = [
            event["params"]["request"]["url"]
            for event in self.cdp.events
            if event.get("method") == "Network.requestWillBeSent"
        ]
        derivative_requests = [url for url in requests if "/images/ember-1200k/" in url]
        original_requests = [
            url
            for url in requests
            if any(image["original"] in url for image in state["images"])
        ]
        self.assertEqual(len(derivative_requests), len(state["images"]))
        self.assertEqual(original_requests, [])

        self.cdp.evaluate("window.scrollTo(0,700)")
        sticky = json.loads(
            self.cdp.evaluate(
                "JSON.stringify({top:document.querySelector('.site-header').getBoundingClientRect().top,overflow:document.documentElement.scrollWidth>innerWidth})"
            )
        )
        self.assertEqual(sticky, {"top": 0, "overflow": False})

        self.cdp.evaluate(
            "document.querySelector('[data-ember-temperature-choice=\"3400k\"]').click()"
        )
        self.cdp.evaluate(
            "Promise.all([...document.querySelectorAll('main .ember-js-content img')].map(img=>img.complete&&img.naturalWidth>0?Promise.resolve():new Promise(resolve=>{img.addEventListener('load',resolve,{once:true});img.addEventListener('error',resolve,{once:true})})))",
            await_promise=True,
        )
        restored = json.loads(
            self.cdp.evaluate(
                "JSON.stringify((()=>{const root=getComputedStyle(document.documentElement);return {palette:document.documentElement.dataset.emberPalette,paragraphLineHeight:getComputedStyle(document.querySelector('main p')).lineHeight,states:[...new Set([...document.querySelectorAll('main .ember-js-content img')].map(img=>img.dataset.emberImageState))],images:[...document.querySelectorAll('main .ember-js-content img')].map(img=>({src:img.getAttribute('src'),width:img.getBoundingClientRect().width,height:img.getBoundingClientRect().height})),link:root.getPropertyValue('--site-link').trim(),visited:root.getPropertyValue('--site-link-visited').trim(),hover:root.getPropertyValue('--site-link-hover').trim(),elevated:root.getPropertyValue('--site-link-elevated').trim(),elevatedVisited:root.getPropertyValue('--site-link-elevated-visited').trim(),elevatedHover:root.getPropertyValue('--site-link-elevated-hover').trim(),header:getComputedStyle(document.querySelector('.site-header')).backgroundColor,body:getComputedStyle(document.body).backgroundColor}})())"
            )
        )
        self.assertEqual(restored["palette"], "3400k-light")
        self.assertEqual(restored["paragraphLineHeight"], state["paragraphLineHeight"])
        self.assertEqual(restored["states"], ["source"])
        self.assertEqual(restored["link"], "#98074F")
        self.assertEqual(restored["visited"], "#844601")
        self.assertEqual(restored["hover"], "#342F2C")
        self.assertEqual(restored["elevated"], "#98074F")
        self.assertEqual(restored["elevatedVisited"], "#844601")
        self.assertEqual(restored["elevatedHover"], "#342F2C")
        self.assertEqual(restored["header"], "rgb(249, 249, 248)")
        self.assertEqual(restored["body"], "rgb(249, 249, 248)")
        self.assertTrue(
            all(
                "/images/ember-1200k/" not in image["src"]
                for image in restored["images"]
            )
        )
        self.assertEqual(len(restored["images"]), len(state["images"]))
        for mapped, source in zip(state["images"], restored["images"], strict=True):
            self.assertLessEqual(abs(mapped["width"] - source["width"]), 1.0)
            self.assertLessEqual(abs(mapped["height"] - source["height"]), 1.0)
            self.assertEqual(
                mapped["width"] >= mapped["height"], source["width"] >= source["height"]
            )

        self.cdp.call(
            "Emulation.setEmulatedMedia",
            {"features": [{"name": "prefers-color-scheme", "value": "dark"}]},
        )
        self.cdp.evaluate(
            "new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))",
            await_promise=True,
        )
        self.assertEqual(
            self.cdp.evaluate("document.documentElement.dataset.emberPalette"),
            "3400k-dark",
        )
        dark_roles = json.loads(
            self.cdp.evaluate(
                "JSON.stringify((()=>{const root=getComputedStyle(document.documentElement);return {link:root.getPropertyValue('--site-link').trim(),visited:root.getPropertyValue('--site-link-visited').trim(),hover:root.getPropertyValue('--site-link-hover').trim(),elevated:root.getPropertyValue('--site-link-elevated').trim(),elevatedVisited:root.getPropertyValue('--site-link-elevated-visited').trim(),elevatedHover:root.getPropertyValue('--site-link-elevated-hover').trim(),header:getComputedStyle(document.querySelector('.site-header')).backgroundColor}})())"
            )
        )
        self.assertEqual(
            dark_roles,
            {
                "link": "#F7B7AA",
                "visited": "#915E42",
                "hover": "#DCD9BF",
                "elevated": "#F7B7AA",
                "elevatedVisited": "#DEA460",
                "elevatedHover": "#DCD9BF",
                "header": "rgb(19, 16, 15)",
            },
        )

        self.cdp.evaluate(
            "document.querySelector('[data-ember-temperature-choice=\"1200k\"]').click()"
        )
        dynamic = self.cdp.evaluate(
            "new Promise(resolve=>{const img=document.createElement('img');img.dataset.emberOriginalSrc='/images/blog/great_wave_puzzle.jpg';img.addEventListener('load',()=>resolve(JSON.stringify({src:img.getAttribute('src'),state:img.dataset.emberImageState,loaded:img.naturalWidth>0})),{once:true});document.querySelector('main .ember-js-content').append(img)})",
            await_promise=True,
        )
        self.assertEqual(
            json.loads(dynamic),
            {
                "src": "/images/ember-1200k/blog/great_wave_puzzle.png",
                "state": "1200k",
                "loaded": True,
            },
        )

        fallback = self.cdp.evaluate(
            "new Promise(resolve=>{const img=document.createElement('img');img.dataset.emberOriginalSrc='/images/missing-image.png';let errors=0;img.addEventListener('error',()=>{errors+=1;if(errors===2)resolve(img.dataset.emberImageState)});document.querySelector('main .ember-js-content').append(img)})",
            await_promise=True,
        )
        self.assertEqual(fallback, "fallback")

        self.cdp.call(
            "Emulation.setDeviceMetricsOverride",
            {"width": 375, "height": 812, "deviceScaleFactor": 1, "mobile": True},
        )
        self.cdp.evaluate(
            "document.querySelector('label[for=\"nav-trigger\"]').click()"
        )
        mobile = json.loads(
            self.cdp.evaluate(
                "JSON.stringify((()=>{const h=document.querySelector('.site-header').getBoundingClientRect(),p=document.querySelector('.ember-palette-switcher').getBoundingClientRect(),about=[...document.querySelectorAll('.page-link')].find(link=>link.textContent.trim()==='About').getBoundingClientRect(),buttons=[...document.querySelectorAll('.ember-palette-switcher button')].map(button=>button.getBoundingClientRect());return {contained:p.top>=about.bottom-0.5,overflow:document.documentElement.scrollWidth>innerWidth,sameRow:Math.abs(buttons[0].top-buttons[1].top)<0.5,buttons:buttons.map(rect=>rect.height)}})())"
            )
        )
        self.assertTrue(mobile["contained"])
        self.assertFalse(mobile["overflow"])
        self.assertTrue(mobile["sameRow"])
        self.assertTrue(all(height >= 44 for height in mobile["buttons"]))

        self.cdp.call(
            "Emulation.setDeviceMetricsOverride",
            {"width": 1280, "height": 720, "deviceScaleFactor": 1, "mobile": False},
        )
        self.cdp.navigate(self.base_url + "/blog.html")
        infinite = json.loads(
            self.cdp.evaluate(
                "new Promise((resolve,reject)=>{window.scrollTo(0,document.body.scrollHeight);const deadline=Date.now()+5000,timer=setInterval(()=>{const posts=document.querySelectorAll('.post-list .post').length;if(posts>=10){clearInterval(timer);const images=[...document.querySelectorAll('.post-list img')],codeBlocks=[...document.querySelectorAll('.post-list .highlight')];resolve(JSON.stringify({posts,states:[...new Set(images.map(img=>img.dataset.emberImageState))],loaded:images.every(img=>img.complete&&img.naturalWidth>0),codeBlocks:codeBlocks.length,codePalettes:[...new Set(codeBlocks.map(block=>block.dataset.emberPalette))]}))}else if(Date.now()>deadline){clearInterval(timer);reject(new Error('infinite scroll timeout'))}},50)})",
                await_promise=True,
            )
        )
        self.assertGreaterEqual(infinite["posts"], 10)
        self.assertEqual(infinite["states"], ["1200k"])
        self.assertTrue(infinite["loaded"])
        self.assertGreater(infinite["codeBlocks"], 0)
        self.assertEqual(infinite["codePalettes"], ["1200k-dark"])

        self.cdp.call("Emulation.setScriptExecutionDisabled", {"value": True})
        self.cdp.navigate(self.base_url + PHOTO_PAGE + "#update-finished", settle=False)
        no_script_requests = [
            event["params"]["request"]["url"]
            for event in self.cdp.events
            if event.get("method") == "Network.requestWillBeSent"
        ]
        self.cdp.call("Emulation.setScriptExecutionDisabled", {"value": False})
        no_script_state = json.loads(
            self.cdp.evaluate(
                "JSON.stringify((()=>{const visible=element=>element&&getComputedStyle(element).display!=='none'&&element.getBoundingClientRect().width>0&&element.getBoundingClientRect().height>0,jsContent=document.querySelector('.ember-js-content'),fallback=document.querySelector('.ember-noscript-content'),target=document.getElementById('update-finished'),targetRect=target.getBoundingClientRect();return {jsVisible:visible(jsContent),fallbackVisible:visible(fallback),visiblePosts:[...document.querySelectorAll('.post')].filter(visible).length,visibleImages:[...document.querySelectorAll('main img')].filter(visible).length,fragmentTargets:document.querySelectorAll('#update-finished').length,fragmentInView:targetRect.top>=-1&&targetRect.top<innerHeight,fragmentScrollY:scrollY}})())"
            )
        )
        self.assertFalse(no_script_state["jsVisible"])
        self.assertTrue(no_script_state["fallbackVisible"])
        self.assertEqual(no_script_state["visiblePosts"], 1)
        self.assertEqual(no_script_state["visibleImages"], 4)
        self.assertEqual(no_script_state["fragmentTargets"], 1)
        self.assertTrue(no_script_state["fragmentInView"])
        self.assertGreater(no_script_state["fragmentScrollY"], 1000)
        no_script_image_requests = [
            url
            for url in no_script_requests
            if "/images/" in url
            and url.lower().endswith((".jpg", ".jpeg", ".png", ".svg"))
        ]
        self.assertEqual(len(no_script_image_requests), 4)
        self.assertTrue(
            all("/images/ember-1200k/" not in url for url in no_script_image_requests)
        )

    def test_surface_roles_and_code_subtheme_contracts(self) -> None:
        cases = (
            {
                "media": "light",
                "temperature": "3400k",
                "palette": "3400k-light",
                "header": "rgb(249, 249, 248)",
                "body": "rgb(249, 249, 248)",
                "blockquote": "rgb(241, 241, 240)",
                "inlineCode": "rgb(241, 241, 240)",
                "tableHeader": "rgb(236, 236, 235)",
                "tableZebra": "rgb(241, 241, 240)",
                "codePalette": "3400k-dark",
                "codeBackground": "rgb(30, 25, 24)",
                "codeToken": "rgb(212, 134, 195)",
            },
            {
                "media": "dark",
                "temperature": "3400k",
                "palette": "3400k-dark",
                "header": "rgb(19, 16, 15)",
                "body": "rgb(5, 4, 4)",
                "blockquote": "rgb(19, 16, 15)",
                "inlineCode": "rgb(41, 33, 31)",
                "tableHeader": "rgb(30, 25, 24)",
                "tableZebra": "rgb(19, 16, 15)",
                "codePalette": "3400k-dark",
                "codeBackground": "rgb(30, 25, 24)",
                "codeToken": "rgb(212, 134, 195)",
            },
            {
                "media": "light",
                "temperature": "1200k",
                "palette": "1200k-dark",
                "header": "rgb(23, 19, 19)",
                "body": "rgb(5, 4, 4)",
                "blockquote": "rgb(23, 19, 19)",
                "inlineCode": "rgb(38, 31, 29)",
                "tableHeader": "rgb(23, 19, 19)",
                "tableZebra": "rgb(23, 19, 19)",
                "codePalette": "1200k-dark",
                "codeBackground": "rgb(23, 19, 19)",
                "codeToken": "rgb(246, 143, 150)",
            },
        )

        for expected in cases:
            with self.subTest(palette=expected["palette"]):
                self.cdp.call(
                    "Emulation.setEmulatedMedia",
                    {
                        "features": [
                            {
                                "name": "prefers-color-scheme",
                                "value": expected["media"],
                            }
                        ]
                    },
                )
                self.cdp.navigate(self.base_url + CODE_PAGE)
                self.cdp.evaluate(
                    f'document.querySelector(\'[data-ember-temperature-choice="{expected["temperature"]}"]\').click()'
                )
                self.cdp.evaluate(
                    "new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))",
                    await_promise=True,
                )
                actual = json.loads(
                    self.cdp.evaluate(
                        """
JSON.stringify((() => {
  const probe = document.createElement('div');
  probe.innerHTML = '<blockquote>quote</blockquote><table><thead><tr><th>head</th></tr></thead><tbody><tr><td>one</td></tr><tr><td>two</td></tr></tbody></table>';
  document.querySelector('main').append(probe);
  const block = document.querySelector('main .highlight');
  const inlineCode = document.querySelector('main p code');
  const background = element => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;
    const context = canvas.getContext('2d');
    context.fillStyle = getComputedStyle(element).backgroundColor;
    context.fillRect(0, 0, 1, 1);
    const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;
    return `rgb(${red}, ${green}, ${blue})`;
  };
  const result = {
    palette: document.documentElement.dataset.emberPalette,
    header: background(document.querySelector('.site-header')),
    body: background(document.body),
    blockquote: background(probe.querySelector('blockquote')),
    inlineCode: background(inlineCode),
    tableHeader: background(probe.querySelector('th')),
    tableZebra: background(probe.querySelector('tbody tr:nth-child(even)')),
    codePalette: block.dataset.emberPalette,
    codeBackground: background(block),
    codeToken: getComputedStyle(block.querySelector('.k')).color,
  };
  probe.remove();
  return result;
})())
                        """
                    )
                )
                expected_actual = {
                    key: value
                    for key, value in expected.items()
                    if key not in {"media", "temperature"}
                }
                self.assertEqual(actual, expected_actual)


if __name__ == "__main__":
    unittest.main()
