"""Offline unit tests. All generated images are test fixtures, never research data."""
from __future__ import annotations

import shutil
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_skill import validate as validate_skill  # noqa: E402
from scripts.validate_final_submission import sha256, validate  # noqa: E402

SIGNATURE = b"\x89PNG\r\n\x1a\n"


def chunk(tag: bytes, payload: bytes) -> bytes:
    return (struct.pack(">I", len(payload)) + tag + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))


def make_png(path: Path, width: int = 60, height: int = 30,
             dpi: int = 600, color_type: int = 2) -> None:
    """Create a small synthetically generated PNG used only as a test fixture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    channels = 3 if color_type == 2 else 4
    row = bytes([210, 225, 235, 255][:channels]) * width
    raw = (b"\x00" + row) * height
    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    ppm = round(dpi * 39.3701)
    phys = struct.pack(">IIB", ppm, ppm, 1)
    path.write_bytes(SIGNATURE + chunk(b"IHDR", ihdr) + chunk(b"pHYs", phys)
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


class TestPackage(unittest.TestCase):
    def test_skill_structure_passes(self) -> None:
        ok, _, failures = validate_skill(ROOT)
        self.assertTrue(ok, failures)


class TestValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="fse-test-"))
        self.figure = self.tmp / "figures" / "Fig01.png"
        make_png(self.figure)
        self.manifest = self.tmp / "CANONICAL_MANIFEST.tsv"
        self.ledger = self.tmp / "TASK_LEDGER.tsv"
        self._write_manifest(sha256(self.figure))
        self._write_ledger("VERIFIED")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write_manifest(self, digest: str, rel: str = "figures/Fig01.png") -> None:
        self.manifest.write_text(
            "path\tsha256\twidth_px\theight_px\tdpi\tcolor_mode\n"
            f"{rel}\t{digest}\t60\t30\t600\tRGB\n", encoding="utf-8")

    def _write_ledger(self, status: str) -> None:
        evidence = "figures/Fig01.png" if status in ("DONE", "VERIFIED") else ""
        note = "" if status != "BLOCKED" else "named source table unavailable"
        self.ledger.write_text(
            "task_id\tstatus\tdeliverable\tevidence\tnote\n"
            f"F01\t{status}\tfigures/Fig01.png\t{evidence}\t{note}\n", encoding="utf-8")

    def _result(self) -> dict:
        return validate(self.tmp, self.ledger, self.manifest)

    def test_validator_accepts_valid_bundle(self) -> None:
        result = self._result()
        self.assertTrue(result["ok"], result["failures"])
        self.assertGreater(result["passed"], 5)

    def test_validator_rejects_wrong_hash(self) -> None:
        self._write_manifest("0" * 64)
        result = self._result()
        self.assertFalse(result["ok"])
        self.assertTrue(any("sha256" in f["name"] for f in result["failures"]))

    def test_validator_rejects_pending_ledger(self) -> None:
        self._write_ledger("PENDING")
        result = self._result()
        self.assertFalse(result["ok"])
        self.assertTrue(any("pending" in f["detail"] for f in result["failures"]))

    def test_validator_accepts_documented_blocker(self) -> None:
        self._write_ledger("BLOCKED")
        self.assertTrue(self._result()["ok"])

    def test_validator_rejects_rgba(self) -> None:
        make_png(self.figure, color_type=6)
        self._write_manifest(sha256(self.figure))
        result = self._result()
        self.assertFalse(result["ok"])
        self.assertTrue(any("rgb" in f["name"] for f in result["failures"]))

    def test_validator_rejects_missing_file(self) -> None:
        self._write_manifest("0" * 64, rel="figures/Missing.png")
        result = self._result()
        self.assertFalse(result["ok"])

    def test_validator_rejects_missing_manifest(self) -> None:
        result = validate(self.tmp, self.ledger, self.tmp / "absent.tsv")
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
