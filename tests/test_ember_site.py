from __future__ import annotations

import hashlib
import json
import posixpath
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EXCLUDED_SITE_PREFIXES = ("dots/", "gridDots/", "randomGrids/")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}


class MainImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.main_depth = 0
        self.sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "main":
            self.main_depth += 1
        if self.main_depth and tag == "img":
            source = attributes.get("data-ember-original-src") or attributes.get("src")
            if source:
                self.sources.append(source)

    def handle_endtag(self, tag: str) -> None:
        if tag == "main" and self.main_depth:
            self.main_depth -= 1


def derivative_for(source: str) -> Path | None:
    parsed = urlparse(source)
    if parsed.hostname not in {
        None,
        "usuallypragmatic.com",
        "www.usuallypragmatic.com",
    }:
        return None
    path = posixpath.normpath(parsed.path)
    if Path(path).suffix.lower() not in IMAGE_EXTENSIONS:
        return None
    if path.startswith("/images/"):
        relative = Path(path.removeprefix("/images/"))
        if relative.parts[0] in {"favicon", "ember-1200k"}:
            return None
    elif path.startswith("/attachments/"):
        relative = Path("attachments") / path.removeprefix("/attachments/")
    else:
        return None
    return ROOT / "images" / "ember-1200k" / relative.with_suffix(".png")


class EmberSiteTests(unittest.TestCase):
    def test_normal_shell_loads_ember_but_utility_pages_do_not(self) -> None:
        default = (ROOT / "_layouts" / "default.html").read_text()
        head = (ROOT / "_includes" / "head.html").read_text()
        header = (ROOT / "_includes" / "header.html").read_text()
        dots_layout = (ROOT / "_layouts" / "dots_layout.html").read_text()
        runtime = (ROOT / "js" / "ember-site.js").read_text()

        self.assertIn('data-ember-palette="3400k-light"', default)
        self.assertIn('id="ember-content-template"', default)
        self.assertIn("contentTemplate.replaceWith", runtime)
        self.assertIn("/assets/ember/ember.css", head)
        self.assertIn("/js/ember-site.js", head)
        self.assertIn('class="ember-palette-switcher"', header)
        self.assertLess(
            header.index('class="site-nav"'),
            header.index('class="ember-palette-switcher"'),
        )
        self.assertNotIn("ember", dots_layout.lower())

        for utility in ("dots", "gridDots", "randomGrids"):
            page = (ROOT / utility / "index.html").read_text()
            self.assertIn("layout: dots_layout", page)

    def test_vendored_ember_css_is_commit_pinned(self) -> None:
        css = (ROOT / "assets" / "ember" / "ember.css").read_bytes()
        self.assertEqual(
            hashlib.sha256(css).hexdigest(),
            "02f364b359718214d3a0245d3de6cbb0ead4d883dd25c49eec522d04da82eada",
        )
        palette = json.loads(
            (ROOT / "assets" / "ember" / "1200k-dark-image-palette.json").read_text()
        )
        self.assertEqual(
            palette["source"]["commit"],
            "bdc5b4268f9d20949fa6d5a3866660521b7852ec",
        )
        self.assertEqual(len(palette["family"]["continuous_rgb"]), 256)

    def test_active_shell_and_syntax_styles_use_ember_roles(self) -> None:
        custom = (ROOT / "_sass" / "minima" / "custom-styles.scss").read_text()
        syntax = (
            ROOT / "_sass" / "minima" / "skins" / "syntax-gruvbox-dark.scss"
        ).read_text()

        self.assertIn("position: sticky", custom)
        self.assertIn("grid-template-rows: auto", custom)
        self.assertIn("--site-link: var(--ember-terminal-red)", custom)
        self.assertRegex(
            custom,
            re.compile(
                r'\.ember-palette-switcher button\[aria-pressed="true"\]\s*\{[^}]*color: var\(--ember-fg-1\)',
                re.DOTALL,
            ),
        )
        self.assertNotRegex(syntax, re.compile(r"#[0-9a-fA-F]{3,8}"))
        for role in (
            "--ember-fg-0",
            "--ember-fg-2",
            "--ember-bg-2",
            "--ember-bg-3",
            "--ember-terminal-red",
            "--ember-terminal-green",
            "--ember-terminal-yellow",
            "--ember-terminal-blue",
            "--ember-terminal-magenta",
            "--ember-terminal-cyan",
        ):
            self.assertIn(role, syntax)

    def test_generated_image_manifest_is_complete_and_grounded(self) -> None:
        manifest_path = ROOT / "images" / "ember-1200k" / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        builder = (ROOT / "tools" / "build_ember_images.py").read_text()
        self.assertIn("ImageOps.exif_transpose", builder)
        self.assertNotIn("np.quantile", builder)
        self.assertIn("normalized = np.clip(lightness, 0.0, 1.0)", builder)
        self.assertEqual(manifest["palette"], "1200k-dark")
        self.assertEqual(manifest["mapping"]["source_coordinate"], "Oklab L")
        self.assertEqual(manifest["mapping"]["normalization"], "none")
        self.assertEqual(manifest["mapping"]["source_range"], [0.0, 1.0])
        self.assertEqual(len(manifest["images"]), 69)
        self.assertLessEqual(manifest["budgets"]["actual_total_bytes"], 25_000_000)

        for record in manifest["images"]:
            source = ROOT / record["source"]
            output = ROOT / record["output"]
            self.assertTrue(source.is_file(), record["source"])
            self.assertTrue(output.is_file(), record["output"])
            self.assertEqual(
                hashlib.sha256(source.read_bytes()).hexdigest(), record["source_sha256"]
            )
            self.assertEqual(
                hashlib.sha256(output.read_bytes()).hexdigest(), record["output_sha256"]
            )
            self.assertGreaterEqual(record["source_output_oklab_l_correlation"], 0.85)
            with Image.open(output) as image:
                self.assertEqual(image.mode, "P")
                self.assertEqual(image.size, (record["width"], record["height"]))
                self.assertLessEqual(image.width, 1200)

    def test_javascript_markup_defers_original_image_requests(self) -> None:
        deferred = 0
        fallbacks = 0
        for page in SITE.rglob("*.html"):
            relative = page.relative_to(SITE).as_posix()
            if relative.startswith(EXCLUDED_SITE_PREFIXES):
                continue
            html = page.read_text(errors="ignore")
            for tag in re.findall(r"<img\b[^>]*>", html, flags=re.IGNORECASE):
                if "data-ember-original-src=" in tag:
                    deferred += 1
                    self.assertIsNone(
                        re.search(r"\ssrc=", tag), f"eager image in {relative}: {tag}"
                    )
            for fallback in re.findall(
                r"<noscript>(.*?)</noscript>", html, flags=re.IGNORECASE | re.DOTALL
            ):
                fallbacks += len(
                    re.findall(r"<img\b[^>]*\ssrc=", fallback, flags=re.IGNORECASE)
                )
        self.assertGreater(deferred, 70)
        self.assertEqual(fallbacks, deferred)

    def test_every_built_main_image_has_a_1200k_derivative(self) -> None:
        self.assertTrue(SITE.is_dir(), "run the Jekyll build before this test")
        checked = 0
        for page in SITE.rglob("*.html"):
            relative_page = page.relative_to(SITE).as_posix()
            if relative_page.startswith(EXCLUDED_SITE_PREFIXES):
                continue
            parser = MainImageParser()
            parser.feed(page.read_text(errors="ignore"))
            for source in parser.sources:
                derivative = derivative_for(source)
                if derivative is None:
                    continue
                checked += 1
                self.assertTrue(derivative.is_file(), f"{relative_page}: {source}")
        self.assertGreater(checked, 70)

    def test_built_utility_pages_remain_outside_ember_shell(self) -> None:
        for utility in EXCLUDED_SITE_PREFIXES:
            page = (SITE / utility / "index.html").read_text()
            self.assertNotIn("data-ember-palette", page)
            self.assertNotIn("ember-site.js", page)
            self.assertNotIn("ember-palette-switcher", page)

    def test_every_other_built_html_page_uses_ember_shell(self) -> None:
        checked = 0
        for path in SITE.rglob("*.html"):
            relative = path.relative_to(SITE).as_posix()
            if relative.startswith(EXCLUDED_SITE_PREFIXES):
                continue
            page = path.read_text(errors="ignore")
            self.assertIn("data-ember-palette", page, relative)
            self.assertIn("ember-site.js", page, relative)
            self.assertIn("ember-palette-switcher", page, relative)
            checked += 1
        self.assertGreater(checked, 60)


if __name__ == "__main__":
    unittest.main()
