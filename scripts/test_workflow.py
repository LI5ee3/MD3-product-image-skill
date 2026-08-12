#!/usr/bin/env python3
"""Small end-to-end functional check for the local workflow scripts."""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from compose_scene import placement_profile
from scene_prompt import PRODUCT_AREA_POLICY, information_safe_zone_block


SCRIPTS = Path(__file__).resolve().parent


def run(script: str, *arguments: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed.stdout


def must_fail(script: str, *arguments: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    if not completed.returncode:
        raise AssertionError(f"expected failure: {script}")
    return completed.stderr or completed.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert placement_profile(1.50) == ("WIDE", 0.68, 0.18)
    assert placement_profile(0.80) == ("TALL", 0.52, 0.12)
    assert placement_profile(1.00) == ("STANDARD", 0.52, 0.18)

    with tempfile.TemporaryDirectory(prefix="md3-product-image-") as temp:
        root = Path(temp)
        output_root = root / "products"
        reference = root / "product.png"
        logo = root / "logo.png"
        master_background = root / "generated-master-background.png"
        sku_background = root / "generated-sku-background.png"
        sku_product = root / "sku-product.png"

        product_image = Image.new("RGBA", (300, 400), (0, 0, 0, 0))
        ImageDraw.Draw(product_image).rounded_rectangle(
            (120, 80, 270, 330), radius=55, fill="#EA4335"
        )
        product_image.save(reference)
        sku_product_image = Image.new("RGBA", (300, 400), (0, 0, 0, 0))
        ImageDraw.Draw(sku_product_image).rounded_rectangle(
            (120, 80, 270, 330), radius=55, fill="#4285F4"
        )
        sku_product_image.save(sku_product)
        logo_image = Image.new("RGBA", (180, 80), (0, 0, 0, 0))
        ImageDraw.Draw(logo_image).rounded_rectangle(
            (20, 15, 150, 60), radius=10, fill="#202124"
        )
        logo_image.save(logo)
        Image.new("RGB", (300, 400), "#F4F6F8").save(master_background)
        Image.new("RGB", (300, 400), "#EDF3FA").save(sku_background)

        layout_report = json.loads(
            run(
                "measure_text.py",
                "--complete-name",
                "Acme Watch",
                "--brand",
                "Acme",
                "--remaining-name",
                "Watch",
                "--logo-type",
                "GRAPHIC",
                "--title-lines",
                "1",
                "--version",
                "Global",
                "--product-reference",
                str(reference),
                "--logo",
                str(logo),
                "--output-root",
                str(output_root),
                "--canvas-height",
                "400",
            )
        )
        product_dir = output_root / "Acme Watch"
        layout = product_dir / "layout.json"
        assert layout_report["product_reference"]["ratio_exact_3_4"] is True
        assert layout_report["product_reference"]["visible_bbox"] == {
            "left": 120,
            "top": 80,
            "right": 271,
            "bottom": 331,
        }
        assert layout_report["logo"]["visible_bbox"] == {
            "left": 20,
            "top": 15,
            "right": 151,
            "bottom": 61,
        }
        assert layout_report["rendered_title"] == "Acme Watch"

        text_logo_report = json.loads(
            run(
                "measure_text.py",
                "--complete-name",
                "Garmin Forerunner 965",
                "--brand",
                "Garmin",
                "--remaining-name",
                "Forerunner 965",
                "--logo-type",
                "TEXT",
                "--title-lines",
                "1",
                "--product-reference",
                str(reference),
                "--logo",
                str(logo),
                "--output-root",
                str(root / "text-logo-products"),
                "--canvas-height",
                "400",
            )
        )
        assert text_logo_report["rendered_title"] == "Forerunner 965"
        assert text_logo_report["title_lines"] == ["Forerunner 965"]
        text_logo_dir = root / "text-logo-products" / "Garmin Forerunner 965"
        assert "FAILURE_RECORD_WITHOUT_SCENE_ATTEMPT" in must_fail(
            "scene_prompt.py",
            "record-failure",
            "--log",
            str(text_logo_dir / "scene-failures.json"),
            "--mode",
            "MASTER",
            "--target",
            "legacy",
            "--failed-check",
            "Legacy failure",
            "--correction",
            "Legacy correction",
        )
        text_logo_state = json.loads(
            (text_logo_dir / "scene-attempts.json").read_text(encoding="utf-8")
        )
        assert text_logo_state["active_run_id"] is None
        assert not (text_logo_dir / "scene-failures.json").exists()

        prompt = run(
            "scene_prompt.py",
            "build",
            "--mode",
            "MASTER",
            "--layout",
            str(layout),
            "--target",
            "01",
        )
        expected_prompt = (
            SCRIPTS.parent / "references" / "image-gen-prompt.txt"
        ).read_text(encoding="utf-8").rstrip("\n")
        safe_zone_block = information_safe_zone_block(layout_report)
        assert prompt == (
            f"{expected_prompt}\n\n{safe_zone_block}\n\n{PRODUCT_AREA_POLICY}"
        )
        assert "FINAL_INFORMATION_SAFE_ZONE" in safe_zone_block
        assert "x 0.0%" in safe_zone_block
        assert "y 0.0%" in safe_zone_block
        assert "expands the union by 5.0%" in safe_zone_block
        assert "TITLE_LINE_RECT_1" not in safe_zone_block
        assert "CONNECTOR" not in safe_zone_block
        assert "continue the geometric background" not in safe_zone_block
        assert "Do not merge" not in safe_zone_block

        failure_log = product_dir / "scene-failures.json"
        run(
            "scene_prompt.py",
            "record-failure",
            "--log",
            str(failure_log),
            "--mode",
            "MASTER",
            "--target",
            "01",
            "--failed-check",
            "A card edge crosses the final information safe zone",
            "--correction",
            "Move the card edge outside the final information safe zone",
        )
        retry_prompt = run(
            "scene_prompt.py",
            "build",
            "--mode",
            "MASTER",
            "--layout",
            str(layout),
            "--target",
            "01",
        )
        assert retry_prompt.startswith(
            f"{expected_prompt}\n\n{safe_zone_block}\n\nTemporary corrections accumulated for this product:"
        )
        assert retry_prompt.count(
            "A card edge crosses the final information safe zone"
        ) == 1
        assert retry_prompt.count(
            "Move the card edge outside the final information safe zone"
        ) == 1
        assert retry_prompt.endswith(PRODUCT_AREA_POLICY)

        limit_product_dir = root / "text-logo-products" / "Garmin Forerunner 965"
        limit_layout = limit_product_dir / "layout.json"
        limit_failure_log = limit_product_dir / "scene-failures.json"
        for attempt in range(3):
            limit_prompt = run(
                "scene_prompt.py",
                "build",
                "--mode",
                "MASTER",
                "--layout",
                str(limit_layout),
                "--target",
                "limit",
            )
            for previous in range(attempt):
                assert limit_prompt.count(f"Failure {previous + 1}") == 1
                assert limit_prompt.count(f"Correction {previous + 1}") == 1
            run(
                "scene_prompt.py",
                "record-failure",
                "--log",
                str(limit_failure_log),
                "--mode",
                "MASTER",
                "--target",
                "limit",
                "--failed-check",
                f"Failure {attempt + 1}",
                "--correction",
                f"Correction {attempt + 1}",
            )
        assert "ATTEMPT_LIMIT_REACHED" in must_fail(
            "scene_prompt.py",
            "build",
            "--mode",
            "MASTER",
            "--layout",
            str(limit_layout),
            "--target",
            "limit",
        )

        bad_color_error = must_fail(
            "artifact_flow.py",
            "preview",
            "--generated-background",
            str(master_background),
            "--product",
            str(reference),
            "--product-dir",
            str(product_dir),
            "--candidate-id",
            "01",
            "--text-color",
            "202124",
            "--version-color",
            "202124",
        )
        assert "VERSION_COLOR_TOO_PROMINENT" in bad_color_error, bad_color_error
        assert not list(product_dir.glob("master-candidate-01*"))

        run(
            "artifact_flow.py",
            "preview",
            "--generated-background",
            str(master_background),
            "--product",
            str(reference),
            "--product-dir",
            str(product_dir),
            "--candidate-id",
            "01",
            "--text-color",
            "202124",
            "--version-color",
            "5F6368",
        )
        run(
            "artifact_flow.py",
            "candidate",
            "--product-dir",
            str(product_dir),
            "--candidate-id",
            "01",
        )
        assert not any((product_dir / "output").iterdir())
        assert (product_dir / "master-candidate-01.png").is_file()
        assert (product_dir / "master-candidate-01-thumb.png").is_file()
        assert (product_dir / "master-candidate-01-background.png").is_file()
        assert (product_dir / "master-candidate-01-product.png").is_file()
        assert (product_dir / "master-candidate-01-shadow.png").is_file()

        run(
            "artifact_flow.py",
            "bind",
            "--product-dir",
            str(product_dir),
            "--candidate-id",
            "01",
        )
        assert not list(product_dir.glob("master-candidate-01*"))
        assert {path.name for path in (product_dir / "output").iterdir()} == {
            "ORIGINAL_MASTER_FINAL.png"
        }
        assert (product_dir / "ORIGINAL_MASTER_BACKGROUND.png").is_file()
        assert (product_dir / "ORIGINAL_MASTER_PRODUCT.png").is_file()
        assert (product_dir / "ORIGINAL_MASTER_SHADOW.png").is_file()
        master_manifest = json.loads((product_dir / "master.json").read_text())
        assert master_manifest["scene_composite"]["shadow"]["angle_degrees"] == 50
        assert master_manifest["scene_composite"]["shadow"]["opacity"] == 0.28
        assert set(master_manifest["scene_composite"]) == {"product_box", "shadow"}
        master_hash = sha256(product_dir / "master.json")

        sku_prompt = run(
            "scene_prompt.py",
            "build",
            "--mode",
            "SKU",
            "--layout",
            str(layout),
            "--master",
            str(product_dir / "master.json"),
        )
        variant_reference = (
            SCRIPTS.parent / "references" / "replace-variant-block.md"
        ).read_text(encoding="utf-8")
        variant_prompt = variant_reference.split("```text\n", 1)[1].split(
            "\n```", 1
        )[0]
        assert sku_prompt.startswith(
            f"{expected_prompt}\n\n{safe_zone_block}\n\n{variant_prompt}\n\n"
        )
        assert sku_prompt.count(
            "A card edge crosses the final information safe zone"
        ) == 1
        assert sku_prompt.count(
            "Move the card edge outside the final information safe zone"
        ) == 1
        assert sku_prompt.endswith(PRODUCT_AREA_POLICY)

        run(
            "artifact_flow.py",
            "sku",
            "--generated-background",
            str(sku_background),
            "--product",
            str(sku_product),
            "--product-dir",
            str(product_dir),
        )
        assert {path.name for path in (product_dir / "output").iterdir()} == {
            "ORIGINAL_MASTER_FINAL.png",
            "SKU_VARIANT-A.png",
        }
        assert (product_dir / "SKU_VARIANT-A-thumb.png").is_file()
        assert (product_dir / "SKU_VARIANT-A-background.png").is_file()
        assert (product_dir / "SKU_VARIANT-A-product.png").is_file()
        assert (product_dir / "SKU_VARIANT-A-shadow.png").is_file()
        assert sha256(product_dir / "master.json") == master_hash

        cached_logo = product_dir / "logo.png"
        cached_logo_bytes = cached_logo.read_bytes()
        cached_logo.write_bytes(b"tampered")
        assert "INFORMATION_ASSET_HASH_MISMATCH" in must_fail(
            "scene_prompt.py",
            "build",
            "--mode",
            "SKU",
            "--layout",
            str(layout),
            "--master",
            str(product_dir / "master.json"),
        )
        cached_logo.write_bytes(cached_logo_bytes)

        (product_dir / "ORIGINAL_MASTER_SCENE.png").write_bytes(b"tampered")
        assert "MASTER_HASH_MISMATCH" in must_fail(
            "scene_prompt.py",
            "build",
            "--mode",
            "SKU",
            "--layout",
            str(layout),
            "--master",
            str(product_dir / "master.json"),
        )

    print("md3-product-image workflow self-check passed")


if __name__ == "__main__":
    main()
