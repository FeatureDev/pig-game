#!/usr/bin/env python3
"""
generate_readme.py
───────────────────
Automatisk generator som uppdaterar README.md med senaste testresultat och coverage-statistik.
Fungerar som bonusverktyg för TDD-projektet "Pig Dice Game".
"""

import subprocess
import re
from datetime import datetime
from pathlib import Path

# ---- Metadata ----
PROJECT_NAME = "🐷 Pig Dice Game"
AUTHOR = "Morgan Lindbom & Yousef Alim"
DESCRIPTION = "A fully tested command-line dice game with AI opponents, cheat mode, and >90% coverage."
LICENSE = "MIT License"
PYTHON_VERSION = "3.13.x"
README_PATH = Path("README.md")

# ---- Hjälpfunktioner ----
def run_tests() -> tuple[str, str]:
    """Kör pytest med coverage och returnerar (coverage_text, summary_line)."""
    print("🧪 Running pytest with coverage...")
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "--cov=src", "--cov-report=term-missing"],
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = result.stdout
        stderr = result.stderr

        # Extrahera total coverage %
        match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", stdout)
        coverage_pct = match.group(1) if match else "N/A"

        summary = f"✅ {coverage_pct}% coverage — {datetime.now():%Y-%m-%d %H:%M:%S}"
        if "FAILED" in stdout or result.returncode != 0:
            summary = f"❌ Tests failed — see output below"

        print(summary)
        return stdout, summary
    except Exception as e:
        return f"⚠️ Error running tests: {e}", "❌ No results"

def update_readme(report: str, summary: str):
    """Uppdaterar README.md med ny coverage-sektion."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    section_header = "## 🧪 Automated Test & Coverage Report"

    new_section = (
        f"\n\n{section_header}\n"
        f"**Generated automatically:** {date_str}\n\n"
        f"**Summary:** {summary}\n\n"
        f"```text\n{report.strip()}\n```\n"
    )

    # Läs in README
    content = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

    # Ersätt befintlig sektion eller lägg till
    if section_header in content:
        print("🔁 Updating existing report section...")
        content = re.sub(
            rf"{section_header}.*?(?=\n# |\Z)",
            new_section.strip(),
            content,
            flags=re.DOTALL,
        )
    else:
        print("➕ Adding new report section...")
        content += new_section

    # Skriv ut resultat
    README_PATH.write_text(content.strip() + "\n", encoding="utf-8")
    print("✅ README.md updated successfully!")

def main():
    print(f"📘 Generating README update for {PROJECT_NAME}")
    print(f"👤 Author: {AUTHOR}")
    print(f"🐍 Python: {PYTHON_VERSION}")
    print("-" * 60)

    report, summary = run_tests()
    update_readme(report, summary)

    print("-" * 60)
    print("📄 README.md now includes the latest coverage summary.")

if __name__ == "__main__":
    main()
