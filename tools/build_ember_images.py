#!/usr/bin/env python3
"""Build deterministic Ember 1200K derivatives for normal-site content images."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import resvg_py  # pyright: ignore[reportMissingImports]
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PALETTE_PATH = ROOT / "assets" / "ember" / "1200k-dark-image-palette.json"
OUTPUT_ROOT = ROOT / "images" / "ember-1200k"
RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
SOURCE_EXTENSIONS = RASTER_EXTENSIONS | {".svg"}
MAX_OUTPUT_WIDTH = 1200
MAX_OUTPUT_FILE_BYTES = 4_000_000
MAX_OUTPUT_TOTAL_BYTES = 25_000_000


def svg_dimensions(path: Path) -> tuple[int, int]:
    root = ET.fromstring(path.read_text())

    def pixels(value: str | None) -> float | None:
        if value is None:
            return None
        match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*(px|pt|in|cm|mm)?\s*", value)
        if not match:
            return None
        amount = float(match.group(1))
        scale = {
            None: 1.0,
            "px": 1.0,
            "pt": 96.0 / 72.0,
            "in": 96.0,
            "cm": 96.0 / 2.54,
            "mm": 96.0 / 25.4,
        }[match.group(2)]
        return amount * scale

    width = pixels(root.get("width"))
    height = pixels(root.get("height"))
    if width is None or height is None:
        view_box = root.get("viewBox")
        if view_box:
            values = [float(value) for value in re.split(r"[\s,]+", view_box.strip())]
            if len(values) == 4:
                width = width or values[2]
                height = height or values[3]
    if width is None or height is None or width <= 0 or height <= 0:
        raise ValueError(
            f"cannot determine positive SVG dimensions for {path.relative_to(ROOT)}"
        )
    return max(1, round(width)), max(1, round(height))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    rgb = np.asarray(rgb, dtype=float)
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def srgb_to_oklab(rgb: np.ndarray) -> np.ndarray:
    linear = srgb_to_linear(rgb)
    matrix_1 = np.array(
        [
            [0.4122214708, 0.5363325363, 0.0514459929],
            [0.2119034982, 0.6806995451, 0.1073969566],
            [0.0883024619, 0.2817188376, 0.6299787005],
        ]
    )
    matrix_2 = np.array(
        [
            [0.2104542553, 0.7936177850, -0.0040720468],
            [1.9779984951, -2.4285922050, 0.4505937099],
            [0.0259040371, 0.7827717662, -0.8086757660],
        ]
    )
    lms = np.tensordot(linear, matrix_1.T, axes=1)
    return np.tensordot(np.cbrt(lms), matrix_2.T, axes=1)


def source_paths() -> list[tuple[Path, Path]]:
    sources: list[tuple[Path, Path]] = []
    images_root = ROOT / "images"
    for path in images_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        relative = path.relative_to(images_root)
        if relative.parts[0] in {"favicon", "ember-1200k"}:
            continue
        sources.append((path, relative.with_suffix(".png")))

    attachments_root = ROOT / "attachments"
    for path in attachments_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        relative = Path("attachments") / path.relative_to(attachments_root)
        sources.append((path, relative.with_suffix(".png")))

    return sorted(sources, key=lambda item: item[1].as_posix())


def load_source_rgb(path: Path) -> tuple[np.ndarray, tuple[int, int]]:
    if path.suffix.lower() == ".svg":
        width, height = svg_dimensions(path)
        svg = path.read_text()
        root = ET.fromstring(svg)
        for attribute, pixels in (("width", width), ("height", height)):
            authored = root.get(attribute)
            if authored:
                pattern = rf"({attribute}\s*=\s*['\"])({re.escape(authored)})(['\"])"
                svg = re.sub(pattern, rf"\g<1>{pixels}\g<3>", svg, count=1)
        try:
            rendered = resvg_py.svg_to_bytes(
                svg_string=svg,
                resources_dir=str(path.parent),
                width=width,
                height=height,
                skip_system_fonts=True,
                font_files=[
                    str(ROOT / "assets" / "Crimson_Text" / "CrimsonText-Regular.ttf"),
                    str(
                        ROOT
                        / "assets"
                        / "Iosevka_Term_Slab_Light"
                        / "iosevka-term-slab-light.ttf"
                    ),
                ],
                font_family="Crimson Text",
                serif_family="Crimson Text",
                sans_serif_family="Crimson Text",
                monospace_family="Iosevka Term Slab Light",
            )
        except ValueError as error:
            raise ValueError(
                f"cannot render {path.relative_to(ROOT)}: {error}"
            ) from error
        image = Image.open(io.BytesIO(rendered))
    else:
        image = Image.open(path)

    with image:
        oriented = ImageOps.exif_transpose(image)
        if oriented is None:
            oriented = image
        rgba = oriented.convert("RGBA")
        # Existing content was authored for the site's original light canvas. Composite
        # transparency over white before measuring Oklab L so SVG equations and diagrams
        # preserve their browser-visible tonal structure rather than mapping invisible RGB.
        composite = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        composite.alpha_composite(rgba)
        rendered = composite.convert("RGB")
        if rendered.width > MAX_OUTPUT_WIDTH:
            height = round(rendered.height * MAX_OUTPUT_WIDTH / rendered.width)
            rendered = rendered.resize(
                (MAX_OUTPUT_WIDTH, height), Image.Resampling.LANCZOS
            )
        rgb = np.asarray(rendered, dtype=float) / 255.0
        return rgb, rendered.size


def palette_png(indices: np.ndarray, palette: np.ndarray) -> bytes:
    palette_rgb8 = np.rint(palette * 255.0).astype(np.uint8)
    mapped = Image.fromarray(indices.astype(np.uint8))
    mapped.putpalette(palette_rgb8.reshape(-1).tolist())
    output = io.BytesIO()
    mapped.save(output, format="PNG", compress_level=9)
    return output.getvalue()


def render(path: Path, palette: np.ndarray) -> tuple[bytes, dict[str, object]]:
    source_rgb, size = load_source_rgb(path)
    lightness = srgb_to_oklab(source_rgb)[..., 0]
    low, high = float(lightness.min()), float(lightness.max())
    normalized = np.clip(lightness, 0.0, 1.0)

    endpoint_lightness = srgb_to_oklab(palette[[0, -1]])[:, 0]
    if endpoint_lightness[0] > endpoint_lightness[1]:
        palette = palette[::-1]

    indices = np.rint(normalized * (len(palette) - 1)).astype(np.uint8)
    output_lightness = srgb_to_oklab(palette[indices])[..., 0]
    correlation = float(
        np.corrcoef(lightness.reshape(-1), output_lightness.reshape(-1))[0, 1]
    )
    if not np.isfinite(correlation):
        correlation = 1.0

    data = palette_png(indices, palette)
    metadata: dict[str, object] = {
        "width": size[0],
        "height": size[1],
        "source_oklab_l_range": [round(low, 10), round(high, 10)],
        "source_output_oklab_l_correlation": round(correlation, 10),
    }
    return data, metadata


def build(check: bool) -> int:
    palette_manifest = json.loads(PALETTE_PATH.read_text())
    palette = np.asarray(palette_manifest["family"]["continuous_rgb"], dtype=float)
    if palette.shape != (256, 3):
        raise ValueError(f"expected a 256x3 palette, found {palette.shape}")

    records = []
    expected_outputs: set[Path] = set()
    failures: list[str] = []

    for source, relative_output in source_paths():
        output = OUTPUT_ROOT / relative_output
        expected_outputs.add(output)
        data, metrics = render(source, palette)
        record = {
            "source": source.relative_to(ROOT).as_posix(),
            "source_sha256": sha256(source.read_bytes()),
            "output": output.relative_to(ROOT).as_posix(),
            "output_sha256": sha256(data),
            "output_bytes": len(data),
            **metrics,
        }
        records.append(record)

        if len(data) > MAX_OUTPUT_FILE_BYTES:
            failures.append(
                f"oversize {output.relative_to(ROOT)}: {len(data)} > {MAX_OUTPUT_FILE_BYTES} bytes"
            )

        if check:
            if not output.exists():
                failures.append(f"missing {output.relative_to(ROOT)}")
            elif output.read_bytes() != data:
                failures.append(f"stale {output.relative_to(ROOT)}")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)

    total_output_bytes = sum(record["output_bytes"] for record in records)
    if total_output_bytes > MAX_OUTPUT_TOTAL_BYTES:
        failures.append(
            f"derivative set is {total_output_bytes} bytes; budget is {MAX_OUTPUT_TOTAL_BYTES}"
        )

    manifest = {
        "schema_version": 1,
        "palette": palette_manifest["family"]["slug"],
        "palette_source": palette_manifest["source"],
        "mapping": palette_manifest["image_mapping"],
        "transparent_source_background": "#FFFFFF",
        "budgets": {
            "maximum_width": MAX_OUTPUT_WIDTH,
            "maximum_file_bytes": MAX_OUTPUT_FILE_BYTES,
            "maximum_total_bytes": MAX_OUTPUT_TOTAL_BYTES,
            "actual_total_bytes": total_output_bytes,
        },
        "images": records,
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    manifest_path = OUTPUT_ROOT / "manifest.json"

    if check:
        if not manifest_path.exists():
            failures.append(f"missing {manifest_path.relative_to(ROOT)}")
        elif manifest_path.read_bytes() != manifest_bytes:
            failures.append(f"stale {manifest_path.relative_to(ROOT)}")

        if OUTPUT_ROOT.exists():
            actual = {path for path in OUTPUT_ROOT.rglob("*.png") if path.is_file()}
            for extra in sorted(actual - expected_outputs):
                failures.append(f"unexpected {extra.relative_to(ROOT)}")
    else:
        OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(manifest_bytes)
        actual = {path for path in OUTPUT_ROOT.rglob("*.png") if path.is_file()}
        for stale in sorted(actual - expected_outputs):
            stale.unlink()

    if failures:
        print("Ember image derivatives are not current:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    verb = "verified" if check else "built"
    print(f"{verb} {len(records)} Ember 1200K image derivatives")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="verify tracked outputs without writing"
    )
    args = parser.parse_args()
    return build(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
