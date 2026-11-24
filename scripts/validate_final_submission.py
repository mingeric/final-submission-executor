#!/usr/bin/env python3
"""Evidence validator for a final-submission workspace.

Checks that canonical PNG files exist, decode, carry the expected colour mode,
pixel dimensions and DPI metadata, match recorded SHA256 values, and that a task
ledger contains no silent pending work. It validates evidence, not science.

Usage:
  python3 scripts/validate_final_submission.py \
      --workspace /path/to/project \
      --ledger /path/to/TASK_LEDGER.tsv \
      --manifest /path/to/CANONICAL_MANIFEST.tsv

Emits a JSON report on stdout. Exit 0 only when every check passes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import sys
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
VALID_STATUSES = {"PENDING", "DONE", "VERIFIED", "BLOCKED"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def png_info(path: Path) -> dict[str, Any]:
    """Read IHDR and pHYs chunks without loading a plotting library."""
    raw = path.read_bytes()
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG")
    pos = 8
    width = height = color_type = bit_depth = None
    ppm_x = ppm_y = None
    unit = 0
    while pos + 12 <= len(raw):
        length = struct.unpack(">I", raw[pos : pos + 4])[0]
        tag = raw[pos + 4 : pos + 8]
        payload = raw[pos + 8 : pos + 8 + length]
        if len(payload) != length:
            raise ValueError("truncated PNG chunk")
        if tag == b"IHDR" and length >= 13:
            width, height, bit_depth, color_type = struct.unpack(">IIBB", payload[:10])
        elif tag == b"pHYs" and length >= 9:
            ppm_x, ppm_y, unit = struct.unpack(">IIB", payload[:9])
        elif tag == b"IEND":
            break
        pos += 12 + length
    if width is None or height is None:
        raise ValueError("missing IHDR")
    dpi = round(ppm_x / 39.3701) if unit == 1 and ppm_x else None
    return {
        "width_px": width,
        "height_px": height,
        "bit_depth": bit_depth,
        "color_type": color_type,
        "dpi": dpi,
    }


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _as_int(value: str | None) -> int | None:
    try:
        return int(str(value).strip()) if value not in (None, "") else None
    except ValueError:
        return None


def _as_float(value: str | None) -> float | None:
    try:
        return float(str(value).strip()) if value not in (None, "") else None
    except ValueError:
        return None


def validate(workspace: Path, ledger: Path | None, manifest: Path | None,
             dpi_tolerance: int = 10, width_tolerance_mm: float = 0.6) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    if not workspace.is_dir():
        add("workspace", False, f"not a directory: {workspace}")
        return {"ok": False, "workspace": str(workspace), "checks": checks,
                "failures": [c for c in checks if not c["ok"]]}

    add("workspace", True, str(workspace))

    if manifest is None or not manifest.is_file():
        add("manifest", False, "manifest file missing")
    else:
        rows = read_tsv(manifest)
        add("manifest_nonempty", bool(rows), f"{len(rows)} rows")
        if not rows:
            add("manifest_columns", False, "no header/rows")
        else:
            required = set(rows[0].keys())
            add("manifest_columns", "path" in required,
                "columns: " + ",".join(sorted(required)))
            for index, row in enumerate(rows, start=2):
                rel = (row.get("path") or "").strip()
                item = Path(rel)
                if not item.is_absolute():
                    item = workspace / item
                label = f"manifest row {index}: {rel or '<empty>'}"
                if not rel or not item.is_file():
                    add(label, False, "file not found")
                    continue
                try:
                    info = png_info(item)
                except Exception as exc:  # noqa: BLE001 - report all bad bytes
                    add(label, False, f"PNG decode failed: {exc}")
                    continue
                expected_hash = (row.get("sha256") or "").strip().lower()
                actual_hash = sha256(item)
                if expected_hash:
                    add(label + " sha256", expected_hash == actual_hash,
                        f"expected {expected_hash} actual {actual_hash}")
                add(label + " rgb", info["color_type"] == 2,
                    f"PNG colour type {info['color_type']} (2=RGB)")
                expected_dpi = _as_int(row.get("dpi"))
                if expected_dpi is not None:
                    add(label + " dpi",
                        info["dpi"] is not None and abs(info["dpi"] - expected_dpi) <= dpi_tolerance,
                        f"expected {expected_dpi} actual {info['dpi']}")
                expected_w = _as_int(row.get("width_px"))
                expected_h = _as_int(row.get("height_px"))
                if expected_w is not None:
                    add(label + " width_px", info["width_px"] == expected_w,
                        f"expected {expected_w} actual {info['width_px']}")
                if expected_h is not None:
                    add(label + " height_px", info["height_px"] == expected_h,
                        f"expected {expected_h} actual {info['height_px']}")
                expected_wmm = _as_float(row.get("width_mm"))
                if expected_wmm is not None and info["dpi"]:
                    actual_mm = info["width_px"] / info["dpi"] * 25.4
                    add(label + " width_mm", abs(actual_mm - expected_wmm) <= width_tolerance_mm,
                        f"expected {expected_wmm} actual {actual_mm:.3f}")

    if ledger is not None and ledger.is_file():
        rows = read_tsv(ledger)
        add("ledger_nonempty", bool(rows), f"{len(rows)} rows")
        if not rows:
            add("ledger_columns", False, "no header/rows")
        else:
            have = set(rows[0].keys())
            needed = {"task_id", "status", "deliverable", "evidence", "note"}
            add("ledger_columns", needed.issubset(have),
                "columns: " + ",".join(sorted(have)))
            for index, row in enumerate(rows, start=2):
                task = (row.get("task_id") or f"row{index}").strip()
                status = (row.get("status") or "").strip().upper()
                if status not in VALID_STATUSES:
                    add(f"ledger {task}", False, f"invalid status {status!r}")
                    continue
                if status == "PENDING":
                    add(f"ledger {task}", False, "task still pending")
                elif status == "BLOCKED":
                    add(f"ledger {task}", True,
                        "documented blocker: " + (row.get("note") or "")[:160])
                else:
                    evidence = (row.get("evidence") or "").strip()
                    evidence_path = Path(evidence)
                    if not evidence_path.is_absolute():
                        evidence_path = workspace / evidence_path
                    add(f"ledger {task}", bool(evidence) and evidence_path.exists(),
                        f"{status}; evidence {evidence or '<empty>'}")
    else:
        add("ledger", False, "ledger file missing or not provided")

    failures = [check for check in checks if not check["ok"]]
    return {
        "ok": not failures,
        "workspace": str(workspace),
        "checked": len(checks),
        "passed": len(checks) - len(failures),
        "failures": failures,
        "checks": checks,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--dpi-tolerance", type=int, default=10)
    parser.add_argument("--width-tolerance-mm", type=float, default=0.6)
    parser.add_argument("--report", type=Path, help="optional path for the JSON report")
    args = parser.parse_args(argv)
    result = validate(args.workspace.resolve(),
                      args.ledger.resolve() if args.ledger else None,
                      args.manifest.resolve() if args.manifest else None,
                      args.dpi_tolerance, args.width_tolerance_mm)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
