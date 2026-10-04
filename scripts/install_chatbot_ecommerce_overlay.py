#!/usr/bin/env python3
"""Install only the verified ChatbotEcommerce v4.9.0 overlay."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.request
import zipfile

ALLOWED_PREFIX = PurePosixPath("extensions/ChatbotEcommerce")
ALLOWED_TARGET = PurePosixPath("app/Extensions/ChatbotEcommerce")
EXPECTED_VERSION = "4.9.0"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--receipt")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if PurePosixPath(manifest["source_prefix"]) != ALLOWED_PREFIX:
        raise ValueError("Unexpected overlay source prefix")
    if PurePosixPath(manifest["target_directory"]) != ALLOWED_TARGET:
        raise ValueError("Unexpected overlay target directory")
    if manifest["extension_version"] != EXPECTED_VERSION:
        raise ValueError("Unexpected extension version")

    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit("Install pyarrow before running this installer") from exc

    with tempfile.TemporaryDirectory(prefix="chatbot-ecommerce-overlay-") as temp:
        parquet = Path(temp) / "overlay.parquet"
        archive = Path(temp) / "overlay.zip"
        request = urllib.request.Request(
            manifest["url"],
            headers={"User-Agent": "titan-zero-ecommerce-installer/1.0"},
        )
        with urllib.request.urlopen(request, timeout=300) as source, parquet.open("wb") as output:
            shutil.copyfileobj(source, output)

        table = pq.read_table(
            parquet,
            columns=["Sequence", "Payload_Base64", "Archive_Sha256", "Archive_Bytes"],
        )
        rows = sorted(
            zip(
                table.column("Sequence").to_pylist(),
                table.column("Payload_Base64").to_pylist(),
                table.column("Archive_Sha256").to_pylist(),
                table.column("Archive_Bytes").to_pylist(),
            ),
            key=lambda row: int(row[0]),
        )
        if [int(row[0]) for row in rows] != list(range(len(rows))):
            raise ValueError("Overlay chunks are missing or out of order")
        if {str(row[2]) for row in rows} != {manifest["archive_sha256"]}:
            raise ValueError("Overlay chunk SHA metadata mismatch")
        if {int(row[3]) for row in rows} != {int(manifest["archive_bytes"])}:
            raise ValueError("Overlay chunk size metadata mismatch")

        with archive.open("wb") as output:
            for _, payload, _, _ in rows:
                output.write(base64.b64decode(str(payload), validate=True))
        if archive.stat().st_size != int(manifest["archive_bytes"]):
            raise ValueError("Overlay archive size mismatch")
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        if digest != manifest["archive_sha256"]:
            raise ValueError("Overlay archive SHA-256 mismatch")

        target = root.joinpath(*ALLOWED_TARGET.parts)
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)

        extracted = 0
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.infolist():
                path = PurePosixPath(member.filename)
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError(f"Unsafe overlay path: {member.filename}")
                if tuple(path.parts[:2]) != tuple(ALLOWED_PREFIX.parts):
                    raise ValueError(f"Unexpected overlay path: {member.filename}")
                suffix = path.parts[2:]
                if not suffix:
                    continue
                destination = target.joinpath(*suffix)
                if member.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                with bundle.open(member) as source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
                extracted += 1

    if extracted != int(manifest["extracted_files"]):
        raise ValueError(f"Expected {manifest['extracted_files']} files, extracted {extracted}")
    installed = json.loads((target / "extension.json").read_text(encoding="utf-8-sig"))
    if installed.get("version") != EXPECTED_VERSION:
        raise ValueError("Installed extension version mismatch")

    receipt = {
        "version": EXPECTED_VERSION,
        "files": extracted,
        "archive_sha256": digest,
        "target": str(ALLOWED_TARGET),
    }
    if args.receipt:
        receipt_path = root / args.receipt
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
