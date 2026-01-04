# 🐷 Pig Game — Test Driven Development Assignment

## 📚 Project Overview
This project was developed as part of the **Assignment 2 – Test Driven Development** course at **Kristianstad University (HKR)**.

The aim is to demonstrate:
- Object-oriented design in Python.  
- Test-driven development (TDD) using `pytest`.  
- Code quality through linting (`flake8`, `pylint`).  
- Automated documentation (`pdoc`) and UML generation (`pyreverse`).  
- Clean, maintainable and *pythonic* code that follows PEP 8 and PEP 20.

The game implemented is **Pig (Dice Game)** — a simple but strategic dice game for one or two players.  
It can be played **player vs player** or **player vs computer** with adjustable AI intelligence levels.

---

## 🧠 Game Rules (Summary)
- Players take turns rolling a six-sided die.  
- Each roll adds points to the turn total.  
- Rolling a **1** resets the turn score to 0 and ends the turn.  
- A player may choose to **hold**, banking the current turn points to their total score.  
- The first to reach **100 points** wins.  
- The game supports:
  - Name selection and name changes  
  - Persistent high-score tracking  
  - An optional **cheat mode** (for testing)
  - Configurable **AI intelligence** for the computer player

---

## 🏗️ Project Structure
pig_game/
├── src/
│ ├── init.py
│ ├── cheat.py
│ ├── dice.py
│ ├── game.py
│ ├── game_cmd.py
│ ├── highscore.py
│ ├── intelligence.py
│ └── player.py
├── tests/
│ ├── test_cheat.py
│ ├── test_dice.py
│ ├── test_game.py
│ ├── test_game_cmd.py
│ ├── test_highscore.py
│ ├── test_intelligence.py
│ └── test_player.py
├── Makefile
├── requirements.txt
├── README.md
└── doc/
├── api/ ← Generated documentation (pdoc)
└── uml/ ← Generated UML diagrams (pyreverse)

yaml
Kopiera kod

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the project
```bash
git clone <repository-url>
cd pig_game
2️⃣ Create and activate a virtual environment
bash
Kopiera kod
python -m venv .venv
# Activate:
# On Windows (Git Bash)
source .venv/Scripts/activate
# On Linux / macOS
source .venv/bin/activate
3️⃣ Install dependencies
bash
Kopiera kod
make install
(Installs all required tools: pytest, coverage, flake8, pylint, black, pdoc, pyreverse etc.)

🎮 Running the Game
bash
Kopiera kod
make run
or directly:

bash
Kopiera kod
python -m src.game_cmd
The game starts in the terminal and supports commands such as roll, hold, quit, rules, and cheat.

🧪 Testing and Coverage
All classes are covered by unit tests under tests/.
To execute the full suite:

bash
Kopiera kod
make test
To generate a coverage report:

bash
Kopiera kod
make coverage
Expected result:

matlab
Kopiera kod
TOTAL 100%  ✓
🧹 Code Quality & Linting
Ensure your code passes both flake8 and pylint:

bash
Kopiera kod
make lint
To automatically format and correct minor issues:

bash
Kopiera kod
make lintfix
# or
make pretty
Linting rules follow:

PEP 8 (Black compatible, 88 chars)

Google-style docstrings

Warnings suppressed only for E203, W503, D212 (Black conflicts)

📘 Generate Documentation
Documentation is built automatically from Python docstrings using pdoc.

bash
Kopiera kod
make doc
Output:

bash
Kopiera kod
doc/api/index.html
Open in a web browser to browse the generated API documentation.

📈 Generate UML Diagrams
Use pyreverse (via pylint) to reverse-engineer class and package diagrams.

bash
Kopiera kod
make uml
UML images will be created under:

bash
Kopiera kod
doc/uml/classes_PigGame.png
doc/uml/packages_PigGame.png
🧾 Project Report
Combine test results, coverage data, and assert counts into one report:

bash
Kopiera kod
make report
This generates rapport.txt summarizing:

Time stamp

Test results

Coverage summary

Assertion counts per file

🪶 Documentation Standards
All public classes and methods include docstrings (Google style).

Code formatting handled by black and isort.

Max line length = 88 characters (Black default).

Docstrings formatted using docformatter.

Code is lint-clean (no E501, D400, D403, etc.).

🧰 Development Tools
Tool	Purpose
pytest	Unit testing
pytest-cov	Coverage measurement
flake8 + flake8-docstrings	Code style checking
pylint	Static analysis
black + isort + autopep8	Formatting & import sorting
pdoc	Automatic HTML documentation
pyreverse (pylint)	UML generation
make	Task automation

🧮 Metrics & Testing Summary
✅ 100 % test coverage (all modules tested)

🧩 > 10 test cases per class

📏 > 20 assertions per class

🧱 Docstrings complete and validated

🧠 Game resilient to bad input (try/except guards)

🧑‍💻 Developer Guidelines
Follow PEP 8 and PEP 20 (“The Zen of Python”).

Keep methods short and focused.

Use type hints where appropriate.

Prefer composition and clarity over complexity.

Write tests first (TDD).

All commits should be atomic and well-commented.

Include LICENSE.md and requirements.txt in repo.

🧪 Self-Test Before Submission
✅ Fresh clone installs and runs without errors
✅ All tests pass with ≥ 90 % coverage
✅ make lint and make pretty produce no issues
✅ Documentation and UML can be regenerated
✅ README.md explains installation and usage
✅ Code robust against bad input
✅ Game meets functional requirements

🧑‍🏫 Authors & Credits
Name	        Role
Morgan Lindbom	Development / Testing / Documentation
Yousef Martaa	Development / Testing / Documentation

🪪 License
This project is released under the MIT License.
See LICENSE.md for details.

yaml
Kopiera kod

---







## 🧪 Automated Test & Coverage Report
**Generated automatically:** 2025-11-06 17:27:05

**Summary:** ✅ 94% coverage — 2025-11-06 17:27:05

```text
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-8.4.2, pluggy-1.6.0
rootdir: C:\Users\morga\Desktop\pig_game_seminar_2
configfile: pytest.ini
plugins: cov-7.0.0
collected 152 items

tests\test_cheat.py ...............                                      [  9%]
tests\test_dice.py ..........                                            [ 16%]
tests\test_game.py ..........                                            [ 23%]
tests\test_game_cmd.py ............................................      [ 51%]
tests\test_highscore.py .........................                        [ 68%]
tests\test_init.py ..........                                            [ 75%]
tests\test_intelligence.py ....................                          [ 88%]
tests\test_player.py ..................                                  [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.7-final-0 _______________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src\__init__.py           0      0   100%
src\cheat.py             63      3    95%   7-8, 67
src\dice.py               4      0   100%
src\game.py              89      8    91%   43-44, 72, 79, 126, 144, 152, 159
src\game_cmd.py         215     18    92%   88, 100-101, 115-123, 145-146, 249-250, 281, 347, 351
src\highscore.py         94      8    91%   42, 56, 58, 71, 95, 111, 125, 149
src\intelligence.py      72      0   100%
src\player.py            47      0   100%
---------------------------------------------------
TOTAL                   584     37    94%
============================= 152 passed in 2.03s =============================
```
