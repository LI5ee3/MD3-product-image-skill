#!/usr/bin/env python3
"""Build prompts and record bounded scene or uncounted delivery failures."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
IMAGE_PROMPT_REFERENCE = SKILL_DIR / "references" / "image-gen-prompt.txt"
VARIANT_REFERENCE = SKILL_DIR / "references" / "replace-variant-block.md"
MAX_ATTEMPTS = 3
ATTEMPT_STATE_NAME = "scene-attempts.json"
SKU_TARGET_PATTERN = re.compile(r"SKU_VARIANT-([A-Z]+)")
FINAL_SAFE_ZONE_MARGIN = 0.05
PRODUCT_AREA_POLICY = """Product and shadow placement policy:
FINAL_INFORMATION_SAFE_ZONE is the only area that must be empty.
Do not create or interpret any product or shadow area as another empty or unobstructed safe zone, including any previous temporary correction that requested one.
Simple, low-detail MD3 cards and their restrained elevation shadows may appear behind the future local product and may receive its local cast shadow.
Avoid only dominant high-contrast edges or dense detail that visibly competes with the product after local compositing."""


def read_json(path: Path):
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"JSON_UNREADABLE: {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ValueError(f"FILE_UNREADABLE: {path}: {exc}") from exc
    return digest.hexdigest()


def fenced_block(path: Path, heading: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"REFERENCE_UNREADABLE: {path}: {exc}") from exc
    match = re.search(
        rf"^#{{1,6}} {re.escape(heading)}\s*$.*?^```text\s*$\n(.*?)^```\s*$",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"REFERENCE_BLOCK_MISSING: {heading}")
    return match.group(1).rstrip()


def image_prompt() -> str:
    try:
        prompt = IMAGE_PROMPT_REFERENCE.read_text(encoding="utf-8").rstrip("\n")
    except OSError as exc:
        raise ValueError(
            f"REFERENCE_UNREADABLE: {IMAGE_PROMPT_REFERENCE}: {exc}"
        ) from exc
    if not prompt:
        raise ValueError("IMAGE_PROMPT_EMPTY")
    return prompt


def information_safe_zone_block(layout: dict) -> str:
    zones = layout.get("clear_zones")
    selected = [
        zone
        for zone in zones or []
        if zone.get("label") == "LOGO_RECT"
        or str(zone.get("label", "")).startswith("TITLE_LINE_RECT_")
        or zone.get("label") == "VERSION_TEXT_RECT"
    ]
    if not selected:
        raise ValueError("INFORMATION_SAFE_ZONES_MISSING")

    bounds = []
    for zone in selected:
        try:
            x0 = float(zone["x"])
            y0 = float(zone["y"])
            x1 = x0 + float(zone["w"])
            y1 = y0 + float(zone["h"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("INFORMATION_SAFE_ZONE_INVALID") from exc
        if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            raise ValueError("INFORMATION_SAFE_ZONE_OUT_OF_CANVAS")
        bounds.append((x0, y0, x1, y1))

    x0 = max(0, min(bound[0] for bound in bounds) - FINAL_SAFE_ZONE_MARGIN)
    y0 = max(0, min(bound[1] for bound in bounds) - FINAL_SAFE_ZONE_MARGIN)
    x1 = min(1, max(bound[2] for bound in bounds) + FINAL_SAFE_ZONE_MARGIN)
    y1 = min(1, max(bound[3] for bound in bounds) + FINAL_SAFE_ZONE_MARGIN)
    return "\n".join(
        (
            "Layout-only final information safe zone:",
            'Interpret any earlier "top-left negative space" instruction only as this one merged rectangle.',
            "This rectangle merges the measured Logo, title-line, and optional version safe zones, then expands the union by 5.0% of the canvas on every side, clipped to the canvas:",
            f"- FINAL_INFORMATION_SAFE_ZONE: x {x0 * 100:.1f}%-{x1 * 100:.1f}%, y {y0 * 100:.1f}%-{y1 * 100:.1f}%",
            "Keep the entire rectangle clear, calm, smooth, and empty, free of card edges, strong shadows, texture changes, or detailed geometry.",
        )
    )


def verify_information_assets(layout: dict, product_dir: Path) -> None:
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
            path = (product_dir / entry["path"]).resolve()
            expected_hash = entry["sha256"]
            expected_path = (product_dir / asset_name).resolve()
        except (KeyError, TypeError) as exc:
            raise ValueError(f"INFORMATION_ASSET_INVALID: {label}") from exc
        if path != expected_path or path.parent != product_dir:
            raise ValueError(f"INFORMATION_ASSET_PATH_MISMATCH: {label}")
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise ValueError(f"INFORMATION_ASSET_HASH_MISMATCH: {label}")


def load_layout(path: Path) -> tuple[dict, Path]:
    layout_path = path.expanduser().resolve()
    if layout_path.name != "layout.json":
        raise ValueError("LAYOUT_PATH_INVALID")
    layout = read_json(layout_path)
    product_dir = layout_path.parent
    if layout.get("product_directory") != str(product_dir):
        raise ValueError("PRODUCT_DIRECTORY_MISMATCH")
    verify_information_assets(layout, product_dir)
    zones = layout.get("clear_zones")
    if not isinstance(zones, list) or not zones:
        raise ValueError("CLEAR_ZONES_MISSING")
    return layout, product_dir


def failures_from(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = read_json(path)
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and isinstance(data.get("failures"), list):
        entries = data["failures"]
    else:
        raise ValueError("FAILURE_LOG_INVALID")
    if not all(isinstance(entry, dict) for entry in entries):
        raise ValueError("FAILURE_LOG_ENTRY_INVALID")
    return entries


def failure_increment(entries: list[dict]) -> str | None:
    lines = ["Temporary corrections accumulated for this product:"]
    number = 0
    for entry in entries:
        checks = entry.get("checks")
        if not isinstance(checks, list):
            raise ValueError("FAILURE_LOG_ENTRY_INVALID")
        for check in checks:
            if not isinstance(check, dict):
                raise ValueError("FAILURE_LOG_ENTRY_INVALID")
            failed = str(check.get("failed_check", "")).strip()
            correction = str(check.get("correction", "")).strip()
            if not failed or not correction:
                raise ValueError("FAILURE_LOG_ENTRY_INVALID")
            number += 1
            lines.extend(
                (
                    f"{number}. Previous failed check: {failed}",
                    f"   Required correction: {correction}",
                )
            )
    return "\n".join(lines) if number else None


def attempt_state_path(product_dir: Path) -> Path:
    return product_dir / ATTEMPT_STATE_NAME


def new_attempt_state() -> dict:
    return {"schema": 1, "next_run": 1, "active_run_id": None, "runs": []}


def load_attempt_state(product_dir: Path) -> dict:
    path = attempt_state_path(product_dir)
    if not path.exists():
        return new_attempt_state()
    state = read_json(path)
    if (
        not isinstance(state, dict)
        or state.get("schema") != 1
        or not isinstance(state.get("runs"), list)
    ):
        raise ValueError("ATTEMPT_STATE_INVALID")
    return state


def active_run(state: dict) -> dict | None:
    run_id = state.get("active_run_id")
    if run_id is None:
        return None
    for run in state["runs"]:
        if isinstance(run, dict) and run.get("run_id") == run_id:
            return run
    raise ValueError("ACTIVE_ATTEMPT_RUN_MISSING")


def start_run(state: dict, mode: str, target: str) -> dict:
    run_number = int(state.get("next_run", len(state["runs"]) + 1))
    run = {
        "run_id": f"{mode}-RUN-{run_number}",
        "mode": mode,
        "target": target,
        "status": "ACTIVE",
        "attempts": [],
    }
    state["runs"].append(run)
    state["next_run"] = run_number + 1
    state["active_run_id"] = run["run_id"]
    return run


def scene_attempts_used(attempts: list[dict]) -> int:
    return sum(
        attempt.get("status") != "DELIVERY_FAILED" for attempt in attempts
    )


def prepare_run(
    state: dict, mode: str, target: str, new_candidate: bool
) -> dict:
    run = active_run(state)
    if new_candidate:
        if run and run.get("status") == "ACTIVE":
            run["status"] = "ABANDONED"
        return start_run(state, mode, target)
    if run is None:
        return start_run(state, mode, target)
    if run.get("mode") != mode or run.get("target") != target:
        raise ValueError(
            "NEW_CANDIDATE_REQUIRED: active scene is "
            f"{run.get('mode')}/{run.get('target')}"
        )
    attempts = run.get("attempts")
    if not isinstance(attempts, list):
        raise ValueError("ATTEMPT_STATE_INVALID")
    if scene_attempts_used(attempts) >= MAX_ATTEMPTS:
        raise ValueError(f"ATTEMPT_LIMIT_REACHED: {mode}/{target}")
    if run.get("status") != "ACTIVE":
        raise ValueError("NEW_CANDIDATE_REQUIRED: active scene is closed")
    if attempts and attempts[-1].get("status") == "PENDING":
        raise ValueError("FAILURE_RECORD_REQUIRED: record the last scene failure first")
    return run


def prompt_file_path(
    product_dir: Path, mode: str, target: str, run: dict, attempt: int
) -> Path:
    target_hash = hashlib.sha256(target.encode("utf-8")).hexdigest()[:10]
    return product_dir / (
        f"scene-prompt-{mode.lower()}-{target_hash}-"
        f"run-{run['run_id'].rsplit('-', 1)[-1]}-attempt-{attempt}.txt"
    )


def verify_master(manifest_path: Path, layout_path: Path) -> None:
    manifest_path = manifest_path.expanduser().resolve()
    product_dir = layout_path.parent
    if manifest_path != product_dir / "master.json":
        raise ValueError("MASTER_MANIFEST_PATH_INVALID")
    manifest = read_json(manifest_path)
    if manifest.get("state") != "BOUND":
        raise ValueError("MASTER_NOT_BOUND")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("MASTER_MANIFEST_INVALID")
    expected_paths = {
        "layout": layout_path,
        "background": product_dir / "ORIGINAL_MASTER_BACKGROUND.png",
        "product": product_dir / "ORIGINAL_MASTER_PRODUCT.png",
        "shadow": product_dir / "ORIGINAL_MASTER_SHADOW.png",
        "scene": product_dir / "ORIGINAL_MASTER_SCENE.png",
        "final": product_dir / "output" / "ORIGINAL_MASTER_FINAL.png",
        "thumbnail": product_dir / "ORIGINAL_MASTER_FINAL-thumb.png",
    }
    for key, expected_path in expected_paths.items():
        try:
            relative = Path(files[key]["path"])
            expected_hash = files[key]["sha256"]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"MASTER_MANIFEST_INVALID: {key}") from exc
        resolved = (product_dir / relative).resolve()
        if resolved != product_dir and product_dir not in resolved.parents:
            raise ValueError(f"MASTER_PATH_OUTSIDE_PRODUCT_DIRECTORY: {key}")
        if resolved != expected_path:
            raise ValueError(f"MASTER_PATH_MISMATCH: {key}")
        if not resolved.is_file() or sha256_file(resolved) != expected_hash:
            raise ValueError(f"MASTER_HASH_MISMATCH: {key}")


def validate_target(value: str) -> str:
    value = value.strip()
    if not value or value in {".", ".."} or any(char in value for char in "/\\\x00"):
        raise ValueError("TARGET_INVALID")
    return value


def sku_letters(number: int) -> str:
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def next_sku_target(product_dir: Path) -> str:
    existing = {
        match.group(1)
        for path in (product_dir / "output").glob("SKU_VARIANT-*.png")
        if (match := SKU_TARGET_PATTERN.fullmatch(path.stem))
    }
    number = 1
    while sku_letters(number) in existing:
        number += 1
    return f"SKU_VARIANT-{sku_letters(number)}"


def resolve_target(args: argparse.Namespace, state: dict) -> str:
    if args.mode == "MASTER":
        if not args.target:
            raise ValueError("TARGET_REQUIRED")
        return validate_target(args.target)
    if args.target:
        raise ValueError("SKU_TARGET_IS_AUTOMATIC")
    run = active_run(state)
    if run and run.get("mode") == "SKU" and run.get("status") == "ACTIVE":
        return validate_target(run.get("target", ""))
    return next_sku_target(Path(args.layout).expanduser().resolve().parent)


def resolve_active_target(args: argparse.Namespace, state: dict) -> str:
    if args.mode == "MASTER":
        if not args.target:
            raise ValueError("TARGET_REQUIRED")
        return validate_target(args.target)
    if args.target:
        raise ValueError("SKU_TARGET_IS_AUTOMATIC")
    run = active_run(state)
    if not run or run.get("mode") != "SKU":
        raise ValueError("ACTIVE_SKU_RUN_MISSING")
    return validate_target(run.get("target", ""))


def build_prompt(args: argparse.Namespace) -> None:
    layout, product_dir = load_layout(Path(args.layout))
    state = load_attempt_state(product_dir)
    target = resolve_target(args, state)

    if args.mode == "SKU":
        if not args.master:
            raise ValueError("MASTER_MANIFEST_REQUIRED")
        verify_master(Path(args.master), Path(args.layout).expanduser().resolve())
    elif args.master:
        raise ValueError("MASTER_MANIFEST_NOT_ALLOWED_FOR_MASTER_PROMPT")

    run = prepare_run(state, args.mode, target, args.new_candidate)
    attempts = run["attempts"]
    attempt_number = len(attempts) + 1
    parts = [image_prompt(), information_safe_zone_block(layout)]
    if args.mode == "SKU":
        parts.append(fenced_block(VARIANT_REFERENCE, "SKU edit block"))
    increment = failure_increment(failures_from(product_dir / "scene-failures.json"))
    if increment:
        parts.append(increment)
    parts.append(PRODUCT_AREA_POLICY)
    prompt = "\n\n".join(parts)
    prompt_path = prompt_file_path(product_dir, args.mode, target, run, attempt_number)
    attempts.append(
        {
            "attempt": attempt_number,
            "status": "PENDING",
            "prompt_path": prompt_path.name,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        }
    )
    atomic_write_text(prompt_path, prompt)
    atomic_write(attempt_state_path(product_dir), state)
    sys.stdout.write(prompt)


def atomic_write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary_created = False
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            temporary_created = True
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temporary.replace(path)
    except Exception:
        if temporary_created and temporary.exists():
            temporary.unlink()
        raise


def atomic_write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary_created = False
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            temporary_created = True
            handle.write(data)
        temporary.replace(path)
    except Exception:
        if temporary_created and temporary.exists():
            temporary.unlink()
        raise


def record_failure(args: argparse.Namespace) -> None:
    log_path = Path(args.log).expanduser().resolve()
    if log_path.name != "scene-failures.json":
        raise ValueError("FAILURE_LOG_FILENAME_INVALID")
    _, product_dir = load_layout(log_path.parent / "layout.json")
    if log_path != product_dir / "scene-failures.json":
        raise ValueError("FAILURE_LOG_PATH_INVALID")
    failed_checks = [value.strip() for value in args.failed_check]
    corrections = [value.strip() for value in args.correction]
    if len(failed_checks) != len(corrections) or not failed_checks:
        raise ValueError("FAILURE_CORRECTION_COUNT_MISMATCH")
    if not all(failed_checks) or not all(corrections):
        raise ValueError("FAILURE_CORRECTION_EMPTY")

    entries = failures_from(log_path)
    state = load_attempt_state(product_dir)
    target = resolve_active_target(args, state)
    run = active_run(state)
    if run is None:
        raise ValueError("FAILURE_RECORD_WITHOUT_SCENE_ATTEMPT")
    if run.get("mode") != args.mode or run.get("target") != target:
        raise ValueError(
            "NEW_CANDIDATE_REQUIRED: active scene is "
            f"{run.get('mode')}/{run.get('target')}"
        )
    attempts = run.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        raise ValueError("FAILURE_RECORD_WITHOUT_SCENE_ATTEMPT")
    if scene_attempts_used(attempts) > MAX_ATTEMPTS:
        raise ValueError(f"ATTEMPT_LIMIT_REACHED: {args.mode}/{target}")
    current = attempts[-1]
    if current.get("status") != "PENDING":
        raise ValueError("FAILURE_ALREADY_RECORDED: build the next scene first")
    attempt = int(current["attempt"])
    record = {
        "mode": args.mode,
        "target": target,
        "run_id": run["run_id"],
        "attempt": attempt,
        "checks": [
            {"failed_check": failed, "correction": correction}
            for failed, correction in zip(failed_checks, corrections)
        ],
    }
    entries.append(record)
    current["status"] = "FAILED"
    current["checks"] = record["checks"]
    attempts_used = scene_attempts_used(attempts)
    atomic_write(attempt_state_path(product_dir), state)
    atomic_write(log_path, entries)
    json.dump(
        {
            "recorded": record,
            "retry_allowed": attempts_used < MAX_ATTEMPTS,
            "attempts_used": attempts_used,
            "attempts_max": MAX_ATTEMPTS,
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


def record_delivery_failure(args: argparse.Namespace) -> None:
    _, product_dir = load_layout(Path(args.layout))
    reason = args.reason.strip()
    if not reason:
        raise ValueError("DELIVERY_FAILURE_REASON_EMPTY")
    state = load_attempt_state(product_dir)
    target = resolve_active_target(args, state)
    run = active_run(state)
    if run is None or run.get("mode") != args.mode or run.get("target") != target:
        raise ValueError("DELIVERY_FAILURE_RUN_MISMATCH")
    attempts = run.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        raise ValueError("DELIVERY_FAILURE_WITHOUT_ATTEMPT")
    current = attempts[-1]
    if current.get("status") != "PENDING":
        raise ValueError("DELIVERY_FAILURE_ALREADY_RECORDED")
    current["status"] = "DELIVERY_FAILED"
    current["reason"] = reason
    atomic_write(attempt_state_path(product_dir), state)
    json.dump(
        {
            "recorded": {
                "mode": args.mode,
                "target": target,
                "run_id": run["run_id"],
                "attempt": int(current["attempt"]),
                "status": "DELIVERY_FAILED",
                "reason": reason,
            },
            "retry_allowed": True,
            "attempts_used": scene_attempts_used(attempts),
            "attempts_max": MAX_ATTEMPTS,
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("--mode", required=True, choices=("MASTER", "SKU"))
    build.add_argument("--layout", required=True)
    build.add_argument("--target")
    build.add_argument("--master")
    build.add_argument(
        "--new-candidate",
        action="store_true",
        help="start an explicitly requested independent candidate run",
    )
    build.set_defaults(handler=build_prompt)

    record = subparsers.add_parser("record-failure")
    record.add_argument("--log", required=True)
    record.add_argument("--mode", required=True, choices=("MASTER", "SKU"))
    record.add_argument("--target")
    record.add_argument("--failed-check", action="append", required=True)
    record.add_argument("--correction", action="append", required=True)
    record.set_defaults(handler=record_failure)

    delivery = subparsers.add_parser("record-delivery-failure")
    delivery.add_argument("--layout", required=True)
    delivery.add_argument("--mode", required=True, choices=("MASTER", "SKU"))
    delivery.add_argument("--target")
    delivery.add_argument("--reason", required=True)
    delivery.set_defaults(handler=record_delivery_failure)

    args = parser.parse_args()
    try:
        args.handler(args)
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
