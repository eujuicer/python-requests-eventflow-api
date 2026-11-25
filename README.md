# Python requests — EventFlow API

Practice repository: querying and working with the **EventFlow** API in Python
using the [`requests`](https://requests.readthedocs.io/) library.

## Prerequisites

- Python 3.10+
- The EventFlow API must be running locally at `http://localhost:8000`
  (Swagger documentation: `http://localhost:8000/docs`)

## Installation

```bash
# 1. Create the virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

# 3. Install the dependencies
pip install -r requirement.txt
```

The terminal shows `(venv)` at the start of the line when the environment is active.
To leave it: `deactivate`.

## Usage

```bash
python main.py
```

To run the solutions of the Day 2 (J2) exercises:

```bash
python exercices_j2.py
```

## Repository contents

| File                        | Description                                               |
|-----------------------------|-----------------------------------------------------------|
| `main.py`                   | API exploration script (GET requests, query params, path params) |
| `exercices_j2.py`           | Solutions of the Day 2 exercises (levels 1 to 4, solo mission, bonus) |
| `J2_requests_cours.md`      | Course: `requests` for testers (Bruno → Python), in French |
| `J2_exercices_eleves.md`    | Day 2 exercise statements, in French                       |
| `requirement.txt`           | Python dependencies of the project                         |

## Notes

- The `venv/` folder (or equivalent) must never be committed — it is
  already excluded via `.gitignore`.
- After adding a dependency: `pip freeze > requirement.txt`.
