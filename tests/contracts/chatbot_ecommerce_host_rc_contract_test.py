#!/usr/bin/env python3
"""Static host contract for the ChatbotEcommerce v4.9.0 release-candidate gate."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTENSION = ROOT / "app" / "Extensions" / "ChatbotEcommerce"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    manifest_path = EXTENSION / "extension.json"
    require(manifest_path.is_file(), "ChatbotEcommerce extension.json is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    require(manifest.get("version") == "4.9.0", "Host must install ChatbotEcommerce v4.9.0")

    feature_flags = (ROOT / "app" / "Support" / "TitanZero" / "TitanZeroFeatureFlags.php").read_text(
        encoding="utf-8"
    )
    require("ExtensionServiceProvider" in feature_flags, "Extension discovery flag must register ExtensionServiceProvider")
    require(
        "if ($this->extensionDiscoveryEnabled)" in feature_flags,
        "ExtensionServiceProvider must remain behind explicit feature enablement",
    )

    titan_config = (ROOT / "config" / "titan-zero.php").read_text(encoding="utf-8")
    require("'extensions'" in titan_config, "config/titan-zero.php must expose extensions configuration")
    require("TITAN_ZERO_EXTENSIONS_ENABLED" in titan_config, "enabled extensions must be configurable by environment")

    migrations = sorted((EXTENSION / "database" / "migrations").glob("*.php"))
    require(len(migrations) >= 21, f"Expected at least 21 ecommerce migrations, found {len(migrations)}")

    scripts = sorted((EXTENSION / "tests").glob("run_*.php"))
    require(len(scripts) == 38, f"Expected 38 packaged regression scripts, found {len(scripts)}")

    provider = EXTENSION / "System" / "ChatbotEcommerceServiceProvider.php"
    require(provider.is_file(), "ChatbotEcommerce service provider is missing")
    provider_text = provider.read_text(encoding="utf-8")
    require("loadMigrationsFrom" in provider_text, "Extension provider must register its migrations")
    require("CommerceScheduleRegistrar" in provider_text, "Extension provider must register its scheduler")

    print("ChatbotEcommerce host RC static contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
