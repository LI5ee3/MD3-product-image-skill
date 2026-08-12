#!/usr/bin/env python3
"""Preview, create, bind, and verify candidate and SKU artifacts."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
SCENE_COMPOSE_SCRIPT = SCRIPTS_DIR / "compose_scene.py"
COMPOSE_SCRIPT = SCRIPTS_DIR / "compose_image.py"
VALIDATE_SCRIPT = SCRIPTS_DIR / "validate_final.py"
ATTEMPT_STATE_NAME = "scene-attempts.json"
TITLE_COLOR = "2C2C2C"
VERSION_COLOR = "5A5A5A"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ValueError(f"FILE_UNREADABLE: {path}: {exc}") from exc
    return digest.hexdigest()


def read_json(path: Path):
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"JSON_UNREADABLE: {path}: {exc}") from exc


def write_json_new(path: Path, data) -> None:
    if path.exists():
        raise ValueError(f"REFUSE_OVERWRITE: {path}")
    temporary = path.with_name(f".{path.name}.tmp")
    temporary_created = False
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            temporary_created = True
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temporary.replace(path)
    finally:
        if temporary_created and temporary.exists():
            temporary.unlink()


def write_json_replace(path: Path, data) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary_created = False
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            temporary_created = True
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temporary.replace(path)
    finally:
        if temporary_created and temporary.exists():
            temporary.unlink()


def safe_component(value: str, label: str) -> str:
    value = value.strip()
    if not value or value in {".", ".."} or any(char in value for char in "/\\\x00"):
        raise ValueError(f"{label}_INVALID")
    return value


def normalize_color(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    color = value.lstrip("#").upper()
    if not re.fullmatch(r"[0-9A-F]{6}", color):
        raise ValueError(f"{label}_INVALID")
    return color


def verify_information_assets(layout: dict, reusable_dir: Path) -> None:
    elements = layout.get("elements")
    assets = layout.get("information_assets")
    if not isinstance(elements, dict) or not isinstance(assets, dict):
        raise ValueError("INFORMATION_ASSETS_INVALID")
    try:
        expected = {"logo": elements["LOGO_RECT"]["asset"]}
        for index, title in enumerate(elements["TITLE_LINE_RECT"], start=1):
            expected[f"title_{index}"] = title["asset"]
        if "VERSION_TEXT_RECT" in elements:
            expected["version"] = elements["VERSION_TEXT_RECT"]["asset"]
    except (KeyError, TypeError) as exc:
        raise ValueError("LAYOUT_ELEMENTS_INVALID") from exc
    if set(assets) != set(expected):
        raise ValueError("INFORMATION_ASSET_SET_MISMATCH")
    for label, asset_name in expected.items():
        try:
            entry = assets[label]
            path = (reusable_dir / entry["path"]).resolve()
            expected_hash = entry["sha256"]
            expected_path = (reusable_dir / asset_name).resolve()
        except (KeyError, TypeError) as exc:
            raise ValueError(f"INFORMATION_ASSET_INVALID: {label}") from exc
        if path != expected_path or path.parent != reusable_dir:
            raise ValueError(f"INFORMATION_ASSET_PATH_MISMATCH: {label}")
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise ValueError(f"INFORMATION_ASSET_HASH_MISMATCH: {label}")


def load_product(product_dir_arg: str) -> tuple[Path, Path, dict]:
    product_dir = Path(product_dir_arg).expanduser().resolve()
    reusable_dir = product_dir / "reusable"
    layout_path = reusable_dir / "layout.json"
    if not product_dir.is_dir():
        raise ValueError(f"PRODUCT_DIRECTORY_MISSING: {product_dir}")
    layout = read_json(layout_path)
    if layout.get("product_directory") != str(product_dir):
        raise ValueError("PRODUCT_DIRECTORY_MISMATCH")
    verify_information_assets(layout, reusable_dir)
    output_dir = product_dir / "output"
    output_dir.mkdir(exist_ok=True)
    if not output_dir.is_dir():
        raise ValueError("OUTPUT_PATH_INVALID")
    return product_dir, layout_path, layout


def ensure_output_allowed(product_dir: Path) -> dict[str, str]:
    output_dir = product_dir / "output"
    result = {}
    for path in output_dir.iterdir():
        allowed = path.name == "ORIGINAL_MASTER_FINAL.png" or (
            path.is_file()
            and path.name.startswith("SKU_VARIANT-")
            and path.name != "SKU_VARIANT-.png"
            and path.suffix.lower() == ".png"
        )
        if not allowed or not path.is_file():
            raise ValueError(f"OUTPUT_CONTAINS_FORBIDDEN_FILE: {path.name}")
        result[path.name] = sha256_file(path)
    return result


def relative_entry(path: Path, product_dir: Path) -> dict[str, str]:
    return {
        "path": path.relative_to(product_dir).as_posix(),
        "sha256": sha256_file(path),
    }


def resolve_entry(
    entry: dict, product_dir: Path, expected: Path, label: str
) -> Path:
    try:
        path = (product_dir / entry["path"]).resolve()
        expected_hash = entry["sha256"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"MANIFEST_ENTRY_INVALID: {label}") from exc
    if path != expected or not path.is_file():
        raise ValueError(f"MANIFEST_PATH_MISMATCH: {label}")
    if sha256_file(path) != expected_hash:
        raise ValueError(f"MANIFEST_HASH_MISMATCH: {label}")
    return path


def copy_new(source_arg: str | Path, destination: Path) -> None:
    source = Path(source_arg).expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"SOURCE_FILE_MISSING: {source}")
    if destination.exists():
        raise ValueError(f"REFUSE_OVERWRITE: {destination}")
    shutil.copy2(source, destination)


def run_script(arguments: list[str]) -> dict:
    completed = subprocess.run(
        [sys.executable, *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ValueError(detail or f"SCRIPT_FAILED: {arguments[0]}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"SCRIPT_OUTPUT_INVALID: {arguments[0]}") from exc


def run_compose(
    scene: Path,
    layout: Path,
    output: Path,
    output_kind: str,
) -> dict:
    command = [
        str(COMPOSE_SCRIPT),
        "--scene",
        str(scene),
        "--layout",
        str(layout),
        "--output",
        str(output),
        "--output-kind",
        output_kind,
    ]
    return run_script(command)


def run_scene_compose(
    background: Path,
    product: Path,
    scene: Path,
    product_layer: Path,
    shadow_mask: Path,
) -> dict:
    if product_layer.exists() != shadow_mask.exists():
        raise ValueError("CACHED_PRODUCT_SHADOW_INCOMPLETE")
    command = [
        str(SCENE_COMPOSE_SCRIPT),
        "--background", str(background),
        "--product", str(product),
        "--output", str(scene),
        "--product-layer", str(product_layer),
        "--shadow-mask", str(shadow_mask),
    ]
    if product_layer.exists():
        command.append("--reuse-layers")
    return run_script(command)


def scene_composite_info(report: dict) -> dict:
    product_box = report.get("product_box")
    shadow = report.get("shadow")
    if not isinstance(product_box, dict) or not isinstance(shadow, dict):
        raise ValueError("SCENE_COMPOSITE_REPORT_INVALID")
    return {"product_box": product_box, "shadow": shadow}


def run_validate(image: Path, image_kind: str) -> None:
    run_script(
        [
            str(VALIDATE_SCRIPT),
            "--image-kind",
            image_kind,
            "--image",
            str(image),
        ]
    )


def scene_attempt_path(product_dir: Path) -> Path:
    return product_dir / ATTEMPT_STATE_NAME


def scene_attempt(product_dir: Path, mode: str, target: str) -> tuple[dict, dict]:
    path = scene_attempt_path(product_dir)
    if not path.is_file():
        raise ValueError("SCENE_ATTEMPT_STATE_MISSING: build the scene prompt first")
    state = read_json(path)
    run_id = state.get("active_run_id")
    runs = state.get("runs")
    if not run_id or not isinstance(runs, list):
        raise ValueError("ATTEMPT_STATE_INVALID")
    run = next((item for item in runs if item.get("run_id") == run_id), None)
    if not isinstance(run, dict):
        raise ValueError("ACTIVE_ATTEMPT_RUN_MISSING")
    if run.get("mode") != mode or run.get("target") != target:
        raise ValueError(
            "SCENE_TARGET_MISMATCH: expected "
            f"{run.get('mode')}/{run.get('target')}"
        )
    attempts = run.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        raise ValueError("SCENE_ATTEMPT_MISSING")
    current = attempts[-1]
    if current.get("status") != "PENDING":
        raise ValueError("SCENE_ATTEMPT_NOT_PENDING")
    return state, {"run": run, "attempt": current}


def accept_scene_attempt(
    product_dir: Path, mode: str, target: str
) -> dict[str, str | int]:
    state, info = scene_attempt(product_dir, mode, target)
    run = info["run"]
    attempt = info["attempt"]
    attempt["status"] = "ACCEPTED"
    run["status"] = "ACCEPTED"
    if mode == "SKU":
        state["active_run_id"] = None
    write_json_replace(scene_attempt_path(product_dir), state)
    return {
        "run_id": run["run_id"],
        "attempt": int(attempt["attempt"]),
        "prompt_path": str(attempt.get("prompt_path", "")),
        "prompt_sha256": str(attempt.get("prompt_sha256", "")),
    }


def close_accepted_master_run(product_dir: Path, candidate_id: str) -> None:
    path = scene_attempt_path(product_dir)
    state = read_json(path)
    run_id = state.get("active_run_id")
    runs = state.get("runs")
    if not run_id or not isinstance(runs, list):
        raise ValueError("ATTEMPT_STATE_INVALID")
    run = next((item for item in runs if item.get("run_id") == run_id), None)
    if (
        not isinstance(run, dict)
        or run.get("mode") != "MASTER"
        or run.get("target") != candidate_id
        or run.get("status") != "ACCEPTED"
    ):
        raise ValueError("ACCEPTED_MASTER_RUN_MISMATCH")
    attempts = run.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        raise ValueError("SCENE_ATTEMPT_MISSING")
    if attempts[-1].get("status") != "ACCEPTED":
        raise ValueError("MASTER_ATTEMPT_NOT_ACCEPTED")
    state["active_run_id"] = None
    write_json_replace(path, state)


def validate_information_colors(layout: dict, information: dict) -> None:
    elements = layout.get("elements")
    if not isinstance(elements, dict):
        raise ValueError("LAYOUT_ELEMENTS_INVALID")
    title_color = normalize_color(information.get("title_color"), "TEXT_COLOR")
    version_color = normalize_color(information.get("version_color"), "VERSION_COLOR")
    expected_version = VERSION_COLOR if "VERSION_TEXT_RECT" in elements else None
    if title_color != TITLE_COLOR or version_color != expected_version:
        raise ValueError("FIXED_INFORMATION_COLOR_MISMATCH")


def cleanup(paths: list[Path]) -> None:
    for path in paths:
        if path.is_file():
            path.unlink()


def candidate_paths(product_dir: Path, candidate_id: str) -> dict[str, Path]:
    if candidate_id.endswith(("-scene", "-preview")):
        raise ValueError("CANDIDATE_ID_RESERVED")
    prefix = f"master-candidate-{candidate_id}"
    reusable_dir = product_dir / "reusable"
    return {
        "background": product_dir / f"{prefix}-background.png",
        "product": reusable_dir / f"{prefix}-product.png",
        "shadow": reusable_dir / f"{prefix}-shadow.png",
        "scene": product_dir / f"{prefix}-scene.png",
        "final": product_dir / f"{prefix}.png",
        "manifest": product_dir / f"{prefix}.json",
    }


def preview_paths(product_dir: Path, candidate_id: str) -> dict[str, Path]:
    candidate_paths(product_dir, candidate_id)
    prefix = f"master-candidate-{candidate_id}-preview"
    reusable_dir = product_dir / "reusable"
    return {
        "background": product_dir / f"{prefix}-background.png",
        "product": reusable_dir / f"master-candidate-{candidate_id}-product.png",
        "shadow": reusable_dir / f"master-candidate-{candidate_id}-shadow.png",
        "scene": product_dir / f"{prefix}-scene.png",
        "final": product_dir / f"{prefix}.png",
        "manifest": product_dir / f"{prefix}.json",
    }


def current_attempt_info(product_dir: Path, candidate_id: str) -> dict:
    _, pending_info = scene_attempt(product_dir, "MASTER", candidate_id)
    run = pending_info["run"]
    attempt = pending_info["attempt"]
    return {
        "run_id": run["run_id"],
        "attempt": int(attempt["attempt"]),
        "prompt_path": str(attempt.get("prompt_path", "")),
        "prompt_sha256": str(attempt.get("prompt_sha256", "")),
    }


def create_preview(args: argparse.Namespace) -> None:
    product_dir, layout_path, layout = load_product(args.product_dir)
    candidate_id = safe_component(args.candidate_id, "CANDIDATE_ID")
    attempt_info = current_attempt_info(product_dir, candidate_id)
    if any(
        path.exists()
        for label, path in candidate_paths(product_dir, candidate_id).items()
        if label not in {"product", "shadow"}
    ):
        raise ValueError("CANDIDATE_ALREADY_EXISTS")
    paths = preview_paths(product_dir, candidate_id)
    if any(
        path.exists()
        for label, path in paths.items()
        if label not in {"product", "shadow"}
    ):
        raise ValueError("PREVIEW_ALREADY_EXISTS")
    output_before = ensure_output_allowed(product_dir)
    layers_existed = paths["product"].exists() and paths["shadow"].exists()
    created = [
        path for label, path in paths.items()
        if label not in {"product", "shadow"}
    ]
    if not layers_existed:
        created.extend((paths["product"], paths["shadow"]))
    try:
        product_source = Path(args.product).expanduser().resolve()
        expected_product_hash = layout.get("product_reference", {}).get("sha256")
        if not product_source.is_file() or sha256_file(product_source) != expected_product_hash:
            raise ValueError("MASTER_PRODUCT_REFERENCE_MISMATCH")
        copy_new(args.generated_background, paths["background"])
        scene_render = scene_composite_info(run_scene_compose(
            paths["background"],
            product_source,
            paths["scene"],
            paths["product"],
            paths["shadow"],
        ))
        render = run_compose(
            paths["scene"],
            layout_path,
            paths["final"],
            "CANDIDATE",
        )
        run_validate(paths["final"], "CANDIDATE")
        information = {
            "title_color": render.get("title_color"),
            "version_color": render.get("version_color"),
        }
        validate_information_colors(layout, information)
        manifest = {
            "schema": 1,
            "kind": "MASTER_CANDIDATE_PREVIEW",
            "candidate_id": candidate_id,
            "files": {
                "layout": relative_entry(layout_path, product_dir),
                "background": relative_entry(paths["background"], product_dir),
                "product": relative_entry(paths["product"], product_dir),
                "shadow": relative_entry(paths["shadow"], product_dir),
                "scene": relative_entry(paths["scene"], product_dir),
                "final": relative_entry(paths["final"], product_dir),
            },
            "information": information,
            "scene_composite": scene_render,
            "scene_attempt": attempt_info,
        }
        write_json_new(paths["manifest"], manifest)
        if ensure_output_allowed(product_dir) != output_before:
            raise ValueError("PREVIEW_MODIFIED_OUTPUT_DIRECTORY")
    except Exception:
        cleanup(created)
        raise
    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    print()


def load_preview(product_dir: Path, candidate_id: str) -> tuple[dict, dict[str, Path]]:
    paths = preview_paths(product_dir, candidate_id)
    manifest = read_json(paths["manifest"])
    if (
        manifest.get("kind") != "MASTER_CANDIDATE_PREVIEW"
        or manifest.get("candidate_id") != candidate_id
    ):
        raise ValueError("PREVIEW_MANIFEST_INVALID")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("PREVIEW_MANIFEST_INVALID")
    expected = {
        "layout": product_dir / "reusable" / "layout.json",
        "background": paths["background"],
        "product": paths["product"],
        "shadow": paths["shadow"],
        "scene": paths["scene"],
        "final": paths["final"],
    }
    for label, path in expected.items():
        resolve_entry(files.get(label), product_dir, path, label)
    return manifest, paths


def discard_preview(args: argparse.Namespace) -> None:
    product_dir, _, _ = load_product(args.product_dir)
    candidate_id = safe_component(args.candidate_id, "CANDIDATE_ID")
    current_attempt_info(product_dir, candidate_id)
    paths = preview_paths(product_dir, candidate_id)
    if not any(path.exists() for path in paths.values()):
        raise ValueError("PREVIEW_MISSING")
    cleanup([
        path for label, path in paths.items()
        if label not in {"product", "shadow"}
    ])
    json.dump(
        {"discarded": True, "candidate_id": candidate_id},
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


def create_candidate(args: argparse.Namespace) -> None:
    product_dir, layout_path, layout = load_product(args.product_dir)
    candidate_id = safe_component(args.candidate_id, "CANDIDATE_ID")
    preview, sources = load_preview(product_dir, candidate_id)
    attempt_info = current_attempt_info(product_dir, candidate_id)
    if preview.get("scene_attempt") != attempt_info:
        raise ValueError("PREVIEW_ATTEMPT_MISMATCH")
    information = preview.get("information")
    if not isinstance(information, dict):
        raise ValueError("PREVIEW_INFORMATION_INVALID")
    validate_information_colors(layout, information)
    paths = candidate_paths(product_dir, candidate_id)
    if any(
        path.exists()
        for label, path in paths.items()
        if label not in {"product", "shadow"}
    ):
        raise ValueError("CANDIDATE_ALREADY_EXISTS")
    output_before = ensure_output_allowed(product_dir)
    created = [
        path for label, path in paths.items()
        if label not in {"product", "shadow"}
    ]
    try:
        for label in ("background", "scene", "final"):
            copy_new(sources[label], paths[label])
            if sha256_file(sources[label]) != sha256_file(paths[label]):
                raise ValueError(f"PREVIEW_COPY_HASH_MISMATCH: {label}")
        manifest = {
            "schema": 1,
            "kind": "MASTER_CANDIDATE",
            "candidate_id": candidate_id,
            "files": {
                "layout": relative_entry(layout_path, product_dir),
                "background": relative_entry(paths["background"], product_dir),
                "product": relative_entry(paths["product"], product_dir),
                "shadow": relative_entry(paths["shadow"], product_dir),
                "scene": relative_entry(paths["scene"], product_dir),
                "final": relative_entry(paths["final"], product_dir),
            },
            "information": information,
            "scene_composite": preview.get("scene_composite"),
            "scene_attempt": attempt_info,
        }
        write_json_new(paths["manifest"], manifest)
        if ensure_output_allowed(product_dir) != output_before:
            raise ValueError("CANDIDATE_MODIFIED_OUTPUT_DIRECTORY")
        cleanup([
            path for label, path in sources.items()
            if label not in {"product", "shadow"}
        ])
        accept_scene_attempt(product_dir, "MASTER", candidate_id)
    except Exception:
        cleanup(created)
        raise
    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    print()


def load_candidate(product_dir: Path, candidate_id: str) -> tuple[dict, dict[str, Path]]:
    paths = candidate_paths(product_dir, candidate_id)
    manifest = read_json(paths["manifest"])
    if (
        manifest.get("kind") != "MASTER_CANDIDATE"
        or manifest.get("candidate_id") != candidate_id
    ):
        raise ValueError("CANDIDATE_MANIFEST_INVALID")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("CANDIDATE_MANIFEST_INVALID")
    expected = {
        "layout": product_dir / "reusable" / "layout.json",
        "background": paths["background"],
        "product": paths["product"],
        "shadow": paths["shadow"],
        "scene": paths["scene"],
        "final": paths["final"],
    }
    for label, path in expected.items():
        resolve_entry(files.get(label), product_dir, path, label)
    return manifest, paths


def bind_candidate(args: argparse.Namespace) -> None:
    product_dir, layout_path, layout = load_product(args.product_dir)
    reusable_dir = product_dir / "reusable"
    candidate_id = safe_component(args.candidate_id, "CANDIDATE_ID")
    if ensure_output_allowed(product_dir):
        raise ValueError("BIND_REQUIRES_EMPTY_OUTPUT_DIRECTORY")
    candidate, candidate_files = load_candidate(product_dir, candidate_id)
    targets = {
        "background": reusable_dir / "ORIGINAL_MASTER_BACKGROUND.png",
        "product": reusable_dir / "ORIGINAL_MASTER_PRODUCT.png",
        "shadow": reusable_dir / "ORIGINAL_MASTER_SHADOW.png",
        "scene": reusable_dir / "ORIGINAL_MASTER_SCENE.png",
        "final": product_dir / "output" / "ORIGINAL_MASTER_FINAL.png",
        "manifest": reusable_dir / "master.json",
    }
    if any(path.exists() for path in targets.values()):
        raise ValueError("MASTER_ALREADY_EXISTS")

    created = list(targets.values())
    try:
        for label in ("background", "product", "shadow", "scene", "final"):
            copy_new(candidate_files[label], targets[label])
            if sha256_file(candidate_files[label]) != sha256_file(targets[label]):
                raise ValueError(f"MASTER_COPY_HASH_MISMATCH: {label}")
        information = candidate.get("information")
        if not isinstance(information, dict):
            raise ValueError("CANDIDATE_INFORMATION_INVALID")
        validate_information_colors(layout, information)
        master = {
            "schema": 1,
            "state": "BOUND",
            "source_candidate_id": candidate_id,
            "files": {
                "layout": relative_entry(layout_path, product_dir),
                "background": relative_entry(targets["background"], product_dir),
                "product": relative_entry(targets["product"], product_dir),
                "shadow": relative_entry(targets["shadow"], product_dir),
                "scene": relative_entry(targets["scene"], product_dir),
                "final": relative_entry(targets["final"], product_dir),
            },
            "information": {
                "title_color": information["title_color"],
                "version_color": information["version_color"],
                "logo_type": layout.get("logo_type"),
                "title_line_count": layout.get("title_line_count"),
            },
            "scene_composite": candidate.get("scene_composite"),
        }
        write_json_new(targets["manifest"], master)
        ensure_output_allowed(product_dir)
        close_accepted_master_run(product_dir, candidate_id)
    except Exception:
        cleanup(created)
        raise

    cleanup(list(candidate_files.values()))
    json.dump(master, sys.stdout, ensure_ascii=False, indent=2)
    print()


def verify_master(product_dir: Path) -> dict:
    reusable_dir = product_dir / "reusable"
    manifest_path = reusable_dir / "master.json"
    manifest = read_json(manifest_path)
    if manifest.get("state") != "BOUND":
        raise ValueError("MASTER_NOT_BOUND")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("MASTER_MANIFEST_INVALID")
    expected = {
        "layout": reusable_dir / "layout.json",
        "background": reusable_dir / "ORIGINAL_MASTER_BACKGROUND.png",
        "product": reusable_dir / "ORIGINAL_MASTER_PRODUCT.png",
        "shadow": reusable_dir / "ORIGINAL_MASTER_SHADOW.png",
        "scene": reusable_dir / "ORIGINAL_MASTER_SCENE.png",
        "final": product_dir / "output" / "ORIGINAL_MASTER_FINAL.png",
    }
    for label, path in expected.items():
        resolve_entry(files.get(label), product_dir, path, label)
    return manifest


def sku_preview_paths(product_dir: Path, sku_label: str) -> dict[str, Path]:
    reusable_dir = product_dir / "reusable"
    prefix = f"{sku_label}-preview"
    return {
        "background": product_dir / f"{prefix}-background.png",
        "product": reusable_dir / f"{sku_label}-product.png",
        "shadow": reusable_dir / f"{sku_label}-shadow.png",
        "layers": reusable_dir / f"{sku_label}-layers.json",
        "scene": product_dir / f"{prefix}-scene.png",
        "final": product_dir / f"{prefix}.png",
        "manifest": product_dir / f"{prefix}.json",
    }


def pending_sku(product_dir: Path) -> tuple[str, dict]:
    state = read_json(scene_attempt_path(product_dir))
    run_id = state.get("active_run_id")
    runs = state.get("runs")
    if not run_id or not isinstance(runs, list):
        raise ValueError("ATTEMPT_STATE_INVALID")
    run = next(
        (item for item in runs if isinstance(item, dict) and item.get("run_id") == run_id),
        None,
    )
    if not isinstance(run, dict) or run.get("mode") != "SKU":
        raise ValueError("ACTIVE_SKU_RUN_MISSING")
    sku_label = safe_component(run.get("target", ""), "SKU_LABEL")
    if not re.fullmatch(r"SKU_VARIANT-[A-Z]+", sku_label):
        raise ValueError("SKU_LABEL_INVALID")
    _, pending_info = scene_attempt(product_dir, "SKU", sku_label)
    return sku_label, pending_info


def create_sku_preview(args: argparse.Namespace) -> None:
    product_dir, layout_path, layout = load_product(args.product_dir)
    ensure_output_allowed(product_dir)
    verify_master(product_dir)
    master_manifest_hash = sha256_file(product_dir / "reusable" / "master.json")
    sku_label, pending_info = pending_sku(product_dir)
    pending_run = pending_info["run"]
    pending_attempt = pending_info["attempt"]
    attempt_info = {
        "run_id": pending_run["run_id"],
        "attempt": int(pending_attempt["attempt"]),
        "prompt_path": str(pending_attempt.get("prompt_path", "")),
        "prompt_sha256": str(pending_attempt.get("prompt_sha256", "")),
    }

    paths = sku_preview_paths(product_dir, sku_label)
    if any(
        path.exists() for label, path in paths.items()
        if label not in {"product", "shadow", "layers"}
    ):
        raise ValueError("SKU_PREVIEW_ALREADY_EXISTS")
    product_source = Path(args.product).expanduser().resolve()
    product_hash = sha256_file(product_source)
    layers_exist = paths["product"].exists() and paths["shadow"].exists()
    if layers_exist:
        layers = read_json(paths["layers"])
        if layers.get("source_sha256") != product_hash:
            raise ValueError("CACHED_PRODUCT_SOURCE_MISMATCH")
    elif any(paths[label].exists() for label in ("product", "shadow", "layers")):
        raise ValueError("CACHED_PRODUCT_SHADOW_INCOMPLETE")
    created = [paths[label] for label in ("background", "scene", "final", "manifest")]
    if not layers_exist:
        created.extend(paths[label] for label in ("product", "shadow", "layers"))
    try:
        copy_new(args.generated_background, paths["background"])
        scene_render = scene_composite_info(run_scene_compose(
            paths["background"], product_source, paths["scene"],
            paths["product"], paths["shadow"],
        ))
        if not layers_exist:
            write_json_new(paths["layers"], {"source_sha256": product_hash})
        render = run_compose(
            paths["scene"], layout_path, paths["final"], "SKU_PREVIEW",
        )
        run_validate(paths["final"], "SKU_PREVIEW")
        ensure_output_allowed(product_dir)
        verify_master(product_dir)
        if sha256_file(product_dir / "reusable" / "master.json") != master_manifest_hash:
            raise ValueError("MASTER_MANIFEST_CHANGED")
        information = {
            "title_color": render.get("title_color"),
            "version_color": render.get("version_color"),
        }
        validate_information_colors(layout, information)
        manifest = {
            "kind": "SKU_PREVIEW",
            "sku_label": sku_label,
            "files": {
                label: relative_entry(paths[label], product_dir)
                for label in ("background", "product", "shadow", "scene", "final")
            },
            "information": information,
            "scene_composite": scene_render,
            "scene_attempt": attempt_info,
            "master_verified": True,
        }
        write_json_new(paths["manifest"], manifest)
    except Exception:
        cleanup(created)
        raise
    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    print()


def confirm_sku(args: argparse.Namespace) -> None:
    product_dir, _, _ = load_product(args.product_dir)
    sku_label, _ = pending_sku(product_dir)
    paths = sku_preview_paths(product_dir, sku_label)
    manifest = read_json(paths["manifest"])
    if manifest.get("kind") != "SKU_PREVIEW" or manifest.get("sku_label") != sku_label:
        raise ValueError("SKU_PREVIEW_MANIFEST_INVALID")
    final = product_dir / "output" / f"{sku_label}.png"
    copy_new(paths["final"], final)
    try:
        run_validate(final, "FINAL")
        accept_scene_attempt(product_dir, "SKU", sku_label)
        manifest["kind"] = "SKU_VARIANT"
        manifest["files"]["final"] = relative_entry(final, product_dir)
        write_json_replace(paths["manifest"], manifest)
    except Exception:
        cleanup([final])
        raise
    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    print()


def discard_sku_preview(args: argparse.Namespace) -> None:
    product_dir, _, _ = load_product(args.product_dir)
    sku_label, _ = pending_sku(product_dir)
    paths = sku_preview_paths(product_dir, sku_label)
    if not paths["manifest"].is_file():
        raise ValueError("SKU_PREVIEW_MISSING")
    cleanup([paths[label] for label in ("background", "scene", "final", "manifest")])
    json.dump({"discarded": True, "sku_label": sku_label}, sys.stdout)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview = subparsers.add_parser("preview")
    preview.add_argument("--generated-background", required=True)
    preview.add_argument("--product", required=True)
    preview.add_argument("--product-dir", required=True)
    preview.add_argument("--candidate-id", required=True)
    preview.set_defaults(handler=create_preview)

    discard = subparsers.add_parser("discard-preview")
    discard.add_argument("--product-dir", required=True)
    discard.add_argument("--candidate-id", required=True)
    discard.set_defaults(handler=discard_preview)

    candidate = subparsers.add_parser("candidate")
    candidate.add_argument("--product-dir", required=True)
    candidate.add_argument("--candidate-id", required=True)
    candidate.set_defaults(handler=create_candidate)

    bind = subparsers.add_parser("bind")
    bind.add_argument("--product-dir", required=True)
    bind.add_argument("--candidate-id", required=True)
    bind.set_defaults(handler=bind_candidate)

    sku = subparsers.add_parser("sku-preview")
    sku.add_argument("--generated-background", required=True)
    sku.add_argument("--product", required=True)
    sku.add_argument("--product-dir", required=True)
    sku.set_defaults(handler=create_sku_preview)

    confirm = subparsers.add_parser("confirm-sku")
    confirm.add_argument("--product-dir", required=True)
    confirm.set_defaults(handler=confirm_sku)

    discard_sku = subparsers.add_parser("discard-sku-preview")
    discard_sku.add_argument("--product-dir", required=True)
    discard_sku.set_defaults(handler=discard_sku_preview)

    args = parser.parse_args()
    try:
        args.handler(args)
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
