"""Structural and execution checks for the generated notebook collection."""

from __future__ import annotations

import json
import re
import sys
import types
from pathlib import Path


ROOT = Path("python_ai_interview")
EXPECTED = [
    "01_Python_Data_Structures.ipynb",
    "02_Functions_Classes_and_Python_Core.ipynb",
    "03_Comprehensions_and_Collections.ipynb",
    "04_NumPy_for_AI_Engineers.ipynb",
    "05_Pandas_for_AI_Engineers.ipynb",
    "06_Clean_Python_and_Interview_Patterns.ipynb",
    "07_LeetCode_Patterns_for_AI_Engineers.ipynb",
    "08_AI_Engineer_Python_Mock_Interview.ipynb",
    "Python_Interview_Cheat_Sheet.ipynb",
]


def validate() -> None:
    assert sorted(path.name for path in ROOT.glob("*.ipynb")) == sorted(EXPECTED)
    notebooks = {}
    footer_quizzes = []
    for name in EXPECTED:
        notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        assert notebook["metadata"]["language_info"]["version"] == "3.11"
        markdown = "\n".join(cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "markdown")
        for required in ("Estimated study/practice time", "Prerequisites", "Table of contents", "Key takeaways", "Mistakes to avoid", "10 rapid-fire interview questions", "Readiness checklist"):
            assert required in markdown, (name, required)
        assert any(cell["cell_type"] == "code" for cell in notebook["cells"]), f"{name} has no executable example"
        assert any("TODO" in cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "code"), f"{name} has no active exercise"
        quiz_text = markdown.split("## 10 rapid-fire interview questions", 1)[1].split("## Readiness checklist", 1)[0]
        footer_quizzes.append(quiz_text)
        notebooks[name] = (notebook, markdown)

    assert len(set(footer_quizzes)) == len(EXPECTED), "Rapid-fire footers must be notebook-specific"

    fundamentals = sum(notebooks[name][1].count("### Exercise —") for name in EXPECTED[:3] + [EXPECTED[5]])
    assert fundamentals >= 40, fundamentals
    assert notebooks[EXPECTED[3]][1].count("### Exercise —") >= 20
    assert notebooks[EXPECTED[4]][1].count("### Exercise —") >= 20
    assert notebooks[EXPECTED[6]][1].count("**Problem summary:**") >= 20
    assert notebooks[EXPECTED[7]][1].count("### Debugging exercise") >= 10
    assert notebooks[EXPECTED[8]][1].count("<details><summary>Answer</summary>") >= 120

    # Concrete exercise scaffolding: each generated exercise has input/output,
    # two hints, a separated solution, explicit time/space, and a mistake.
    for name, (_, markdown) in notebooks.items():
        exercise_count = markdown.count("### Exercise —") + markdown.count("**Problem summary:**")
        if exercise_count:
            assert markdown.count("Input") >= exercise_count, (name, "exercise input examples")
            assert markdown.count("Output") >= exercise_count, (name, "exercise output examples")
            assert markdown.count("Hint 1") >= exercise_count, (name, "hint 1")
            assert markdown.count("Hint 2") >= exercise_count, (name, "hint 2")
            assert markdown.count("Time:") >= exercise_count, (name, "time complexity")
            assert markdown.count("Space:") >= exercise_count, (name, "space complexity")
            assert markdown.lower().count("common mistake") >= exercise_count, (name, "common mistakes")

    all_text = "\n".join(cell["source"] for notebook, _ in notebooks.values() for cell in notebook["cells"])
    for forbidden in ("See assertion in solution", "Time typically O(n)", "Time and space depend", "lambda z:", "out :=", "(_ for _ in ())", "items.count(x)"):
        assert forbidden not in all_text, forbidden

    topic_terms = {
        EXPECTED[0]: ("d.keys()", "d.values()", "nums[2:]", "min_and_max"),
        EXPECTED[1]: ("Optional[str]", "class BadRegistry", "with open", "@log_call"),
        EXPECTED[2]: ("Too dense", "range(len(names))", "sorted_nums", "max(zip"),
        EXPECTED[3]: ("np.random.randn", "broadcasting", "ravel()", "flatten()"),
        EXPECTED[4]: ("dropna", "fillna", "validate=", "value_counts", "dayofweek"),
        EXPECTED[6]: ("seen[ch] >= left", "level_order_values", "iterative_dfs_values", "bisect_left"),
    }
    for name, terms in topic_terms.items():
        notebook_text = "\n".join(cell["source"] for cell in notebooks[name][0]["cells"])
        for term in terms:
            assert term in notebook_text, (name, term)

    concept_minimums = {EXPECTED[0]: 6, EXPECTED[1]: 5, EXPECTED[2]: 4, EXPECTED[3]: 5, EXPECTED[4]: 5, EXPECTED[5]: 4}
    for name, minimum in concept_minimums.items():
        assert notebooks[name][1].count("**Concept") >= minimum, (name, "structured concept sections")

    for name, (notebook, _) in notebooks.items():
        module_name = "notebook_" + re.sub(r"\W", "_", name)
        module = types.ModuleType(module_name)
        sys.modules[module_name] = module
        namespace = module.__dict__
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            try:
                exec(compile(cell["source"], f"{name}:cell-{index}", "exec"), namespace)
            except Exception as error:
                raise RuntimeError(f"{name} failed in code cell {index}: {error}") from error
        print(f"PASS {name}: {len(notebook['cells'])} cells")


if __name__ == "__main__":
    validate()
