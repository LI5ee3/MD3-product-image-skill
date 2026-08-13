"""Shared file helpers for the MD3 workflow."""

import hashlib
import json
from pathlib import Path


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
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"JSON_UNREADABLE: {path}: {exc}") from exc


def atomic_write(path: Path, data, *, new: bool = False) -> None:
    if new and path.exists():
        raise ValueError(f"REFUSE_OVERWRITE: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        temporary.write_text(
            data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def verify_information_assets(layout: dict, reusable_dir: Path) -> None:
    try:
        elements = layout["elements"]
        assets = layout["information_assets"]
        expected = {"logo": elements["LOGO_RECT"]["asset"]}
        expected.update(
            (f"title_{index}", title["asset"])
            for index, title in enumerate(elements["TITLE_LINE_RECT"], 1)
        )
        if "VERSION_TEXT_RECT" in elements:
            expected["version"] = elements["VERSION_TEXT_RECT"]["asset"]
    except (KeyError, TypeError) as exc:
        raise ValueError("INFORMATION_ASSETS_INVALID") from exc
    if set(assets) != set(expected):
        raise ValueError("INFORMATION_ASSET_SET_MISMATCH")
    for label, name in expected.items():
        try:
            entry = assets[label]
            path = (reusable_dir / entry["path"]).resolve()
        except (KeyError, TypeError) as exc:
            raise ValueError(f"INFORMATION_ASSET_INVALID: {label}") from exc
        if path != (reusable_dir / name).resolve() or not path.is_file():
            raise ValueError(f"INFORMATION_ASSET_PATH_MISMATCH: {label}")
        if sha256_file(path) != entry.get("sha256"):
            raise ValueError(f"INFORMATION_ASSET_HASH_MISMATCH: {label}")


def resolve_entry(entry: dict, product_dir: Path, expected: Path, label: str) -> Path:
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


def verify_master(product_dir: Path) -> dict:
    reusable = product_dir / "reusable"
    manifest = read_json(reusable / "master.json")
    if manifest.get("state") != "BOUND" or not isinstance(manifest.get("files"), dict):
        raise ValueError("MASTER_NOT_BOUND")
    expected = {
        "layout": reusable / "layout.json",
        "background": reusable / "ORIGINAL_MASTER_BACKGROUND.png",
        "product": reusable / "ORIGINAL_MASTER_PRODUCT.png",
        "shadow": reusable / "ORIGINAL_MASTER_SHADOW.png",
        "scene": reusable / "ORIGINAL_MASTER_SCENE.png",
        "final": product_dir / "output" / "ORIGINAL_MASTER_FINAL.png",
    }
    for label, path in expected.items():
        resolve_entry(manifest["files"].get(label), product_dir, path, label)
    return manifest
