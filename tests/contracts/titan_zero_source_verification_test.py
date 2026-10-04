from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "titan-zero" / "verify-source.sh"


class TitanZeroSourceVerificationTest(unittest.TestCase):
    def make_fixture(self) -> Path:
        root = Path(tempfile.mkdtemp(prefix="titan-source-verify-"))
        required = [
            "artisan",
            "composer.json",
            "app/Domains/WorkCore/WorkCoreServiceProvider.php",
            "packages/titanzero/interaction-engine/composer.json",
            "packages/titanzero/interaction-engine/src/Providers/InteractionServiceProvider.php",
            "app/Extensions/Chatbot/extension.json",
            "app/Extensions/Chatbot/System/ChatbotServiceProvider.php",
            "docs/archive/plans/2026-07/titan-zero-chatbot-pwa-upgrade-plan.md",
        ]
        for relative in required:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".json":
                path.write_text("{}\n", encoding="utf-8")
            else:
                path.write_text("fixture\n", encoding="utf-8")
        return root

    def run_verifier(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(VERIFY_SCRIPT)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_json_with_utf8_bom_is_accepted(self) -> None:
        root = self.make_fixture()
        self.addCleanup(shutil.rmtree, root, True)
        manifest = root / "app/Extensions/Legacy/extension.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_bytes(b"\xef\xbb\xbf" + b'{"name":"Legacy"}\n')

        result = self.run_verifier(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Strict JSON validation: PASS", result.stdout)

    def test_malformed_json_is_rejected(self) -> None:
        root = self.make_fixture()
        self.addCleanup(shutil.rmtree, root, True)
        manifest = root / "app/Extensions/Broken/extension.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text('{"name":', encoding="utf-8")

        result = self.run_verifier(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid strict JSON", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
