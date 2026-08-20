(() => {
  "use strict";

  const contentTemplate = document.getElementById("ember-content-template");
  if (contentTemplate) {
    contentTemplate.replaceWith(contentTemplate.content.cloneNode(true));
  }

  const root = document.documentElement;
  const storageKey = "usuallypragmatic.ember-temperature";
  const supportedImageExtensions = /\.(?:jpe?g|png|webp|gif|svg)$/i;
  const localHosts = new Set([
    window.location.hostname,
    "usuallypragmatic.com",
    "www.usuallypragmatic.com",
  ]);
  const darkPreference = window.matchMedia("(prefers-color-scheme: dark)");
  const controls = Array.from(document.querySelectorAll("[data-ember-temperature-choice]"));
  const themeColor = document.querySelector('meta[name="theme-color"]');

  const selectedTemperature = () =>
    root.dataset.emberTemperature === "1200k" ? "1200k" : "3400k";

  const familyFor = (temperature) => {
    if (temperature === "1200k") return "1200k-dark";
    return darkPreference.matches ? "3400k-dark" : "3400k-light";
  };

  const derivativePathFor = (source) => {
    let url;
    try {
      url = new URL(source, window.location.href);
    } catch (_) {
      return null;
    }

    if (!localHosts.has(url.hostname) || !supportedImageExtensions.test(url.pathname)) {
      return null;
    }

    let relative;
    if (url.pathname.startsWith("/images/")) {
      relative = url.pathname.slice("/images/".length);
      if (relative.startsWith("favicon/") || relative.startsWith("ember-1200k/")) {
        return null;
      }
    } else if (url.pathname.startsWith("/attachments/")) {
      relative = `attachments/${url.pathname.slice("/attachments/".length)}`;
    } else {
      return null;
    }

    relative = relative.replace(/\.[^./]+$/, ".png");
    return `/images/ember-1200k/${relative}`;
  };

  const rememberImageSource = (image) => {
    if (image.dataset.emberOriginalSrc === undefined) {
      image.dataset.emberOriginalSrc = image.getAttribute("src") || "";
    }
    if (image.dataset.emberOriginalSrcset === undefined) {
      image.dataset.emberOriginalSrcset = image.getAttribute("srcset") || "";
    }

    if (image.dataset.emberErrorHandler === "ready") return;
    image.dataset.emberErrorHandler = "ready";

    image.addEventListener("error", () => {
      if (image.dataset.emberImageState !== "1200k") return;
      image.dataset.emberImageState = "fallback";
      image.setAttribute("src", image.dataset.emberOriginalSrc);
      if (image.dataset.emberOriginalSrcset) {
        image.setAttribute("srcset", image.dataset.emberOriginalSrcset);
      }
    });
  };

  const applyImageState = (image, temperature) => {
    rememberImageSource(image);

    if (temperature !== "1200k") {
      image.dataset.emberImageState = "source";
      image.setAttribute("src", image.dataset.emberOriginalSrc);
      if (image.dataset.emberOriginalSrcset) {
        image.setAttribute("srcset", image.dataset.emberOriginalSrcset);
      } else {
        image.removeAttribute("srcset");
      }
      return;
    }

    const derivative = derivativePathFor(
      image.dataset.emberOriginalSrc || image.currentSrc || image.src,
    );
    if (!derivative) {
      image.dataset.emberImageState = "unmapped";
      return;
    }

    image.dataset.emberImageState = "1200k";
    image.removeAttribute("srcset");
    image.setAttribute("src", derivative);
  };

  const applyImages = (temperature, scope = document) => {
    const images = [];
    if (scope === document) {
      images.push(...document.querySelectorAll("main img"));
    } else if (scope instanceof HTMLImageElement && scope.closest("main")) {
      images.push(scope);
    } else if (scope.closest && scope.closest("main")) {
      images.push(...scope.querySelectorAll("img"));
    }
    images.forEach((image) => applyImageState(image, temperature));
  };

  const syncThemeColor = () => {
    if (!themeColor) return;
    themeColor.content = getComputedStyle(root).getPropertyValue("--ember-bg-0").trim();
  };

  const applyTemperature = (temperature, persist = true) => {
    const normalized = temperature === "1200k" ? "1200k" : "3400k";
    root.dataset.emberTemperature = normalized;
    root.dataset.emberPalette = familyFor(normalized);

    controls.forEach((control) => {
      control.setAttribute(
        "aria-pressed",
        String(control.dataset.emberTemperatureChoice === normalized),
      );
    });

    if (persist) {
      try {
        localStorage.setItem(storageKey, normalized);
      } catch (_) {
        // The palette remains usable when storage is unavailable.
      }
    }

    applyImages(normalized);
    requestAnimationFrame(syncThemeColor);
  };

  controls.forEach((control) => {
    control.addEventListener("click", () => {
      applyTemperature(control.dataset.emberTemperatureChoice);
    });
  });

  const handlePreferenceChange = () => {
    if (selectedTemperature() !== "3400k") return;
    root.dataset.emberPalette = familyFor("3400k");
    requestAnimationFrame(syncThemeColor);
  };
  if (darkPreference.addEventListener) {
    darkPreference.addEventListener("change", handlePreferenceChange);
  } else {
    darkPreference.addListener(handlePreferenceChange);
  }

  const main = document.querySelector("main");
  if (main) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            applyImages(selectedTemperature(), node);
          }
        });
      });
    });
    observer.observe(main, { childList: true, subtree: true });
  }

  applyTemperature(selectedTemperature(), false);
})();
