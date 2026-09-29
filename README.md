# Python for AI Engineer Interviews

Practice Python fundamentals, data work, and coding interview patterns with Jupyter notebooks. This repository also includes **PyReady**, a browser-friendly version of the lessons, and a printable Python quick reference.

## What's here

| Path | Contents |
| --- | --- |
| [`python_ai_interview/`](python_ai_interview/) | Eight numbered practice notebooks and a notebook cheat sheet |
| [`python_ai_interview_site/`](python_ai_interview_site/) | PyReady course website built from the notebooks |
| [`python_cheat_sheet/python_cheat_sheet.pdf`](python_cheat_sheet/python_cheat_sheet.pdf) | Printable Python 3.12+ quick reference |
| [`python_cheat_sheet/python_cheat_sheet.tex`](python_cheat_sheet/python_cheat_sheet.tex) | LaTeX source for the printable reference |
| [`generate_notebooks.py`](generate_notebooks.py) | Generates the nine notebooks |
| [`validate_notebooks.py`](validate_notebooks.py) | Checks notebook structure and runs their code cells |

## Study the notebooks

The numbered notebooks form a suggested learning path:

1. [Python Data Structures](python_ai_interview/01_Python_Data_Structures.ipynb) — lists, dictionaries, sets, tuples, and copying
2. [Functions, Classes, and Python Core](python_ai_interview/02_Functions_Classes_and_Python_Core.ipynb) — functions, scope, typing, errors, decorators, and generators
3. [Comprehensions and Collections](python_ai_interview/03_Comprehensions_and_Collections.ipynb) — comprehensions and standard collection tools
4. [NumPy for AI Engineers](python_ai_interview/04_NumPy_for_AI_Engineers.ipynb) — arrays, shapes, broadcasting, and linear algebra
5. [pandas for AI Engineers](python_ai_interview/05_Pandas_for_AI_Engineers.ipynb) — DataFrames, missing data, grouping, joins, and ML features
6. [Clean Python and Interview Patterns](python_ai_interview/06_Clean_Python_and_Interview_Patterns.ipynb) — readable solutions, edge cases, and complexity
7. [LeetCode Patterns for AI Engineers](python_ai_interview/07_LeetCode_Patterns_for_AI_Engineers.ipynb) — guided algorithm practice
8. [AI Engineer Python Mock Interview](python_ai_interview/08_AI_Engineer_Python_Mock_Interview.ipynb) — a five-round practice interview

Use the [interview cheat sheet notebook](python_ai_interview/Python_Interview_Cheat_Sheet.ipynb) for review and rapid-fire questions. Each lesson includes executable examples and `TODO` exercises; try the exercises before reading the solutions.

To run the notebooks locally, use Python 3.11 and install Jupyter, NumPy, pandas, and Matplotlib. For example:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install jupyter numpy pandas matplotlib ipykernel
jupyter lab
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Open a notebook from `python_ai_interview/` and select the environment's Python kernel.

## Run PyReady locally

The website displays the notebook content with navigation, searchable lessons, revealable solutions, and progress saved in your browser. Code shown on the site is for reading and copying; run it in Jupyter to practice interactively.

Requires Node.js **22.13.0 or newer**:

```bash
cd python_ai_interview_site
npm install
npm run dev
```

Open the local URL printed by the development server. The site uses [vinext](https://github.com/cloudflare/vinext), React, and Vite.

## Update the content

Run these commands from the repository root:

```bash
python generate_notebooks.py
python validate_notebooks.py
node python_ai_interview_site/scripts/import-notebooks.mjs
```

`generate_notebooks.py` rewrites the notebooks in `python_ai_interview/`. The import script then refreshes `python_ai_interview_site/app/data/lessons.json`, which the site reads. Run the validator in an environment with NumPy, pandas, and Matplotlib installed.

To rebuild the printable quick reference after editing its LaTeX source, run this from `python_cheat_sheet/` with a LaTeX installation that provides the packages used in the source:

```bash
pdflatex python_cheat_sheet.tex
```

The existing PDF is ready to use without building it yourself.
