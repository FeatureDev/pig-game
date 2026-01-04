# ============================================================
# Pig Game — Makefile
# Robust, portable, and academically correct environment
# ============================================================

SHELL := bash

# ============================================================
# Dynamic Python detection (Windows/Linux)
# ============================================================
PYTHON := .venv/Scripts/python.exe
ifeq ("$(wildcard $(PYTHON))","")
	PYTHON := .venv/bin/python
endif

.PHONY: venv install test coverage lint lintfix pretty autofix doc uml run clean report deps checkenv readme

# ============================================================
# Create and activate virtual environment (.venv)
# ============================================================
venv:
	@echo "🐷 Creating virtual environment (.venv)..."
ifeq ($(OS),Windows_NT)
	@python -m venv .venv
	@echo "✅ Virtual environment created!"
	@echo "👉 Activate with: 'source .venv/Scripts/activate' (Git Bash)"
	@echo "   or '.venv\\Scripts\\Activate.ps1' (PowerShell)"
else
	@python3 -m venv .venv
	@echo "✅ Virtual environment created!"
	@echo "👉 Activate with: 'source .venv/bin/activate'"
endif

# ============================================================
# Dependency installation
# ============================================================
install: venv
	@echo "📦 Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	@if [ -f requirements.txt ]; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "⚠️  No requirements.txt found! Installing defaults..."; \
		$(PYTHON) -m pip install pytest pytest-cov flake8 pylint black isort autopep8 docformatter pdoc graphviz; \
	fi
	@echo "✅ Installation complete!"

# ============================================================
# Testing and coverage
# ============================================================
test:
	@echo "🧪 Running unit tests..."
	$(PYTHON) -m pytest -v --maxfail=1 --disable-warnings -q
	@echo "✅ Tests complete!"

coverage:
	@echo "📊 Generating coverage report..."
	$(PYTHON) -m pytest --cov=src --cov-report=term-missing
	@echo "✅ Coverage finished!"

# ============================================================
# Code quality and linting
# ============================================================
lint:
	@echo "🔍 Checking code quality..."
	$(PYTHON) -m flake8 src tests || true
	$(PYTHON) -m pylint src || true
	$(PYTHON) -m black --check src tests || true
	@echo "✅ Linting complete!"

# ============================================================
# Quick PEP8 fixer
# ============================================================
lintfix:
	@echo "🧼 Fixing minor code style issues..."
	$(PYTHON) -m black src tests
	$(PYTHON) -m autopep8 --in-place --aggressive --aggressive -r src tests
	@echo "✅ Code style corrected!"

# ============================================================
# Full code beautification (Pretty Mode)
# ============================================================
pretty:
	@echo "=============================================="
	@echo "✨ Starting full code cleanup (Pretty Mode)"
	@echo "=============================================="
	-$(PYTHON) -m isort src tests || echo "⚠️ isort not found!"
	-$(PYTHON) -m black src tests || echo "⚠️ black not found!"
	-$(PYTHON) -m autopep8 --in-place --aggressive --aggressive -r src tests || echo "⚠️ autopep8 not found!"
	@echo "🪶 Formatting docstrings..."
	-$(PYTHON) -m docformatter -r -i src tests \
		--wrap-summaries 100 --wrap-descriptions 100 \
		--make-summary-multi-line --pre-summary-newline \
		--close-quotes-on-newline --in-place --blank || echo "⚠️ docformatter not found!"
	@echo "✅ Code and docstrings fully polished!"
	@echo "=============================================="

# ============================================================
# Documentation and UML
# ============================================================
doc:
	@echo "📚 Generating API documentation..."
	rm -rf doc/api || true
	$(PYTHON) -m pdoc src -o doc/api
	@echo "✅ Documentation saved in doc/api"

uml:
	@echo "📈 Generating UML diagrams..."
	$(PYTHON) -c "import pylint, os, subprocess, sys; mp=os.path.join(os.path.dirname(pylint.__file__),'pyreverse','main.py'); subprocess.run([sys.executable, mp, '-o','png','-p','PigGame','src'], check=False)"
	@mkdir -p doc/uml || true
	@mv -f classes_PigGame.* packages_PigGame.* doc/uml/ 2>/dev/null || true
	@echo "✅ UML diagrams saved in doc/uml"

# ============================================================
# Run the game
# ============================================================
run:

	@$(PYTHON) -m src.game_cmd

# ============================================================
# Cleanup
# ============================================================
clean:
	@echo "🧹 Cleaning project..."
	rm -rf __pycache__ .pytest_cache .coverage .mypy_cache \
		doc/api doc/uml \
		coverage_report.txt rapport.txt test_report.txt || true
	@echo "✅ Project cleaned!"

# ============================================================
# Combined report (tests + coverage + statistics)
# ============================================================
report:
	@echo "🧾 Creating report..."
	@date +"=== REPORT GENERATED: %Y-%m-%d %H:%M:%S" > rapport.txt
	@echo "# Test results" >> rapport.txt
	@$(PYTHON) -m pytest -v --disable-warnings --maxfail=3 | tee -a rapport.txt
	@echo "# Coverage summary" >> rapport.txt
	@$(PYTHON) -m pytest --cov=src --cov-report=term | tee -a rapport.txt
	@echo "# Assertion count" >> rapport.txt
	@grep -c "assert " tests/*.py | tee -a rapport.txt
	@echo "✅ Report complete! See rapport.txt for details."

# ============================================================
# Automated README update (bonus)
# ============================================================
readme:
	@echo "🧾 Updating README.md with latest test results..."
	@if [ -f generate_readme.py ]; then \
		$(PYTHON) generate_readme.py; \
	else \
		echo "⚠️  generate_readme.py not found!"; \
	fi
	@echo "✅ README.md updated with test summary!"

# ============================================================
# Verify environment & dependencies
# ============================================================
checkenv:
	@echo "🧭 Checking Python environment..."
	@$(PYTHON) --version
	@$(PYTHON) -m pip list | grep -E "pytest|pdoc|flake8|pylint|black|autopep8|isort|docformatter" || true
	@echo "✅ Environment check complete!"

# ============================================================
# Take a break ☕ — Developer Easter Egg
# ============================================================
coffee:
	@echo ""
	@echo "     (  )   (   )  )"
	@echo "      ) (   )  (  ("
	@echo "      ( )  (    ) )"
	@echo "      _____________"
	@echo "     <_____________> ___"
	@echo "     |             |/ _ \\"
	@echo "     |               | | |"
	@echo "     |               |_| |"
	@echo "  ___|             |\\___/"
	@echo " /    \\___________/    \\"
	@echo " \\_____________________/"
	@echo ""
	@echo "Brewing virtual coffee... Please wait..."
	@sleep 2
	@echo "Energy restored! Time to code smarter, not harder."
	@echo ""
