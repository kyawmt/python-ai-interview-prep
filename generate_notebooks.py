"""Generate the Python AI Engineer interview-practice notebook collection."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


OUT = Path("python_ai_interview")


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": dedent(text).strip() + "\n"}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip() + "\n",
    }


def intro(title: str, objectives: list[str], minutes: str, sections: list[str], prereq: str) -> list[dict]:
    toc = "\n".join(f"{i}. [{name}](#{name.lower().replace(' ', '-').replace('/', '')})" for i, name in enumerate(sections, 1))
    goals = "\n".join(f"- {goal}" for goal in objectives)
    return [md(f"""
    # {title}

    {goals}

    **Estimated study/practice time:** {minutes}  
    **Prerequisites:** {prereq}

    **Priority legend:** 🔴 **Must Know** · 🟠 **Important** · 🟢 **Good to Know**

    ## Table of contents

    {toc}

    > Active-practice rule: run examples, predict output before revealing it, complete every `TODO`, then compare with the solution below it.
    """)]


def setup_cell() -> dict:
    return md("""
    ## Environment setup

    ```bash
    conda create -n python-ai-interview python=3.11 -y
    conda activate python-ai-interview
    pip install jupyter numpy pandas matplotlib ipykernel
    python -m ipykernel install --user --name python-ai-interview --display-name "Python AI Interview"
    ```

    Registering a kernel lets Jupyter and VS Code select this exact environment and its installed packages.
    """)


EXAMPLE_CASES = {
    # NumPy
    "vector_norm": "Input: [3.0, 4.0]\nOutput: 5.0",
    "normalize_vector": "Input: [3.0, 4.0]\nOutput: [0.6, 0.8]",
    "standardize_columns": "Input: [[1, 2], [3, 4]]\nOutput: each output column has mean 0 and standard deviation 1",
    "row_max": "Input: [[1, 3], [4, 2]]\nOutput: [3, 4]",
    "cosine_similarity": "Input: [1, 0], [1, 0]\nOutput: 1.0",
    "flatten_images": "Input shape: (2, 3, 4)\nOutput shape: (2, 12)",
    "filter_predictions": "Input: [0.2, 0.8], threshold=0.5\nOutput: [0.8]",
    "linear_layer": "Input shapes: X=(2,3), W=(3,1), b=(1,)\nOutput shape: (2,1)",
    "one_hot": "Input: labels=[0,2], classes=3\nOutput: [[1,0,0],[0,0,1]]",
    "column_means": "Input: [[1,2],[3,4]]\nOutput: [2,3]",
    "row_softmax": "Input: [[1.0, 2.0]]\nOutput: one row of probabilities summing to 1",
    "clip_scores": "Input: [-1, 0.5, 2]\nOutput: [0, 0.5, 1]",
    "replace_nan": "Input: [[1, NaN], [3, 2]]\nOutput: no NaNs; missing value uses its column mean",
    "top_index_per_row": "Input: [[1,2],[3,0]]\nOutput: [1,0]",
    "pairwise_scores": "Input shapes: X=(2,3), Y=(4,3)\nOutput shape: (2,4)",
    "center_rows": "Input: [[1,3]]\nOutput: [[-1,1]]",
    "batch_indices": "Input: n=4, seed=42\nOutput: a reproducible permutation of [0,1,2,3]",
    "accuracy": "Input: true=[1,0], predicted=[1,1]\nOutput: 0.5",
    "confusion_counts": "Input: true=[0,1], predicted=[0,1], classes=2\nOutput: [[1,0],[0,1]]",
    "minmax_columns": "Input: [[1,2],[3,2]]\nOutput: [[0,0],[1,0]]",
    # pandas
    "select_features": "Input columns: age, salary, label\nOutput columns: age, salary",
    "filter_adults": "Input ages: [17,18]\nOutput: row with age 18",
    "sg_high_salary": "Input: SG/10 and US/20, threshold=5\nOutput: SG/10 row",
    "missing_counts": "Input column x=[1,NaN]\nOutput: x=1",
    "fill_age": "Input age=[NaN], training median=20\nOutput age=[20]",
    "drop_exact_duplicates": "Input x=[1,1]\nOutput: one row with x=1",
    "label_distribution": "Input labels=[1,1,0]\nOutput: class 1 proportion=2/3",
    "country_salary": "Input: a/1, a/3\nOutput: a mean salary=2",
    "country_summary": "Input: one country=a salary=2\nOutput: mean_salary=2, rows=1",
    "left_join_predictions": "Input users 1,2 and prediction for 1\nOutput: two rows; user 2 score is missing",
    "rank_scores": "Input scores=[0.1,0.9]\nOutput first score=0.9",
    "add_margin": "Input top1=0.9, top2=0.7\nOutput margin=0.2",
    "parse_month": "Input date=2026-02-01\nOutput month=2",
    "unique_users": "Input two dated rows for user 1\nOutput: latest row only",
    "class_counts": "Input labels=[1,NaN]\nOutput: total count=2 including missing",
    "rename_target": "Input column label\nOutput column target",
    "query_ids": "Input user 1 score=0.9, threshold=0.8\nOutput: [1]",
    "pivot_metrics": "Input model=a, split=test, score=0.5\nOutput: pivot cell (a,test)=0.5",
    "string_normalize": "Input text=' A '\nOutput text='a'",
    "safe_export": "Input one-column DataFrame\nOutput: CSV text without an index column",
    # clean-Python drills
    "safe_first": "Input: []\nOutput: None",
    "last_index": "Input: [1,2]\nOutput: 1",
    "count_truthy": "Input: [0,1,'',2]\nOutput: 2",
    "equal_values": "Input: [1], [1]\nOutput: True",
    "copy_append": "Input: [1], 2\nOutput: [1,2] while input remains [1]",
    "frequency_map": "Input: ['a','a']\nOutput: {'a': 2}",
    "unique_count": "Input: [1,1,2]\nOutput: 2",
    "pair_items": "Input: [1], [2]\nOutput: [(1,2)]",
    "indexed": "Input: ['a']\nOutput: [(0,'a')]",
    "sorted_copy": "Input: [2,1]\nOutput: [1,2] while input remains unchanged",
    "descending": "Input: [1,2]\nOutput: [2,1]",
    "key_with_max": "Input: {'a':1,'b':2}\nOutput: 'b'",
    "all_positive": "Input: [1,2]\nOutput: True",
    "any_missing": "Input: [1,None]\nOutput: True",
    "merge_options": "Input: defaults={'a':1}, overrides={'a':2}\nOutput: {'a':2}",
    "safe_get": "Input: {}, key='x', default=0\nOutput: 0",
    "immutable_key": "Input: [1,2]\nOutput: (1,2)",
    "remove_none": "Input: [0,None]\nOutput: [0]",
    "clamp": "Input: value=10, low=0, high=5\nOutput: 5",
    "chunk_count": "Input: n=5, size=2\nOutput: 3",
    "palindrome": "Input: 'A man, a plan, a canal: Panama'\nOutput: True",
    "validate_nonempty": "Input: ''\nOutput: raises ValueError",
}


def exercise(title: str, goal: str, starter: str, solution: str, example: str, hint1: str,
             hint2: str, complexity: str, mistake: str, difficulty: str = "🟢 Easy") -> list[dict]:
    exercise_name = title.split()[-1]
    if example == "See assertion in solution":
        example = EXAMPLE_CASES[exercise_name]
    elif "Input:" not in example and "Input shape:" not in example:
        if " -> " in example:
            sample_input, sample_output = example.split(" -> ", 1)
            example = f"Input: {sample_input}\nOutput: {sample_output}"
        else:
            example = f"Input: {example}\nOutput: a result satisfying the stated goal"
    if complexity.startswith("Time/Space "):
        bound = complexity.removeprefix("Time/Space ")
        complexity = f"Time: {bound}\nSpace: {bound}"
    else:
        complexity = complexity.replace("Time ", "Time: ").replace("Space ", "Space: ")
    return [
        md(f"""
        ### Exercise — {difficulty}: {title}

        **Goal:** {goal}

        **Example**

        ```text
        {example}
        ```

        <details><summary>Hint 1</summary>{hint1}</details>
        <details><summary>Hint 2</summary>{hint2}</details>
        """),
        code(starter),
        md("#### Solution — reveal only after attempting"),
        code(solution),
        md(f"""
        **Complexity**

        ```text
        {complexity}
        ```

        **Common mistake:** {mistake}
        """),
    ]


def footer(takeaways: list[str], mistakes: list[str], questions: list[tuple[str, str]], checklist: list[str]) -> list[dict]:
    take = "\n".join(f"- {x}" for x in takeaways)
    bad = "\n".join(f"- {x}" for x in mistakes)
    quiz = "\n".join(f"{i}. **{q}** <details><summary>Answer</summary>{a}</details>" for i, (q, a) in enumerate(questions, 1))
    checks = "\n".join(f"- [ ] {x}" for x in checklist)
    return [md(f"""
    ## Key takeaways

    {take}

    ## Mistakes to avoid

    {bad}

    ## 10 rapid-fire interview questions

    {quiz}

    ## Readiness checklist

    {checks}
    """)]


def write_notebook(name: str, cells: list[dict]) -> None:
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python AI Interview", "language": "python", "name": "python-ai-interview"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def quiz_for(notebook: str) -> list[tuple[str, str]]:
    """Return ten relevant questions without repeating one universal footer."""
    indexes = {
        "data": range(0, 10),
        "core": range(20, 30),
        "collections": range(40, 50),
        "numpy": range(60, 70),
        "pandas": range(80, 90),
        "clean": range(110, 120),
        "leetcode": range(100, 110),
        "mock": [4, 23, 41, 50, 68, 84, 102, 105, 108, 118],
        "cheat": [10, 31, 45, 55, 71, 91, 101, 111, 115, 119],
    }[notebook]
    bank = rapid_bank()
    return [bank[index] for index in indexes]


def notebook_01() -> None:
    cells = intro(
        "01 — Python Data Structures", ["Choose the right built-in collection", "Reason about references, hashing, and complexity", "Practice interview patterns with AI-flavored data"],
        "3–4 hours", ["Lists", "References and copying", "Dictionaries and hashing", "Sets", "Tuples and mutability", "Selection drills", "Practice"], "Basic Python syntax"
    ) + [setup_cell()]
    cells += [md("""
    ## Lists

    🔴 **Must Know**

    **Concept.** A list is an ordered, mutable dynamic array.  
    **Why it matters.** Lists commonly hold batches, tokens, predictions, and records.  
    **Syntax.** `nums = [1, 2, 3]`; indexing `nums[0]`, negative indexing `nums[-1]`, slicing `nums[start:end:step]`.  
    **How Python executes it.** A list stores references in a contiguous internal array and occasionally reallocates extra capacity, making `append` amortized O(1).

    **Syntax:** `nums = [1, 2, 3]`; indexing `nums[0]`, negative indexing `nums[-1]`, slicing `nums[start:end:step]`.

    | Operation | Typical time |
    |---|---:|
    | index | O(1) |
    | append / pop end | amortized O(1) / O(1) |
    | insert beginning / remove by value | O(n) |
    | membership | O(n) |
    | sort | O(n log n) |

    **Interview question:** Why is inserting at index 0 slow? Every existing reference must shift right.
    **Exercise/solution:** complete *slice batches* in the Practice section before viewing its solution.
    """), code("""
    nums = [3, 1, 2]
    print(nums[0], nums[-1], nums[:3], nums[2:], nums[::-1], nums[::2])
    nums.append([4, 5])      # one nested element
    print(nums)
    nums = [3, 1, 2]
    nums.extend([4, 5])      # two elements
    nums.insert(0, 9)
    nums.remove(3)
    last = nums.pop()
    sorted_copy = sorted(nums)  # new list
    nums.sort()                  # mutates, returns None
    nums.reverse()
    print(nums, sorted_copy, last, 2 in nums)
    """), md("""
    **Common interview mistake:** assigning `result = nums.sort()` makes `result` be `None`. Slice end is exclusive; `nums[:3]` contains indices 0–2.

    ### List slicing

    **Concept.** `nums[start:end:step]` creates a shallow list copy of the selected references.  
    **Why it matters.** Slicing is common in batching, windows, and reversing interview inputs.  
    **Syntax/example.** `nums[:3]`, `nums[2:]`, `nums[::-1]`, and `nums[::2]`.  
    **How Python executes it.** Python normalizes the indices, walks the selected positions, and copies their references into a new outer list.  
    **Complexity.** Time and space are O(k) for k selected elements.  
    **Common interview mistake.** Treating the end index as inclusive.  
    **Interview question.** Does a list slice deep-copy nested values? No.  
    **Exercise/solution.** Complete *slice batches* below.

    ## References and copying

    🔴 **Must Know**

    **Concept.** Assignment copies a reference, not an object. A shallow copy (`copy()` or `[:]`) creates a new outer list but shares nested objects; `deepcopy` recursively copies the reachable structure.  
    **Why it matters.** AI preprocessing should not mutate caller-owned batches accidentally.  
    **Syntax.** `alias = a`, `shallow = a.copy()`, `shallow = a[:]`, `deep = copy.deepcopy(a)`.  
    **How Python executes it.** Names point to objects; shallow copying duplicates only the outer reference array.  
    **Complexity.** Shallow list copy is O(n); deep-copy cost is proportional to the reachable object graph.  
    **Common interview mistake.** Assuming a shallow copy makes nested lists independent.  
    **Interview question.** Why do changes through `b = a` appear through `a`? Both names reference one object.  
    **Exercise/solution.** Complete *safe metadata* below.

    ```text
    a ──┐
        ├──> [1, 2, 3]
    b ──┘

    shallow_a --> [ inner ──> [1, 2] ]
    shallow_b --> [ inner ──> [1, 2] ]
    ```
    """), code("""
    import copy

    a = [[1, 2], [3, 4]]
    alias = a
    shallow_1 = a.copy()
    shallow_2 = a[:]
    deep = copy.deepcopy(a)
    alias.append([5])
    shallow_1[0].append(99)
    print("original", a)
    print("same outer?", alias is a, shallow_1 is a)
    print("shared inner?", shallow_1[0] is a[0], shallow_2[0] is a[0])
    print("deep independent?", deep[0] is not a[0], deep)
    """), md("""
    ## Dictionaries and hashing

    🔴 **Must Know**

    **Concept.** A dictionary maps unique hashable keys to values using a hash table.  
    **Why it matters.** Dictionaries power counting, caching, grouping, ID lookup, and complement lookup in Two Sum.  
    **Syntax.** `d[key] = value`, `d.get(key, default)`, `d.keys()`, `d.values()`, `d.items()`.  
    **How Python executes it.** Conceptually:

    ```text
    key → hash(key) → bucket/location → key equality check → value
    ```

    **Complexity.** Lookup, insert, and delete are average O(1), worst-case O(n).  
    **Common interview mistake.** `d[key]` raises `KeyError`; `d.get(key, default)` supplies a fallback.  
    **Interview question.** Why must keys be hashable? Their hash/equality must remain stable while stored.  
    **Exercise/solution.** Complete *group by source* and *first duplicate* below.
    """), code("""
    user = {"name": "Alice", "age": 30}
    user["role"] = "ML Engineer"
    print(user["name"], user.get("country", "unknown"))
    user.setdefault("skills", []).append("Python")
    print("keys", list(user.keys()))
    print("values", list(user.values()))
    for key, value in user.items():
        print(key, value)
    del user["age"]

    tokens = ["rag", "llm", "rag"]
    counts = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    from collections import Counter
    print(counts, Counter(tokens))
    """), md("""
    **How Python executes it.** Python hashes the key, probes for a matching slot, then checks equality. Mutable lists cannot be keys because changing them would invalidate their location. A tuple works only when all its contents are hashable.

    **Common mistake:** using `if d.get(key):` to test existence fails when the stored value is false-like; use `if key in d:`.

    ## Sets

    🔴 **Must Know**

    **Concept.** A set is a hash table of unique hashable values.  
    **Why it matters.** It turns repeated membership checks and duplicate detection from O(n) per list lookup into average O(1).  
    **Syntax.** `seen=set()`, `add`, `remove`, `discard`, union `|`, intersection `&`, difference `-`.  
    **How Python executes it.** Values are hashed into table locations; collisions are resolved and equality confirms a match.  
    **Complexity.** Average add, remove, and membership O(1); worst case O(n).  
    **Common interview mistake.** `remove` raises if absent; `discard` does not.  
    **Interview question.** Why is a set common in Contains Duplicate? It stores prior values with average O(1) membership.  
    **Exercise/solution.** Complete *first duplicate* and *deduplicate* below.
    """), code("""
    seen = set()
    for model_id in [10, 11, 10]:
        if model_id in seen:
            print("duplicate", model_id)
        seen.add(model_id)
    seen.discard(999)
    print({1, 2} | {2, 3}, {1, 2} & {2, 3}, {1, 2} - {2, 3})
    """), md("""
    ## Tuples and mutability

    🔴 **Must Know**

    **Concept.** Tuples are ordered and immutable.  
    **Why it matters.** They support unpacking, multiple return values, and—when all members are hashable—dictionary keys.  
    **Syntax.** `point=(3,5)`, `x,y=point`, `return minimum, maximum`.  
    **How Python executes it.** Tuple membership references cannot be replaced; hashability still depends on every contained object.  
    **Complexity.** Indexing O(1); membership O(n); construction O(n).  
    **Common interview mistake.** Assuming every tuple is hashable even when it contains a list.  
    **Interview question.** Why use `tuple(sorted(word))`? It converts the sorted list into a stable Group Anagrams key.  
    **Exercise/solution.** Complete *matrix coordinates* below.

    | Type | Mutable? | Normally hashable? |
    |---|---|---|
    | list | Yes | No |
    | dict | Yes | No |
    | set | Yes | No |
    | tuple | No | If contents are hashable |
    | str / int | No | Yes |
    """), code("""
    point = (3, 5)
    x, y = point
    def min_and_max(values):
        return min(values), max(values)
    minimum, maximum = min_and_max([3, 1, 5])
    anagram_key = tuple(sorted("listen"))
    grouped = {anagram_key: ["listen", "silent"]}
    print(x, y, minimum, maximum, grouped)
    """), md("""
    ## Selection drills

    Choose before revealing: 1 fast membership—**set**; 2 key→value—**dict**; 3 ordered mutable sequence—**list**; 4 immutable composite key—**tuple**; 5 FIFO—**deque**; 6 LIFO—**list**; 7 count labels—**Counter/dict**; 8 group documents—**defaultdict(list)**; 9 deduplicate IDs—**set**; 10 preserve duplicates and order—**list**; 11 cache by parameters—**dict**; 12 coordinate—**tuple**; 13 BFS frontier—**deque**; 14 priority frontier—**heap**; 15 top-level JSON payload—**dict**.
    """)]
    fundamentals = [
        ("deduplicate", "Return unique values while preserving order.", "def deduplicate(items):\n    # TODO: Write your solution here\n    pass", "def deduplicate(items):\n    return list(dict.fromkeys(items))\n\nassert deduplicate([3, 1, 3, 2]) == [3, 1, 2]", "[3,1,3,2] -> [3,1,2]", "Track first occurrences.", "Dictionary keys preserve insertion order.", "Time O(n) average; Space O(n)", "Using `set(items)` loses ordering."),
        ("first duplicate", "Return the first value seen twice, or None.", "def first_duplicate(items):\n    # TODO: Write your solution here\n    pass", "def first_duplicate(items):\n    seen = set()\n    for item in items:\n        if item in seen: return item\n        seen.add(item)\n    return None\n\nassert first_duplicate([2,1,3,2]) == 2", "[2,1,3,2] -> 2", "Use a set.", "Check before adding.", "Time O(n) average; Space O(n)", "Adding before checking makes every item appear duplicate."),
        ("group by source", "Group document dictionaries by `source`.", "def group_by_source(docs):\n    # TODO: Write your solution here\n    pass", "from collections import defaultdict\ndef group_by_source(docs):\n    groups = defaultdict(list)\n    for doc in docs: groups[doc['source']].append(doc)\n    return dict(groups)\n\nassert len(group_by_source([{'source':'a'}, {'source':'a'}])['a']) == 2", "two source=a docs -> {'a': [doc, doc]}", "Map source to a list.", "`defaultdict(list)` removes initialization branches.", "Time O(n); Space O(n)", "Using one shared list for every key."),
        ("safe metadata", "Return a copied metadata dict with a score.", "def add_score(metadata, score):\n    # TODO: Write your solution here\n    pass", "def add_score(metadata, score):\n    result = metadata.copy()\n    result['score'] = score\n    return result\n\nsource = {'page': 1}\nassert add_score(source, .8) == {'page':1, 'score':.8} and 'score' not in source", "{'page':1}, .8 -> new dict", "Copy before mutation.", "A shallow copy is enough for a top-level scalar.", "Time O(n); Space O(n)", "Mutating caller-owned metadata."),
        ("matrix coordinates", "Count repeated `(row, column)` coordinates.", "def coordinate_counts(coords):\n    # TODO: Write your solution here\n    pass", "from collections import Counter\ndef coordinate_counts(coords):\n    return Counter(coords)\n\nassert coordinate_counts([(0,1),(0,1)])[(0,1)] == 2", "[(0,1),(0,1)] -> {(0,1):2}", "Tuples are hashable.", "Use Counter.", "Time O(n); Space O(k)", "Trying to use lists as keys."),
        ("slice batches", "Split a list into fixed-size batches.", "def batches(items, size):\n    # TODO: Write your solution here\n    pass", "def batches(items, size):\n    if size <= 0: raise ValueError('size must be positive')\n    return [items[i:i+size] for i in range(0, len(items), size)]\n\nassert batches([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]", "[1,2,3,4,5], 2 -> [[1,2],[3,4],[5]]", "Step by `size`.", "The last slice may be short.", "Time O(n); Space O(n)", "Forgetting to reject size zero."),
    ]
    cells.append(md("## Practice"))
    for item in fundamentals:
        cells += exercise(*item)
    cells += footer(["Lists are dynamic arrays.", "Hash tables drive fast lookup.", "Assignment aliases; copying controls shared mutation."], ["Using a list for repeated membership.", "Confusing shallow with deep copying.", "Using unhashable keys."], quiz_for("data"), ["I can choose list/dict/set/tuple.", "I can explain aliasing.", "I can state typical operation costs."])
    write_notebook("01_Python_Data_Structures.ipynb", cells)


def notebook_02() -> None:
    cells = intro("02 — Functions, Classes, and Python Core", ["Design clear functions and small classes", "Avoid Python state and scope traps", "Stream large AI datasets lazily"], "3 hours", ["Functions", "Scope and first-class functions", "Classes and composition", "Typing and errors", "Generators", "Practice"], "Notebook 01")
    cells += [md("""
    ## Functions

    🔴 **Must Know**

    **Concept.** Functions package reusable behavior; parameters belong to the definition and arguments to the call.  
    **Why it matters.** AI pipelines are clearer when validation, preprocessing, retrieval, and scoring are small testable functions.  
    **Syntax.** `def name(required, default=..., *args, **kwargs): return value`.  
    **How Python executes it.** Calling creates a local frame; defaults were already evaluated when `def` executed.  
    **Complexity.** A function call is O(1) overhead plus the body’s work.  
    **Common interview mistake.** Forgetting that no explicit `return` means `None`.  
    **Interview question.** Parameters versus arguments? Names in a definition versus values supplied at a call.  
    **Exercise/solution.** Complete *keyword configuration* and *independent defaults* below.
    """), code("""
    def score(text: str, weight: float = 1.0, *features: float, **metadata: str) -> float:
        # Return a transparent toy score.
        print(metadata)
        return len(text) * weight + sum(features)

    print(score("rag", 0.5, 1.0, source="docs"))
    """), md("""
    ### 🔴 Mutable default argument trap

    `items=[]` is created once, so calls share state. Use `None`, then allocate inside. **Interview question:** When are default expressions evaluated? Once, at function definition time.
    """), code("""
    def bad_add(item, items=[]):
        items.append(item)
        return items

    def add_item(item, items=None):
        if items is None:
            items = []
        items.append(item)
        return items

    print(bad_add("a"), bad_add("b"))
    assert add_item("a") == ["a"] and add_item("b") == ["b"]
    """), md("""
    ## Scope and first-class functions

    🟠 **Important** — **Concept:** LEGB lookup order is Local → Enclosing → Global → Built-in, and functions are first-class objects. **Why it matters:** callbacks, sorting keys, decorators, and ML pipeline steps pass behavior around. **Syntax:** `nonlocal name`, `global name`, `apply(fn, value)`, and short `lambda x: ...`. **How Python executes it:** name lookup follows LEGB; closures retain enclosing references. **Complexity:** passing a function is O(1); calling it adds its body’s cost. **Common mistake:** rebinding an enclosing name without `nonlocal`. **Interview question:** when is `def` clearer than lambda? When logic needs a meaningful name or multiple steps. **Exercise/solution:** see *typed normalization*.
    """), code("""
    threshold = 0.8
    def make_filter(minimum):
        calls = 0
        def keep(prediction):
            nonlocal calls
            calls += 1
            return prediction["score"] >= minimum
        return keep

    def apply(fn, values):
        return [fn(value) for value in values]

    keep = make_filter(threshold)
    predictions = [{"label":"cat", "score":.9}, {"label":"dog", "score":.6}]
    print(list(filter(keep, predictions)))
    print(sorted(predictions, key=lambda item: item["score"], reverse=True))
    """), md("""
    ## Classes and composition

    🔴 **Must Know** — **Concept:** a class defines behavior; instances own state, while class variables are shared. **Why it matters:** model configuration and RAG services benefit from explicit interfaces and replaceable components. **Syntax:** `class`, `__init__`, `self`, methods, inheritance with `super()`, composition through constructor arguments, and `@dataclass`. **How Python executes it:** attribute lookup checks the instance and then its class hierarchy. **Complexity:** ordinary attribute lookup is average O(1); method bodies determine overall cost. **Common mistake:** placing a mutable list on the class when each instance needs its own list. **Interview question:** composition versus inheritance? Prefer composition for a *has-a* relationship. **Exercise/solution:** complete *dataclass validation*.
    """), code("""
    from dataclasses import dataclass, field

    class BaseModel:
        def __init__(self, name: str): self.name = name
        def predict(self, text: str) -> str: raise NotImplementedError

    class LLMModel(BaseModel):
        def __init__(self, name: str, temperature: float = 0.0):
            super().__init__(name)
            self.temperature = temperature
        def predict(self, text: str) -> str: return f"{self.name}: {text}"

    @dataclass
    class Chunk:
        text: str
        page: int
        source: str
        tags: list[str] = field(default_factory=list)  # new list per instance

    class RAGService:
        def __init__(self, retriever, llm):
            self.retriever, self.llm = retriever, llm
        def answer(self, question):
            context = self.retriever(question)
            return self.llm.predict(f"{context}: {question}")

    service = RAGService(lambda q: "retrieved context", LLMModel("toy"))
    print(service.answer("What is RAG?"), Chunk("hello", 1, "guide"))

    class BadRegistry:
        models = []  # shared by every instance: usually a bug

    first_bad = BadRegistry()
    second_bad = BadRegistry()
    first_bad.models.append("shared-model")
    assert second_bad.models == ["shared-model"]

    class ModelRegistry:
        def __init__(self):
            self.models = []  # independent per instance

    first_good, second_good = ModelRegistry(), ModelRegistry()
    first_good.models.append("private-model")
    assert second_good.models == []
    """), md("""
    ## Typing and errors

    🟠 **Important** — **Concept:** type hints document contracts; exceptions represent invalid operations; context managers own setup/cleanup. **Why it matters:** AI payloads, configurations, and preprocessing failures need readable contracts and actionable errors. **Syntax:** `str | None` (modern) or `Optional[str]`, `raise ValueError(...)`, `try/except/finally`, and `with`. **How Python executes it:** hints are normally not runtime enforcement; exceptions unwind until handled; `with` always calls its exit protocol. **Complexity:** annotations add no meaningful runtime cost by themselves. **Common mistake:** catching `Exception` and hiding unrelated bugs. **Interview question:** why catch specific exceptions? To handle only failures you understand. **Exercise/solution:** complete *safe division*.
    """), code("""
    from typing import Optional

    def find_user(user_id: int) -> str | None:
        return {1: "Alice"}.get(user_id)

    def find_user_legacy_spelling(user_id: int) -> Optional[str]:
        return {1: "Alice"}.get(user_id)

    def validate_chunk_size(chunk_size: int) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

    try:
        validate_chunk_size(0)
    except ValueError as error:
        print("validation:", error)
    finally:
        print("validation finished")

    from contextlib import nullcontext
    with nullcontext("inference resource") as resource:
        print(resource)
    """), md("""
    ### Context managers and basic decorators

    `with open("file.txt") as file:` closes the file even if reading raises. The same protocol supports database transactions and inference contexts. A decorator receives a function and returns a replacement; learn the basic idea, but do not prioritize advanced decorator internals.

    ```python
    def log_call(function):
        def wrapper(*args, **kwargs):
            print(function.__name__)
            return function(*args, **kwargs)
        return wrapper

    @log_call
    def embed(text): ...
    ```

    **Interview question:** Why is `with` safer than manually opening and closing? Cleanup is guaranteed through the context-manager protocol, including exceptional exits.

    ## Generators

    🟠 **Important** — **Concept:** an iterable can produce an iterator; an iterator tracks state; `yield` creates a generator that pauses between values. **Why it matters:** large AI datasets should be batched without materializing every batch. **Syntax:** `yield items[i:i+size]`. **How Python executes it:** a call returns a suspended generator; each `next` resumes until the next yield. **Complexity:** batching is O(n) total time and O(batch size) working space. **Common mistake:** returning a complete list and losing laziness. **Interview question:** generator versus list? Lazy one-pass production versus eager materialization. **Exercise/solution:** complete *lazy batches*.
    """), code("""
    def batches(items, batch_size):
        if batch_size <= 0: raise ValueError("batch_size must be positive")
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]

    batch_iterator = batches(list(range(7)), 3)
    print(iter(batch_iterator) is batch_iterator, list(batch_iterator))
    """), md("## Practice")]
    exs = [
        ("independent defaults", "Fix a tag collector so calls do not share a list.", "def add_tag(tag, tags=[]):\n    # TODO: fix signature and body\n    tags.append(tag)\n    return tags", "def add_tag(tag, tags=None):\n    if tags is None: tags = []\n    tags.append(tag)\n    return tags\nassert add_tag('a') == ['a'] and add_tag('b') == ['b']", "separate calls -> separate lists", "Use None.", "Allocate inside.", "Time O(1) amortized; Space O(1) per add", "Checking `if not tags` replaces an intentionally empty list."),
        ("keyword configuration", "Build a dict from required model plus keyword options.", "def model_config(model, **options):\n    # TODO: Write your solution here\n    pass", "def model_config(model, **options):\n    return {'model': model, **options}\nassert model_config('x', temperature=0) == {'model':'x','temperature':0}", "model_config('x', temperature=0) -> dict", "Use dict unpacking.", "Keyword arguments arrive as a dict.", "Time/Space O(k)", "Mutating options unexpectedly."),
        ("typed normalization", "Return lowercase stripped strings with a clear type hint.", "def normalize_texts(texts):\n    # TODO: add hints and implementation\n    pass", "def normalize_texts(texts: list[str]) -> list[str]:\n    return [text.strip().lower() for text in texts]\nassert normalize_texts([' A ']) == ['a']", "[' A '] -> ['a']", "Map strip and lower.", "Return a new list.", "Time O(total characters); Space O(total characters)", "Claiming O(n) without defining whether n is strings or characters."),
        ("safe division", "Raise ValueError when denominator is zero.", "def safe_divide(a, b):\n    # TODO: Write your solution here\n    pass", "def safe_divide(a: float, b: float) -> float:\n    if b == 0: raise ValueError('denominator must be nonzero')\n    return a / b\nassert safe_divide(6, 2) == 3", "6,2 -> 3", "Validate first.", "Raise rather than return an ambiguous sentinel.", "Time O(1); Space O(1)", "Catching every exception and hiding programming errors."),
        ("lazy batches", "Yield chunks and reject nonpositive size.", "def lazy_batches(items, size):\n    # TODO: Write your solution here\n    pass", "def lazy_batches(items, size):\n    if size <= 0: raise ValueError('size must be positive')\n    for i in range(0, len(items), size): yield items[i:i+size]\nassert list(lazy_batches([1,2,3],2)) == [[1,2],[3]]", "[1,2,3],2 -> [1,2], then [3]", "Use yield.", "Step range by size.", "Time O(n); extra Space O(size)", "Returning a complete list defeats laziness."),
        ("dataclass validation", "Create an immutable ModelConfig with name and temperature.", "# TODO: define ModelConfig", "from dataclasses import dataclass\n@dataclass(frozen=True)\nclass ModelConfig:\n    name: str\n    temperature: float = 0.0\nconfig = ModelConfig('demo')\nassert config.temperature == 0.0", "ModelConfig('demo')", "Use @dataclass(frozen=True).", "Provide a default.", "Time O(1); Space O(1)", "Using a mutable shared class attribute."),
    ]
    for e in exs: cells += exercise(*e)
    cells += footer(["Defaults are evaluated once.", "Composition keeps AI components replaceable.", "Generators stream work lazily."], ["Mutable defaults/class variables.", "Broad exception swallowing.", "Overusing inheritance or lambdas."], quiz_for("core"), ["I can explain LEGB.", "I can write a generator.", "I can model a service with composition."])
    write_notebook("02_Functions_Classes_and_Python_Core.ipynb", cells)


def notebook_03() -> None:
    cells = intro("03 — Comprehensions and `collections`", ["Write readable transformations", "Use Counter, defaultdict, and deque", "Apply standard-library interview tools"], "2.5 hours", ["Comprehensions", "Counter", "defaultdict", "deque and traversal", "Standard tools", "Practice"], "Notebooks 01–02")
    cells += [md("""
    ## Comprehensions

    🔴 **Must Know** — **Concept:** comprehensions build list/dict/set results; generator expressions produce values lazily. **Why it matters:** concise transformations are common in AI preprocessing and interview code. **Syntax:** `[expression for item in iterable if condition]`; inline `a if condition else b` chooses an output while a trailing `if` filters. **How Python executes it:** collection comprehensions eagerly add to a new container; generators suspend iteration. **Complexity:** one simple pass is O(n), with output-dependent space; generators use O(1) iteration state. **Common mistake:** nesting enough logic to hide intent. **Interview question:** filter versus conditional expression? A trailing `if` drops inputs; inline `if/else` chooses outputs. **Exercise/solution:** complete *filter predictions* and *invert unique mapping*.
    """), code("""
    nums = [-2, -1, 0, 1, 2]
    squares_loop = []
    for x in nums: squares_loop.append(x * x)
    squares = [x * x for x in nums]
    positives = [x for x in nums if x > 0]              # filter
    labels = ["positive" if x > 0 else "nonpositive" for x in nums]  # choose
    mapping = {x: x * x for x in range(4)}
    lengths = {len(word) for word in ["AI", "ML", "Python"]}
    lazy_squares = (x * x for x in nums)
    assert squares == squares_loop
    print(positives, labels, mapping, lengths, sum(lazy_squares))
    """), md("""
    **How Python executes it.** A list comprehension eagerly appends to a new list. A generator expression stores suspended iteration state and produces one item at a time.

    **Common interview mistake:** `[x if x > 0 for x in nums]` is invalid ordering. Keep comprehensions short; nested conditions with side effects deserve a named loop.
    """), code("""
    # Too dense: transformation, filter, and fallback policy are hard to explain.
    dense = [text.strip().lower() for text in [" AI ", "", " ML "] if text and text.strip()]

    # Interview-readable refactor when the policy grows.
    normalized = []
    for text in [" AI ", "", " ML "]:
        if not text or not text.strip():
            continue
        normalized.append(text.strip().lower())
    assert dense == normalized == ["ai", "ml"]
    """), md("""

    ## Counter

    🔴 **Must Know** — **Concept:** `Counter` is a dictionary subclass for frequencies. **Why it matters:** label balance, anagrams, and Top K start with counts. **Syntax:** `Counter(items)` and `most_common(k)`. **How Python executes it:** one pass updates a hash map. **Complexity:** construction O(n), storage O(k) unique items. **Common mistake:** indexing `most_common(1)[0]` on empty input. **Interview question:** Counter versus manual dict? Counter is concise; a dict demonstrates the underlying pattern. **Exercise/solution:** complete *top label*.
    """), code("""
    from collections import Counter
    labels = ["cat", "dog", "cat", "bird", "cat"]
    counts = Counter(labels)
    print(counts, counts.most_common(2))
    assert Counter("silent") == Counter("listen")
    """), md("""
    ## defaultdict

    🔴 **Must Know** — **Concept:** a missing key calls a zero-argument factory. **Why it matters:** `defaultdict(list)` makes document and anagram grouping concise. **Syntax:** `groups = defaultdict(list)`. **How Python executes it:** missing access calls `list()` and inserts the result. **Complexity:** average O(1) lookup/append plus stored output. **Common mistake:** reading a missing key inserts it. **Interview question:** what manual branch does it replace? `if key not in groups: groups[key]=[]`. **Exercise/solution:** complete *group lengths*.
    """), code("""
    from collections import defaultdict
    groups = defaultdict(list)
    for word in ["eat", "tea", "tan", "ate"]:
        groups[tuple(sorted(word))].append(word)
    print(list(groups.values()))
    """), md("""
    ## deque and traversal

    🔴 **Must Know** — **Concept:** a deque is a double-ended queue. **Why it matters:** BFS needs FIFO removal without list shifting. **Syntax:** `append`, `appendleft`, `pop`, `popleft`. **How Python executes it:** block-based storage supports both ends efficiently. **Complexity:** all four end operations O(1); `list.pop(0)` is O(n). **Common mistake:** mixing stack `pop()` and queue `popleft()` semantics. **Interview question:** why does a queue produce level order? Earlier-discovered nodes leave first. **Exercise/solution:** complete *moving window* and use the traversal reference in Notebook 07.

    ```text
    Stack: push ↓ [1, 2, 3] → pop gives 3
    Queue: 1 → 2 → 3         → popleft gives 1

    DFS: stack + pop()       BFS: deque + popleft()
    ```
    """), code("""
    from collections import deque
    queue = deque(["level-0"])
    queue.append("level-1")
    assert queue.popleft() == "level-0"
    stack = [1, 2, 3]
    assert stack.pop() == 3
    """), md("""
    ## Standard tools

    🟠 **Important**

    - `heapq`: min-heap; push/pop O(log n).
    - `bisect_left`: lower-bound insertion/search index in O(log n) search.
    - `enumerate`: pairs index and value; clearer than indexing when both are needed.
    - `zip`: walks iterables together and stops at the shortest.
    - `any` / `all`: short-circuit existential/universal checks.
    - `sorted`, `min`, `max` accept `key=`. Nested sequences sort lexicographically: first item, then second on ties.

    **Common interview mistake:** writing `for i in range(len(nums))` when only values are needed, or assigning the result of `.sort()`. **Interview question:** when choose `sorted`? When input ownership or type means it must remain unchanged. **Exercise/solution:** complete *lexicographic sort*.
    """), code("""
    import bisect, heapq
    names, scores = ["A", "B"], [.8, .9]
    for i in range(len(names)):  # valid, but noisier when index and value are both needed
        print(i, names[i])
    for i, name in enumerate(names):
        print(i, name)
    print(list(enumerate(names)), list(zip(names, scores)))
    records = [[2, 3], [1, 5], [2, 1]]
    records.sort()
    assert records == [[1, 5], [2, 1], [2, 3]]
    nums = [3, 1, 2]
    sorted_nums = sorted(nums)
    assert nums == [3, 1, 2] and sorted_nums == [1, 2, 3]
    nums.sort()
    assert nums == [1, 2, 3]
    best = max(zip(names, scores), key=lambda pair: pair[1])
    worst = min(zip(names, scores), key=lambda pair: pair[1])
    heap = []
    for value in [3, 1, 2]: heapq.heappush(heap, value)
    print(heapq.heappop(heap), bisect.bisect_left([1, 3, 5], 4), any(scores), all(s > 0 for s in scores), best, worst)
    """), md("## Practice")]
    exs = [
        ("filter predictions", "Keep predictions with score >= 0.8 using a comprehension.", "def high_confidence(predictions):\n    # TODO: Write your solution here\n    pass", "def high_confidence(predictions):\n    return [p for p in predictions if p['score'] >= .8]\nassert len(high_confidence([{'score':.9},{'score':.7}])) == 1", ".9,.7 -> .9 only", "Use a trailing if.", "Do not mutate inputs.", "Time O(n); Space O(n)", "Putting `if` before the `for`."),
        ("invert unique mapping", "Swap keys and unique values.", "def invert(mapping):\n    # TODO: Write your solution here\n    pass", "def invert(mapping):\n    return {value:key for key,value in mapping.items()}\nassert invert({'a':1}) == {1:'a'}", "{'a':1} -> {1:'a'}", "Dictionary comprehension.", "Iterate items.", "Time O(n); Space O(n)", "Duplicate values overwrite earlier keys."),
        ("top label", "Return the most frequent label or None.", "def top_label(labels):\n    # TODO: Write your solution here\n    pass", "from collections import Counter\ndef top_label(labels):\n    return Counter(labels).most_common(1)[0][0] if labels else None\nassert top_label(['a','b','a']) == 'a'", "['a','b','a'] -> 'a'", "Counter.most_common.", "Handle empty input.", "Time O(n); Space O(k)", "Indexing an empty `most_common` result."),
        ("group lengths", "Group words by length.", "def group_lengths(words):\n    # TODO: Write your solution here\n    pass", "from collections import defaultdict\ndef group_lengths(words):\n    groups=defaultdict(list)\n    for word in words: groups[len(word)].append(word)\n    return dict(groups)\nassert group_lengths(['a','bb'])[2] == ['bb']", "['a','bb'] -> {1:['a'],2:['bb']}", "defaultdict(list).", "Append per length.", "Time O(n); Space O(n)", "Reusing one list across groups."),
        ("moving window", "Return sums of every width-k window.", "def window_sums(nums, k):\n    # TODO: Write your solution here\n    pass", "from collections import deque\ndef window_sums(nums, k):\n    if k <= 0 or k > len(nums): return []\n    result=[]; current=sum(nums[:k]); result.append(current)\n    for i in range(k,len(nums)):\n        current += nums[i]-nums[i-k]; result.append(current)\n    return result\nassert window_sums([1,2,3,4],2)==[3,5,7]", "[1,2,3,4],2 -> [3,5,7]", "Update rather than resumming.", "Add entering, subtract leaving.", "Time O(n); Space O(n) output", "Recomputing every sum makes O(nk)."),
        ("lexicographic sort", "Sort `(label, score)` by descending score then label.", "def rank(items):\n    # TODO: Write your solution here\n    pass", "def rank(items):\n    return sorted(items, key=lambda x: (-x[1], x[0]))\nassert rank([('b',.9),('a',.9)]) == [('a',.9),('b',.9)]", "tie -> alphabetical", "Tuple sort key.", "Negate numeric descending component.", "Time O(n log n); Space O(n)", "Using reverse=True reverses both tie dimensions."),
    ]
    for e in exs: cells += exercise(*e)
    cells += footer(["Comprehensions should remain readable.", "Counter counts; defaultdict groups; deque queues.", "Sorting keys encode multiple priorities."], ["Using list.pop(0) for BFS.", "Forgetting generator exhaustion.", "Overly clever one-liners."], quiz_for("collections"), ["I can distinguish filter from conditional expression.", "I can group anagrams.", "I can select stack versus queue."])
    write_notebook("03_Comprehensions_and_Collections.ipynb", cells)


def notebook_04() -> None:
    cells = intro("04 — NumPy for AI Engineers", ["Manipulate arrays and shapes", "Explain broadcasting and axes", "Implement vectorized ML calculations"], "3–4 hours", ["Arrays and shapes", "Indexing and masking", "Vectorization and broadcasting", "Reshape and axes", "Linear algebra", "20 exercises"], "Python data structures; basic algebra")
    cells += [md("""
    ## Arrays and shapes

    🔴 **Must Know** — **Concept:** `ndarray` is a homogeneous n-dimensional numeric container. **Why it matters:** embeddings, batches, weights, and predictions depend on shape-correct vectorized computation. **Syntax:** `np.array`, `shape`, `ndim`, `size`, and `dtype`. **How NumPy executes it:** homogeneous buffers let compiled loops operate without per-element Python dispatch. **Complexity:** construction/copying is O(number of elements); metadata access is O(1). **Common mistake:** confusing `(n,)` with `(n,1)`. **Interview question:** list versus ndarray? Flexible reference collection versus homogeneous numerical tensor. **Exercise/solution:** begin with *vector norm* and *flatten images*.

    ```text
    [[1, 2, 3],     2 rows
     [4, 5, 6]]  ×  3 columns  → shape (2, 3), ndim 2, size 6
    ```
    """), code("""
    import numpy as np
    rng = np.random.default_rng(42)
    np.random.seed(42)
    x = np.array([[1, 2, 3], [4, 5, 6]])
    print(x.shape, x.ndim, x.size, x.dtype)
    print(np.zeros((2, 3)), np.ones(3), np.arange(0, 6, 2), np.linspace(0, 1, 5))
    normal_samples = rng.standard_normal((2, 3))  # reproducible replacement for legacy randn
    legacy_randn_example = np.random.randn(2, 3)  # explicitly requested legacy API
    print(normal_samples, legacy_randn_example)
    """), md("""
    ## Indexing and masking

    🔴 **Must Know** — **Concept:** indices and slices select positions; boolean masks select by condition. **Why it matters:** ML preprocessing often filters predictions or chooses feature columns. **Syntax:** `x[row,column]`, `x[:,0]`, `x[0,:]`, `x[x>0]`. **How NumPy executes it:** basic slices are usually views; advanced/boolean indexing usually copies. **Complexity:** scalar indexing O(1); selecting k outputs O(k). **Common mistake:** mutating a slice view unintentionally. **Interview question:** what does `x[:,0]` mean? Every row, first column. **Exercise/solution:** complete *filter predictions* and *top index per row*.
    """), code("""
    x = np.array([[1, 2, 3], [4, 5, 6]])
    print("first", x[0, 0], "column", x[:, 0], "row", x[0, :], "block", x[:2, 1:])
    scores = np.array([.2, .8, .95])
    print(scores[scores >= .5])
    """), md("""
    ## Vectorization and broadcasting

    🔴 **Must Know** — **Concept:** vectorization applies operations to whole arrays; broadcasting expands compatible size-1 dimensions conceptually. **Why it matters:** readable, efficient feature and batch operations avoid Python loops. **Syntax:** `arr*2`, `matrix+vector`. **How NumPy executes it:** compiled strided loops align shapes from the right without necessarily copying broadcast values. **Complexity:** O(number of result elements), with result-sized space. **Common mistake:** comparing only total element counts. **Interview question:** when are aligned dimensions compatible? Equal or one is 1. **Exercise/solution:** complete *standardize columns*, *center rows*, and *linear layer*.

    ```text
    matrix (3, 4)
          +    vector (4,)
          =    result (3, 4)

    (3, 4) + (3,)  ✗ trailing dimensions 4 and 3 conflict
    ```
    """), code("""
    matrix = np.arange(12).reshape(3, 4)
    feature_bias = np.array([10, 20, 30, 40])
    print(matrix + feature_bias)
    print(matrix * 2)  # vectorized scalar broadcast
    """), md("""
    **Common interview mistake:** guessing broadcast compatibility from total element count. Compare aligned dimensions from right to left.

    ## Reshape and axes

    🔴 **Must Know** — **Concept:** reshape changes dimensional interpretation while axes name dimensions reduced by aggregations. **Why it matters:** batch/image layouts and row/column statistics must preserve intended samples and features. **Syntax:** `reshape`, `ravel`, `flatten`, and `sum(axis=...)`. **How NumPy executes it:** reshape/ravel return views when strides permit; flatten copies; a reduction removes the selected axis. **Complexity:** view reshape O(1), flatten O(n), reductions O(n). **Common mistake:** saying axis=0 means “rows” without explaining that rows are collapsed. **Interview question:** axis=0 output? One aggregate per column. **Exercise/solution:** complete *column means* and *row max*.

    ```text
      1 2 3
      4 5 6
    axis=0 ↓ collapse rows → [5, 7, 9]  (one result per column)
    axis=1 → collapse cols → [6, 15]    (one result per row)
    ```
    """), code("""
    x = np.array([[1,2,3],[4,5,6]])
    print(x.reshape(3, 2), x.ravel(), x.flatten())
    print("sum0", x.sum(axis=0), "sum1", x.sum(axis=1))
    print(np.mean(x), np.std(x), np.min(x), np.max(x), np.argmax(x, axis=1))
    """), md("""
    ## Linear algebra

    🔴 **Must Know**

    **Concept.** Element-wise multiplication and matrix multiplication are distinct operations.  
    **Why it matters.** Neural layers use `X @ W + b`; embedding similarity uses dot products and norms.  
    **Syntax.** `A * B`, `A @ B`, `np.dot(a,b)`.  
    **How NumPy executes it.** Element-wise shapes broadcast; matrix multiplication contracts matching inner dimensions.  
    **Complexity.** Dense `(b,f) @ (f,o)` is O(bfo), output space O(bo).  
    **Common mistake.** Using `*` where `@` is required.  
    **Interview question.** What is the output of `(b,f) @ (f,o)`? `(b,o)`.  
    **Exercise/solution.** Complete *pairwise scores* and *cosine similarity*.

    ```text
    A * B → element-wise; shapes must broadcast
    A @ B → matrix multiplication; inner dimensions must match
    X (batch, features) @ W (features, outputs) + b (outputs,)
      → predictions (batch, outputs)
    ```

    Vector dot products measure weighted alignment and form the numerator of cosine similarity.
    """), code("""
    A = np.array([[1,2],[3,4]])
    B = np.array([[2,0],[1,2]])
    print("elementwise", A * B)
    print("matrix", A @ B)
    a, b = np.array([1., 2.]), np.array([3., 4.])
    cosine = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    print("dot", np.dot(a, b), "cosine", cosine)
    """), md("## 20 exercises")]
    numpy_specs = [
        ("vector_norm", "Return L2 norm.", "np.linalg.norm(x)", "np.isclose(vector_norm(np.array([3.,4.])),5)", "Time O(n); Space O(1)"),
        ("normalize_vector", "Return a unit vector; leave zero vector unchanged.", "x / norm if (norm := np.linalg.norm(x)) else x.copy()", "np.allclose(normalize_vector(np.array([3.,4.])),[.6,.8])", "Time O(n); Space O(n)"),
        ("standardize_columns", "Z-score each column.", "(x - x.mean(axis=0)) / x.std(axis=0)", "np.allclose(standardize_columns(np.array([[1.,2.],[3.,4.]])).mean(0),0)", "Time O(rc); Space O(rc)"),
        ("row_max", "Return maximum per row.", "x.max(axis=1)", "np.array_equal(row_max(np.array([[1,3],[4,2]])),[3,4])", "Time O(rc); Space O(r)"),
        ("cosine_similarity", "Compute cosine similarity, rejecting zero norms.", "np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)) if np.linalg.norm(a)*np.linalg.norm(b) else 0.0", "np.isclose(cosine_similarity(np.array([1.,0.]),np.array([1.,0.])),1)", "Time O(n); Space O(1)"),
        ("flatten_images", "Flatten `(batch,height,width)` to `(batch,-1)`.", "images.reshape(images.shape[0], -1)", "flatten_images(np.zeros((2,3,4))).shape==(2,12)", "Time O(1) view; Space O(1) when possible"),
        ("filter_predictions", "Keep scores at least threshold.", "scores[scores >= threshold]", "np.array_equal(filter_predictions(np.array([.2,.8]),.5),[.8])", "Time O(n); Space O(n)"),
        ("linear_layer", "Compute X @ W + b.", "X @ W + b", "linear_layer(np.ones((2,3)),np.ones((3,1)),np.array([1])).shape==(2,1)", "Time O(bfo); Space O(bo)"),
        ("one_hot", "One-hot encode integer labels.", "np.eye(num_classes, dtype=int)[labels]", "np.array_equal(one_hot(np.array([0,2]),3),[[1,0,0],[0,0,1]])", "Time/Space O(nc)"),
        ("column_means", "Return column means.", "x.mean(axis=0)", "np.array_equal(column_means(np.array([[1,2],[3,4]])),[2,3])", "Time O(rc); Space O(c)"),
        ("row_softmax", "Stable softmax over each row.", "None", "np.allclose(row_softmax(np.array([[1.,2.]]).copy()).sum(1),1)", "Time/Space O(rc)"),
        ("clip_scores", "Clip values to [0,1].", "np.clip(x, 0, 1)", "np.array_equal(clip_scores(np.array([-1,.5,2])),[0,.5,1])", "Time/Space O(n)"),
        ("replace_nan", "Replace NaN with column means.", "np.where(np.isnan(x), np.nanmean(x,axis=0), x)", "not np.isnan(replace_nan(np.array([[1.,np.nan],[3.,2.]]))).any()", "Time/Space O(rc)"),
        ("top_index_per_row", "Return argmax per row.", "x.argmax(axis=1)", "np.array_equal(top_index_per_row(np.array([[1,2],[3,0]])),[1,0])", "Time O(rc); Space O(r)"),
        ("pairwise_scores", "Compute X @ Y.T.", "X @ Y.T", "pairwise_scores(np.ones((2,3)),np.ones((4,3))).shape==(2,4)", "Time O(nmd); Space O(nm)"),
        ("center_rows", "Subtract each row mean.", "x - x.mean(axis=1,keepdims=True)", "np.allclose(center_rows(np.array([[1.,3.]])).mean(1),0)", "Time/Space O(rc)"),
        ("batch_indices", "Return shuffled indices from a seeded RNG.", "np.random.default_rng(seed).permutation(n)", "np.array_equal(batch_indices(4,42),batch_indices(4,42))", "Time/Space O(n)"),
        ("accuracy", "Compute fraction of equal labels.", "np.mean(y_true == y_pred)", "np.isclose(accuracy(np.array([1,0]),np.array([1,1])),.5)", "Time O(n); Space O(n)"),
        ("confusion_counts", "Build a class-by-class count matrix.", "None", "np.array_equal(confusion_counts(np.array([0,1]),np.array([0,1]),2),np.eye(2,dtype=int))", "Time O(n); Space O(c²)"),
        ("minmax_columns", "Scale columns to [0,1], guarding constant columns.", "None", "np.allclose(minmax_columns(np.array([[1.,2.],[3.,2.]]))[:,0],[0,1])", "Time/Space O(rc)"),
    ]
    numpy_mistakes = {
        "vector_norm":"Forgetting the square root by returning the sum of squares.", "normalize_vector":"Dividing a zero vector by zero.",
        "standardize_columns":"Using a global mean/std instead of axis=0.", "row_max":"Reducing axis=0 and returning column maxima.",
        "cosine_similarity":"Omitting either vector norm from the denominator.", "flatten_images":"Flattening the batch dimension together with pixels.",
        "filter_predictions":"Using `>` when the threshold is inclusive.", "linear_layer":"Using element-wise `*` instead of matrix `@`.",
        "one_hot":"Using a class count smaller than the largest label plus one.", "column_means":"Reducing axis=1.",
        "row_softmax":"Exponentiating unshifted large logits and overflowing.", "clip_scores":"Mutating the input when a new result is expected.",
        "replace_nan":"Taking one global mean instead of a mean per column.", "top_index_per_row":"Returning maximum values rather than their indices.",
        "pairwise_scores":"Forgetting to transpose Y.", "center_rows":"Dropping `keepdims=True` and breaking broadcasting.",
        "batch_indices":"Using an unseeded global RNG and losing reproducibility.", "accuracy":"Using Python `and` instead of element-wise equality.",
        "confusion_counts":"Overwriting repeated class pairs instead of accumulating them.", "minmax_columns":"Dividing constant columns by zero.",
    }
    for i, (name, goal, expr, test, comp) in enumerate(numpy_specs, 1):
        args = {
            "vector_norm":"x", "normalize_vector":"x", "standardize_columns":"x", "row_max":"x", "cosine_similarity":"a, b", "flatten_images":"images", "filter_predictions":"scores, threshold", "linear_layer":"X, W, b", "one_hot":"labels, num_classes", "column_means":"x", "row_softmax":"x", "clip_scores":"x", "replace_nan":"x", "top_index_per_row":"x", "pairwise_scores":"X, Y", "center_rows":"x", "batch_indices":"n, seed", "accuracy":"y_true, y_pred", "confusion_counts":"y_true, y_pred, classes", "minmax_columns":"x"
        }[name]
        starter = f"def {name}({args}):\n    # TODO: Write your NumPy solution here\n    pass"
        if name == "row_softmax":
            solution = "def row_softmax(x):\n    shifted = x - x.max(axis=1, keepdims=True)\n    exponentials = np.exp(shifted)\n    return exponentials / exponentials.sum(axis=1, keepdims=True)"
        elif name == "confusion_counts":
            solution = "def confusion_counts(y_true, y_pred, classes):\n    counts = np.zeros((classes, classes), dtype=int)\n    np.add.at(counts, (y_true, y_pred), 1)\n    return counts"
        elif name == "minmax_columns":
            solution = "def minmax_columns(x):\n    minimum = x.min(axis=0)\n    span = x.max(axis=0) - minimum\n    safe_span = np.where(span == 0, 1, span)\n    return (x - minimum) / safe_span"
        else:
            solution = f"def {name}({args}):\n    return {expr}"
        solution += f"\n\nassert {test}"
        cells += exercise(f"{i}. {name}", goal, starter, solution, "See assertion in solution", "Identify the output shape.", "Use an axis-aware vectorized operation.", comp, numpy_mistakes[name], "🟠 Medium" if i > 8 else "🟢 Easy")
    cells += footer(["Shapes are part of the algorithm.", "Broadcasting aligns from the right.", "`*` and `@` mean different operations."], ["Reducing the wrong axis.", "Dividing by zero norms.", "Accidentally mutating through a view."], quiz_for("numpy"), ["I can predict shapes.", "I can normalize rows/columns.", "I can explain X @ W + b."])
    write_notebook("04_NumPy_for_AI_Engineers.ipynb", cells)


def notebook_05() -> None:
    cells = intro("05 — pandas for AI Engineers", ["Inspect and clean tabular data", "Filter, aggregate, and join", "Avoid preprocessing leakage"], "3–4 hours", ["DataFrame basics", "Selection and filtering", "Missing data", "GroupBy and merge", "Vectorization and features", "20 exercises", "ML mini-project"], "Notebook 04; basic tabular concepts")
    cells += [md("""
    ## DataFrame basics

    🔴 **Must Know** — **Concept:** a DataFrame is a labeled 2D table. **Why it matters:** AI interviews test rapid inspection and safe preprocessing. **Syntax:** `head`, `shape`, `columns`, `dtypes`, `info`, `describe`. **How pandas executes it:** columns are aligned labeled arrays that may use different dtypes. **Complexity:** metadata access is small/O(1); summaries scan relevant values. **Common mistake:** transforming before inspecting schema and missingness. **Interview question:** Series versus DataFrame? One labeled dimension versus two. **Exercise/solution:** complete *select features* and *missing counts*.
    """), code("""
    import numpy as np
    import pandas as pd
    df = pd.DataFrame({
        "user_id": [1,2,3,4,4], "age": [25,np.nan,40,35,35],
        "country": ["SG","US","SG","MY","MY"], "salary": [60,80,100,70,70],
        "label": [0,1,1,0,0], "date": ["2026-01-01","2026-01-02","2026-02-01","2026-02-02","2026-02-02"]
    })
    print(df.head(), df.shape, list(df.columns), df.dtypes)
    df.info()
    print(df.select_dtypes("number").describe())
    """), md("""
    ## Selection and filtering

    🔴 **Must Know** — **Concept:** column selection chooses labels; `loc` uses labels and `iloc` positions; masks filter rows. **Why it matters:** feature selection and cohort analysis are everyday ML tasks. **Syntax:** `df['age']`, `df[['age','salary']]`, `.loc`, `.iloc`, and parenthesized masks. **How pandas executes it:** labels align operations; a boolean Series chooses matching rows. **Complexity:** filtering scans O(n) rows and produces output-sized storage. **Common mistake:** omitting parentheses around comparisons joined by `&`/`|`. **Interview question:** `loc` versus `iloc`? Label-based/inclusive label slices versus position-based/exclusive positional slices. **Exercise/solution:** complete *filter adults*, *SG high salary*, and *query IDs*.
    """), code("""
    print(df["age"])
    print(df[["age", "salary"]])
    print(df.loc[df["country"].eq("SG"), ["user_id", "salary"]])
    print(df.iloc[:2, :3])
    subset = df[(df["age"] > 30) & (df["country"] == "SG")]
    print(subset)
    """), md("""
    ## Missing data

    🔴 **Must Know** — **Concept:** missing values require explicit detection and a domain-appropriate policy. **Why it matters:** careless imputation can bias models or leak evaluation data. **Syntax:** `isna`, `dropna`, `fillna`; mean/median/mode/domain sentinel. **How pandas executes it:** masks identify missing markers and methods return transformed frames unless `inplace` is requested. **Complexity:** detection/filling scans O(nc) cells. **Common mistake:** fitting imputation statistics on validation/test data. **Interview question:** why use a training median? Robustness and leakage prevention. **Exercise/solution:** complete *fill age*.
    """), code("""
    print(df.isna().sum())
    train_age_median = df["age"].median()
    filled = df.assign(age=df["age"].fillna(train_age_median))
    print(filled.dropna(), train_age_median)
    """), md("""
    ## GroupBy and merge

    🔴 **Must Know** — **Concept:** GroupBy is split → apply → combine; merge is SQL-style key alignment. **Why it matters:** ML datasets often combine metadata and predictions then summarize cohorts. **Syntax:** `groupby(...).agg(...)` and `pd.merge(..., how='left')`. **How pandas executes it:** grouping hashes/sorts keys; merge builds key matches and can multiply rows. **Complexity:** usually O(n) average grouping and O(n+m) average hash joins, with output-dependent space. **Common mistake:** ignoring duplicate-key cardinality; use `validate=`. **Interview question:** what does a left join preserve? Every left row. **Exercise/solution:** complete *country summary* and *left join predictions*.

    ```text
    LEFT JOIN on user_id
    users:       1 A      predictions: 1 .9      result: 1 A .9
                 2 B                   3 .7              2 B NaN
    ```
    """), code("""
    summary = df.groupby("country").agg(mean_salary=("salary","mean"), users=("salary","count"))
    predictions = pd.DataFrame({"user_id":[1,3], "score":[.9,.7]})
    joined = pd.merge(df, predictions, on="user_id", how="left", validate="many_to_one")
    print(summary, joined)
    """), md("""
    ## Vectorization and features

    🟠 **Important** — **Concept:** vectorized column, string, and datetime operations transform whole Series. **Why it matters:** efficient feature engineering includes class balance, duplicate control, and temporal features. **Syntax:** arithmetic columns, `value_counts`, `drop_duplicates`, `pd.to_datetime`, `.dt`. **How pandas executes it:** vectorized kernels operate over arrays; `apply` invokes a callable per element/row and remains appropriate for irreducible custom logic. **Complexity:** most transformations scan O(n); sorting/deduplication may add hashing or O(n log n) sorting. **Common mistake:** saying `apply` is always bad or parsing dates after using `.dt`. **Interview question:** why inspect duplicates before splitting? The same record can leak across train/test. **Exercise/solution:** complete *label distribution*, *unique users*, and *parse month*.
    """), code("""
    featured = df.assign(
        salary_adjusted=df["salary"] * 1.1,
        date=pd.to_datetime(df["date"]),
    ).drop_duplicates()
    featured["year"] = featured["date"].dt.year
    featured["month"] = featured["date"].dt.month
    featured["dayofweek"] = featured["date"].dt.dayofweek
    print(df["label"].value_counts(), df["label"].value_counts(normalize=True))
    print(featured.sort_values("salary", ascending=False))
    """), md("## 20 exercises")]
    specs = [
        ("select_features", "Return age and salary columns.", "df[['age','salary']]", "list(select_features(pd.DataFrame({'age':[1],'salary':[2]})).columns)==['age','salary']"),
        ("filter_adults", "Keep age >= 18.", "df.loc[df['age'] >= 18].copy()", "len(filter_adults(pd.DataFrame({'age':[17,18]})))==1"),
        ("sg_high_salary", "Keep SG rows with salary > threshold.", "df.loc[(df['country']=='SG') & (df['salary']>threshold)].copy()", "len(sg_high_salary(pd.DataFrame({'country':['SG','US'],'salary':[10,20]}),5))==1"),
        ("missing_counts", "Count missing values per column.", "df.isna().sum()", "missing_counts(pd.DataFrame({'x':[1,np.nan]}))['x']==1"),
        ("fill_age", "Fill age with supplied training median.", "df.assign(age=df['age'].fillna(train_median))", "fill_age(pd.DataFrame({'age':[np.nan]}),20)['age'].iloc[0]==20"),
        ("drop_exact_duplicates", "Remove duplicate rows.", "df.drop_duplicates().reset_index(drop=True)", "len(drop_exact_duplicates(pd.DataFrame({'x':[1,1]})))==1"),
        ("label_distribution", "Return normalized label frequencies.", "df['label'].value_counts(normalize=True)", "np.isclose(label_distribution(pd.DataFrame({'label':[1,1,0]})).loc[1],2/3)"),
        ("country_salary", "Mean salary by country.", "df.groupby('country')['salary'].mean()", "country_salary(pd.DataFrame({'country':['a','a'],'salary':[1,3]})).loc['a']==2"),
        ("country_summary", "Return mean salary and row count.", "df.groupby('country').agg(mean_salary=('salary','mean'), rows=('salary','size'))", "country_summary(pd.DataFrame({'country':['a'],'salary':[2]})).loc['a','rows']==1"),
        ("left_join_predictions", "Left join predictions on user_id.", "df.merge(predictions,on='user_id',how='left',validate='many_to_one')", "len(left_join_predictions(pd.DataFrame({'user_id':[1,2]}),pd.DataFrame({'user_id':[1],'score':[.9]})))==2"),
        ("rank_scores", "Sort descending by score.", "df.sort_values('score',ascending=False).reset_index(drop=True)", "rank_scores(pd.DataFrame({'score':[.1,.9]}))['score'].iloc[0]==.9"),
        ("add_margin", "Create margin = top1 - top2.", "df.assign(margin=df['top1']-df['top2'])", "add_margin(pd.DataFrame({'top1':[.9],'top2':[.7]}))['margin'].iloc[0] > .19"),
        ("parse_month", "Parse date and add month.", "df.assign(month=pd.to_datetime(df['date']).dt.month)", "parse_month(pd.DataFrame({'date':['2026-02-01']}))['month'].iloc[0]==2"),
        ("unique_users", "Keep latest row per user by date.", "df.assign(date=pd.to_datetime(df['date'])).sort_values('date').drop_duplicates('user_id',keep='last')", "len(unique_users(pd.DataFrame({'user_id':[1,1],'date':['2026-01-01','2026-02-01']})))==1"),
        ("class_counts", "Count labels including missing.", "df['label'].value_counts(dropna=False)", "class_counts(pd.DataFrame({'label':[1,np.nan]})).sum()==2"),
        ("rename_target", "Rename label to target without mutating input.", "df.rename(columns={'label':'target'})", "'target' in rename_target(pd.DataFrame({'label':[1]}))"),
        ("query_ids", "Return IDs whose score meets threshold.", "df.loc[df['score']>=threshold,'user_id'].tolist()", "query_ids(pd.DataFrame({'user_id':[1],'score':[.9]}),.8)==[1]"),
        ("pivot_metrics", "Pivot mean score by model and split.", "df.pivot_table(index='model',columns='split',values='score',aggfunc='mean')", "pivot_metrics(pd.DataFrame({'model':['a'],'split':['test'],'score':[.5]})).loc['a','test']==.5"),
        ("string_normalize", "Strip and lowercase a text column.", "df.assign(text=df['text'].str.strip().str.lower())", "string_normalize(pd.DataFrame({'text':[' A ']}))['text'].iloc[0]=='a'"),
        ("safe_export", "Return CSV text without the index.", "df.to_csv(index=False)", "not safe_export(pd.DataFrame({'x':[1]})).startswith(',')"),
    ]
    argmap = {"select_features":"df","filter_adults":"df","sg_high_salary":"df, threshold","missing_counts":"df","fill_age":"df, train_median","drop_exact_duplicates":"df","label_distribution":"df","country_salary":"df","country_summary":"df","left_join_predictions":"df, predictions","rank_scores":"df","add_margin":"df","parse_month":"df","unique_users":"df","class_counts":"df","rename_target":"df","query_ids":"df, threshold","pivot_metrics":"df","string_normalize":"df","safe_export":"df"}
    pandas_complexity = {
        "select_features":"Time O(n); Space O(n) for the returned frame", "filter_adults":"Time O(n); Space O(n) output",
        "sg_high_salary":"Time O(n); Space O(n) output", "missing_counts":"Time O(nc); Space O(c)",
        "fill_age":"Time O(n); Space O(n)", "drop_exact_duplicates":"Time O(n) average; Space O(n)",
        "label_distribution":"Time O(n) average; Space O(k)", "country_salary":"Time O(n) average; Space O(k)",
        "country_summary":"Time O(n) average; Space O(k)", "left_join_predictions":"Time O(n+m) average; Space O(n+m)",
        "rank_scores":"Time O(n log n); Space O(n)", "add_margin":"Time O(n); Space O(n)",
        "parse_month":"Time O(n); Space O(n)", "unique_users":"Time O(n log n); Space O(n)",
        "class_counts":"Time O(n) average; Space O(k)", "rename_target":"Time O(c); Space O(nc) for the returned frame",
        "query_ids":"Time O(n); Space O(n) output", "pivot_metrics":"Time O(n) average; Space O(models × splits)",
        "string_normalize":"Time O(total characters); Space O(total characters)", "safe_export":"Time O(nc); Space O(output CSV)",
    }
    pandas_mistakes = {
        "select_features":"Using one bracket returns a Series when a DataFrame is required.", "filter_adults":"Using `>` accidentally excludes age 18.",
        "sg_high_salary":"Omitting parentheses around each boolean condition.", "missing_counts":"Calling `sum()` before `isna()`.",
        "fill_age":"Computing the median from validation or test data.", "drop_exact_duplicates":"Mutating the caller when a returned clean frame is expected.",
        "label_distribution":"Forgetting `normalize=True`.", "country_salary":"Aggregating the wrong numeric column.",
        "country_summary":"Using `count` when missing salaries must still count as rows; use `size`.", "left_join_predictions":"Allowing duplicate right keys to multiply rows silently.",
        "rank_scores":"Leaving `ascending=True`.", "add_margin":"Subtracting in the wrong direction.",
        "parse_month":"Using `.dt` before converting to datetime.", "unique_users":"Dropping duplicates before sorting chronologically.",
        "class_counts":"Dropping missing labels unintentionally.", "rename_target":"Using `inplace=True` and unexpectedly mutating shared data.",
        "query_ids":"Returning the Series index instead of `user_id` values.", "pivot_metrics":"Assuming every model/split pair is unique without an aggregation.",
        "string_normalize":"Calling Python string methods directly on a Series.", "safe_export":"Writing the DataFrame index as an unintended first column.",
    }
    for i, (name, goal, expr, test) in enumerate(specs, 1):
        args = argmap[name]
        cells += exercise(f"{i}. {name}", goal, f"def {name}({args}):\n    # TODO: Write your pandas solution here\n    pass", f"def {name}({args}):\n    return {expr}\n\nassert {test}", "See assertion in solution", "Write the row mask or column operation first.", "Return a new object when practical.", pandas_complexity[name], pandas_mistakes[name], "🟠 Medium" if i > 8 else "🟢 Easy")
    cells += [md("""
    ## ML mini-project

    Complete before revealing: inspect shape; count missing; remove duplicates; fill age with the **training** median; inspect target distribution; filter SG users; aggregate salary; join predictions; create age bucket; produce CSV text.
    """), code("""
    # TODO: build `clean_ml_data` from `df` and `predictions`
    clean_ml_data = None
    """), md("### Mini-project solution"), code("""
    print("shape", df.shape)
    print("missing", df.isna().sum().to_dict())
    clean_ml_data = df.drop_duplicates().copy()
    training_median = clean_ml_data["age"].median()
    clean_ml_data["age"] = clean_ml_data["age"].fillna(training_median)
    print("target", clean_ml_data["label"].value_counts(normalize=True).to_dict())
    print("SG", clean_ml_data.loc[clean_ml_data["country"].eq("SG")])
    print(clean_ml_data.groupby("country")["salary"].mean())
    clean_ml_data = clean_ml_data.merge(predictions, on="user_id", how="left", validate="one_to_one")
    clean_ml_data["age_bucket"] = pd.cut(clean_ml_data["age"], bins=[0,29,39,np.inf], labels=["20s","30s","40+"])
    csv_text = clean_ml_data.to_csv(index=False)
    assert not clean_ml_data["age"].isna().any() and csv_text.startswith("user_id")
    """)]
    cells += footer(["Inspect before transforming.", "Fit preprocessing only on training data.", "Validate merge cardinality."], ["Missing parentheses in filters.", "Chained assignment.", "Silent many-to-many row explosion."], quiz_for("pandas"), ["I can explain loc vs iloc.", "I can group and merge.", "I can prevent preprocessing leakage."])
    write_notebook("05_Pandas_for_AI_Engineers.ipynb", cells)


def notebook_06() -> None:
    cells = intro("06 — Clean Python and Interview Patterns", ["Write code that is easy to explain", "Analyze complexity accurately", "Debug common live-coding failures"], "3 hours", ["Readable design", "Edge cases", "Complexity", "Bug clinic", "22 fundamentals drills"], "Notebooks 01–03")
    cells += [md("""
    ## Readable design

    🔴 **Must Know** — **Concept:** readable code uses descriptive names, focused functions, early returns, and named intermediate values. **Why it matters:** interviewers must follow both the algorithm and your explanation. **Syntax/example:** prefer `frequency`/`results`, guard with `if not input: return`, and compute an anagram key once. **How Python executes it:** naming does not change asymptotic behavior, but avoiding repeated expressions can. **Complexity:** analyze the refactored operations, not line count. **Common mistake:** compressing logic into a one-liner that hides mutation or edge cases. **Interview question:** why split a 50-line preprocessing function? Independent validation, normalization, and aggregation become testable. **Exercise/solution:** complete the 22 drills below.
    """), code("""
    from collections import defaultdict

    def group_anagrams(words: list[str]) -> list[list[str]]:
        if not words:                         # early return / edge case
            return []
        groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
        for word in words:
            key = tuple(sorted(word))         # compute once; immutable key
            groups[key].append(word)
        return list(groups.values())

    assert group_anagrams([]) == []
    grouped = group_anagrams(["eat", "tea"])
    assert len(grouped) == 1 and set(grouped[0]) == {"eat", "tea"}

    def validate_predictions(predictions):
        if predictions is None:
            raise ValueError("predictions must not be None")

    def filter_predictions(predictions, threshold):
        return [item for item in predictions if item["score"] >= threshold]

    def prepare_predictions(predictions, threshold):
        validate_predictions(predictions)
        return filter_predictions(predictions, threshold)
    """), md("""
    ## Edge cases

    **Concept.** Edge cases define behavior at the boundaries of the input domain.  
    **Why it matters.** Hidden interview tests target empty input, one element, duplicates, negative values, `None`, large input, order requirements, and malformed data.  
    **Syntax/example.** Guard clauses and assertions make assumptions explicit.  
    **How Python executes it.** Early returns skip the main algorithm when the contract permits.  
    **Complexity.** A constant-time guard does not change the main asymptotic cost.  
    **Common mistake.** Silently inventing behavior instead of clarifying it.  
    **Interview question.** Which four tests should you write first? Normal, empty, duplicate, boundary.  
    **Exercise/solution.** Every drill includes a starter and tested solution.

    A lightweight test matrix should cover normal, empty, duplicate, and boundary cases.
    """), code("""
    def contains_duplicate(nums):
        seen = set()
        for num in nums:
            if num in seen: return True
            seen.add(num)
        return False

    def run_tests():
        assert contains_duplicate([1,2,1]) is True   # normal/duplicate
        assert contains_duplicate([]) is False       # empty
        assert contains_duplicate([1]) is False      # boundary
        assert contains_duplicate([-1,-1]) is True   # negative
    run_tests()
    """), md("""
    ## Complexity

    🔴 **Must Know** — **Concept:** complexity describes growth of work and storage. **Why it matters:** interview solutions are evaluated against input scale. **Syntax:** state `Time: O(...)` and `Space: O(...)`, defining variables. **How Python executes it:** built-in costs compose—one scan with average O(1) set operations is O(n); nested pairs O(n²); sorting O(n log n). **Common mistake:** ignoring an internal sort or counting required output as auxiliary space without saying so. **Interview question:** average dict lookup? O(1), worst case O(n). **Exercise/solution:** each drill now states exact time and space.

    | Operation | Typical complexity |
    |---|---:|
    | list index / append | O(1) / amortized O(1) |
    | list membership / sort | O(n) / O(n log n) |
    | dict or set lookup | average O(1) |
    | deque append/popleft | O(1) |
    | heap push/pop | O(log n) |
    """), md("""
    ## Bug clinic

    🔴 **Must Know** — **Concept:** debugging traces state, invariants, and boundary transitions. **Why it matters:** live coding often includes correcting partially working code. **Syntax/example:** print or inspect `left`, `right`, keys, shapes, and return state on a minimal failing input. **How Python executes it:** mutation during iteration shifts subsequent positions; identity and equality call different semantics. **Complexity:** a fix should preserve or improve the target bounds. **Common mistake:** patching symptoms without a failing test. **Interview question:** what is the fastest debugging starting point? A minimal reproducible failing case. **Exercise/solution:** complete the ten timed debugging cases in Notebook 08.

    - Infinite pointer loop: move `left += 1` and `right -= 1` on every relevant branch.
    - Wrong endpoint: `range(2, len(nums))` includes the final index; `range` stops before its endpoint.
    - Wrong return variable: trace which variable holds the final state.
    - Mutable defaults: replace `[]` with `None` plus allocation.
    - Modifying while iterating: iterate over a copy or build a new list.
    - `==` compares values; `is` compares identity. Use `x is None`.
    - Check off-by-one bounds, dictionary key types, and duplicate behavior.
    - Truthiness: `None`, `False`, `0`, `''`, `[]`, `{}` are false-like; `if not nums` is idiomatic when all false-like values mean empty/absent.
    """), code("""
    a = [1, 2]
    b = [1, 2]
    assert a == b and a is not b
    value = None
    assert value is None
    """), md("## 22 fundamentals drills")]
    drills = [
        ("safe_first", "Return first item or None.", "items[0] if items else None", "safe_first([]) is None"),
        ("last_index", "Return final index or -1.", "len(items)-1 if items else -1", "last_index([1,2])==1"),
        ("count_truthy", "Count truthy values.", "sum(bool(x) for x in items)", "count_truthy([0,1,'',2])==2"),
        ("equal_values", "Compare values, not identities.", "a == b", "equal_values([1],[1]) is True"),
        ("copy_append", "Append to a shallow copy.", "items.copy() + [value]", "copy_append([1],2)==[1,2]"),
        ("frequency_map", "Build a frequency dictionary.", "None", "frequency_map(['a','a'])=={'a':2}"),
        ("unique_count", "Count unique hashable values.", "len(set(items))", "unique_count([1,1,2])==2"),
        ("pair_items", "Pair equal-length sequences.", "list(zip(left,right,strict=True))", "pair_items([1],[2])==[(1,2)]"),
        ("indexed", "Return `(index,value)` pairs.", "list(enumerate(items))", "indexed(['a'])==[(0,'a')]"),
        ("sorted_copy", "Return sorted data without mutation.", "sorted(items)", "sorted_copy([2,1])==[1,2]"),
        ("descending", "Sort descending.", "sorted(items,reverse=True)", "descending([1,2])==[2,1]"),
        ("key_with_max", "Return key with max value or None.", "max(mapping,key=mapping.get) if mapping else None", "key_with_max({'a':1,'b':2})=='b'"),
        ("all_positive", "Test whether every number is positive.", "all(x>0 for x in nums)", "all_positive([1,2]) is True"),
        ("any_missing", "Test whether any value is None.", "any(x is None for x in items)", "any_missing([1,None]) is True"),
        ("merge_options", "Merge defaults with overrides.", "{**defaults, **overrides}", "merge_options({'a':1},{'a':2})=={'a':2}"),
        ("safe_get", "Read a missing key with default.", "mapping.get(key, default)", "safe_get({},'x',0)==0"),
        ("immutable_key", "Convert an iterable to tuple.", "tuple(items)", "immutable_key([1,2])==(1,2)"),
        ("remove_none", "Return values that are not None.", "[x for x in items if x is not None]", "remove_none([0,None])==[0]"),
        ("clamp", "Clamp value to inclusive bounds.", "max(low,min(value,high))", "clamp(10,0,5)==5"),
        ("chunk_count", "Return ceiling number of batches.", "(n+size-1)//size if size>0 else 0", "chunk_count(5,2)==3"),
        ("palindrome", "Compare normalized text to reverse.", "(clean := ''.join(c.lower() for c in text if c.isalnum())) == clean[::-1]", "palindrome('A man, a plan, a canal: Panama')"),
        ("validate_nonempty", "Raise ValueError for empty string; return text otherwise.", "None", "validate_nonempty('x')=='x'"),
    ]
    argmap = {
        "safe_first":"items","last_index":"items","count_truthy":"items","equal_values":"a, b","copy_append":"items, value","frequency_map":"items","unique_count":"items","pair_items":"left, right","indexed":"items","sorted_copy":"items","descending":"items","key_with_max":"mapping","all_positive":"nums","any_missing":"items","merge_options":"defaults, overrides","safe_get":"mapping, key, default","immutable_key":"items","remove_none":"items","clamp":"value, low, high","chunk_count":"n, size","palindrome":"text","validate_nonempty":"text"
    }
    drill_complexity = {
        "safe_first":"Time O(1); Space O(1)", "last_index":"Time O(1); Space O(1)",
        "count_truthy":"Time O(n); Space O(1)", "equal_values":"Time O(n) worst case; Space O(1)",
        "copy_append":"Time O(n); Space O(n)", "frequency_map":"Time O(n) average; Space O(k)",
        "unique_count":"Time O(n) average; Space O(k)", "pair_items":"Time O(n); Space O(n)",
        "indexed":"Time O(n); Space O(n)", "sorted_copy":"Time O(n log n); Space O(n)",
        "descending":"Time O(n log n); Space O(n)", "key_with_max":"Time O(n); Space O(1)",
        "all_positive":"Time O(n); Space O(1)", "any_missing":"Time O(n); Space O(1)",
        "merge_options":"Time O(n+m); Space O(n+m)", "safe_get":"Time O(1) average; Space O(1)",
        "immutable_key":"Time O(n); Space O(n)", "remove_none":"Time O(n); Space O(n) output",
        "clamp":"Time O(1); Space O(1)", "chunk_count":"Time O(1); Space O(1)",
        "palindrome":"Time O(n); Space O(n) for normalized text", "validate_nonempty":"Time O(1); Space O(1)",
    }
    drill_mistakes = {
        "safe_first":"Indexing before checking emptiness.", "last_index":"Returning 0 for an empty list.",
        "count_truthy":"Assuming truthy means numerically positive.", "equal_values":"Using `is` instead of `==`.",
        "copy_append":"Aliasing and mutating the caller's list.", "frequency_map":"Calling `list.count` once per unique value, causing O(n²) work.",
        "unique_count":"Using an unhashable element inside the input.", "pair_items":"Letting ordinary `zip` silently truncate unequal inputs.",
        "indexed":"Starting at 1 when zero-based indices are expected.", "sorted_copy":"Calling `.sort()` and returning `None`.",
        "descending":"Negating values when items are not numeric.", "key_with_max":"Calling `max` on an empty mapping.",
        "all_positive":"Forgetting that `all([])` is True.", "any_missing":"Using `if not x`, which also treats 0 as missing.",
        "merge_options":"Applying dictionaries in the wrong precedence order.", "safe_get":"Using `mapping[key]` when absence is valid.",
        "immutable_key":"Assuming a tuple is hashable when it contains a list.", "remove_none":"Filtering with `if x`, which incorrectly removes 0.",
        "clamp":"Reversing the low and high bounds.", "chunk_count":"Dividing by zero when size is nonpositive.",
        "palindrome":"Forgetting case normalization or punctuation handling.", "validate_nonempty":"Hiding a simple guard clause inside a clever expression.",
    }
    for i, (name, goal, expr, test) in enumerate(drills, 1):
        args = argmap[name]
        if name == "frequency_map":
            solution = "def frequency_map(items):\n    frequency = {}\n    for item in items:\n        frequency[item] = frequency.get(item, 0) + 1\n    return frequency"
        elif name == "validate_nonempty":
            solution = "def validate_nonempty(text):\n    if not text:\n        raise ValueError('text must not be empty')\n    return text"
        else:
            solution = f"def {name}({args}):\n    return {expr}"
        solution += f"\n\nassert {test}"
        cells += exercise(f"{i}. {name}", goal, f"def {name}({args}):\n    # TODO: Write your solution here\n    pass", solution, "See assertion in solution", "Choose a readable built-in or guard clause.", "State behavior for empty input.", drill_complexity[name], drill_mistakes[name], "🟢 Easy" if i < 13 else "🟠 Medium")
    cells += footer(["Readable code is easier to verify aloud.", "Guard edge cases deliberately.", "Complexity needs a defined input size."], ["Clever one-liners.", "Hidden mutation.", "Skipping manual tests."], quiz_for("clean"), ["I can narrate my code.", "I can test four edge-case categories.", "I can analyze time and auxiliary space."])
    write_notebook("06_Clean_Python_and_Interview_Patterns.ipynb", cells)


LC_EXAMPLES = {
    "Contains Duplicate":"Input: [1,2,1]\nOutput: True", "Valid Anagram":"Input: 'silent', 'listen'\nOutput: True",
    "Two Sum":"Input: [2,7,11,15], target=9\nOutput: [0,1]", "Group Anagrams":"Input: ['eat','tea','tan']\nOutput: two groups: ['eat','tea'] and ['tan']",
    "Top K Frequent Elements":"Input: [1,1,1,2,2,3], k=2\nOutput: [1,2] in any order",
    "Valid Palindrome":"Input: 'A man, a plan, a canal: Panama'\nOutput: True", "Two Sum II":"Input: [2,7,11,15], target=9\nOutput: [1,2]",
    "3Sum":"Input: [-1,0,1,2,-1,-4]\nOutput: [[-1,-1,2],[-1,0,1]]",
    "Best Time to Buy and Sell Stock":"Input: [7,1,5,3,6,4]\nOutput: 5",
    "Longest Substring Without Repeating Characters":"Input: 'abcabcbb'\nOutput: 3",
    "Valid Parentheses":"Input: '([])'\nOutput: True", "Binary Search":"Input: [-1,0,3,5,9,12], target=9\nOutput: 4",
    "Find Minimum in Rotated Sorted Array":"Input: [3,4,5,1,2]\nOutput: 1",
    "Invert Binary Tree":"Input: root with children 2 and 3\nOutput: root with children 3 and 2",
    "Maximum Depth of Binary Tree":"Input: root → left child\nOutput: 2", "Same Tree":"Input: two single nodes with value 1\nOutput: True",
    "Balanced Binary Tree":"Input: root with two leaf children\nOutput: True", "Climbing Stairs":"Input: n=3\nOutput: 3",
    "House Robber":"Input: [2,7,9,3,1]\nOutput: 12", "Coin Change":"Input: coins=[1,2,5], amount=11\nOutput: 3",
}


def lc_exercise(number: int, title: str, difficulty: str, pattern: str, summary: str, intuition: str,
                signature: str, solution: str, tests: str, complexity: str, mistake: str) -> list[dict]:
    complexity = complexity.replace("Time ", "Time: ").replace("Space ", "Space: ")
    return [md(f"""
    ### {number}. {difficulty} — {title}

    **Goal:** Solve the problem with the stated pattern and explain the invariant.  
    **Problem summary:** {summary}  
    **Pattern:** {pattern}  
    **Intuition:** {intuition}

    **Example**

    ```text
    {LC_EXAMPLES[title]}
    ```

    <details><summary>Hint 1</summary>Identify the operation repeated by the brute-force approach.</details>
    <details><summary>Hint 2</summary>{intuition}</details>
    """), code(f"""
    {signature}
        # TODO: Write your solution here
        pass
    """), md("#### Solution — reveal after attempting"), code(solution + "\n\n" + tests), md(f"""
    **Complexity**

    ```text
    {complexity}
    ```

    **Common mistake:** {mistake}
    """)]


def notebook_07() -> None:
    cells = intro("07 — LeetCode Patterns for AI Engineers", ["Recognize reusable coding patterns", "Move from brute force to an efficient solution", "Communicate invariants, tests, and complexity"], "6–8 hours", ["Problem-solving framework", "Core patterns", "20 guided problems", "Difficulty strategy"], "Notebooks 01–03 and 06")
    cells += [md("""
    ## Problem-solving framework

    🔴 **Must Know**

    ```text
    1 Clarify → 2 Example → 3 Brute force → 4 Bottleneck → 5 Pattern
    → 6 Code → 7 Manual test → 8 Complexity → 9 Edge cases
    ```

    **Think aloud—Two Sum:** “I could compare every pair in O(n²). The repeated question is whether the complement has appeared. A dictionary gives average O(1) lookup, so I scan once, check `target-current`, then store current value and index.”
    """), md("""
    ## Core patterns

    - Hash/frequency map: remember complements or counts.
    - Set: average O(1) membership.
    - Two pointers: shrink a search range with an invariant.
    - Sliding window: maintain a valid contiguous interval.
    - Stack: match nested structure; LIFO.
    - BFS queue: level order; DFS stack/recursion: depth order.
    - Binary search: discard half a sorted/monotonic space.
    - Heap: repeatedly access an extreme.
    - DP: define state, base case, and transition.

    ```text
    two pointers: L → a b c d ← R
    sliding:       a [b c a] b c   maintain validity
    BFS: queue.popleft()           DFS: stack.pop()
    binary: [discard | mid | keep] repeat
    DP stairs: dp[i-2] → dp[i-1] → dp[i]
    ```
    
    **Lower bound:** binary search can return the first index where a value could be inserted while keeping order (`bisect_left`), not only an exact match. In a rotated sorted array, one side around `mid` remains sorted; comparisons identify which half can contain the answer.

    **More think-aloud models:** “For palindrome, normalization need not allocate a new string; two pointers can skip punctuation in O(1) extra space.” “For longest unique substring, I maintain a valid window and move left forward—never backward.” “For tree level order, FIFO order is the invariant, so I choose a deque.”
    """), code("""
    from collections import Counter, defaultdict, deque
    from dataclasses import dataclass
    import heapq

    @dataclass
    class TreeNode:
        val: int
        left: "TreeNode | None" = None
        right: "TreeNode | None" = None
    """), code("""
    def level_order_values(root):
        if root is None: return []
        queue=deque([root]); values=[]
        while queue:
            node=queue.popleft(); values.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        return values

    def iterative_dfs_values(root):
        if root is None: return []
        stack=[root]; values=[]
        while stack:
            node=stack.pop(); values.append(node.val)
            if node.right: stack.append(node.right)
            if node.left: stack.append(node.left)
        return values

    sample_tree=TreeNode(1,TreeNode(2,TreeNode(4)),TreeNode(3))
    assert level_order_values(sample_tree)==[1,2,3,4]
    assert iterative_dfs_values(sample_tree)==[1,2,4,3]
    """), md("## 20 guided problems")]
    problems = [
        ("Contains Duplicate","🟢 Essential Easy","Set","Return whether a value repeats.","Membership is the bottleneck; remember seen values.","def contains_duplicate(nums):", "def contains_duplicate(nums):\n    return len(nums) != len(set(nums))", "assert contains_duplicate([1,2,1]) and not contains_duplicate([])", "Time O(n) average; Space O(n)", "Ignoring how duplicates should behave."),
        ("Valid Anagram","🟢 Essential Easy","Frequency map","Decide whether two strings contain identical character counts.","Equal Counters mean equal multisets.","def valid_anagram(s, t):", "def valid_anagram(s,t):\n    return Counter(s) == Counter(t)", "assert valid_anagram('silent','listen') and not valid_anagram('a','ab')", "Time O(n+m); Space O(k)", "Comparing only sets loses multiplicity."),
        ("Two Sum","🟢 Essential Easy","Hash map","Return two indices whose values sum to target.","Store value→index after checking its complement.","def two_sum(nums, target):", "def two_sum(nums,target):\n    seen={}\n    for i,num in enumerate(nums):\n        if target-num in seen: return [seen[target-num],i]\n        seen[num]=i\n    return []", "assert two_sum([2,7,11,15],9)==[0,1] and two_sum([3,3],6)==[0,1]", "Time O(n); Space O(n)", "Storing before checking can reuse the same element."),
        ("Group Anagrams","🟠 Essential Medium","Frequency/sort key","Group words that are anagrams.","A sorted-character tuple is a stable hashable signature.","def group_anagrams(words):", "def group_anagrams(words):\n    groups=defaultdict(list)\n    for word in words: groups[tuple(sorted(word))].append(word)\n    return list(groups.values())", "assert len(group_anagrams(['eat','tea','tan']))==2", "Time O(n·m log m); Space O(nm)", "Using the sorted list itself as a key."),
        ("Top K Frequent Elements","🟠 Essential Medium","Heap","Return k most frequent values.","Keep/retrieve extremes from value-frequency pairs.","def top_k_frequent(nums, k):", "def top_k_frequent(nums,k):\n    return [value for value,_ in heapq.nlargest(k,Counter(nums).items(),key=lambda p:p[1])]", "assert set(top_k_frequent([1,1,1,2,2,3],2))=={1,2}", "Time O(n + u log k); Space O(u)", "Confusing heap pairs with required returned values."),
        ("Valid Palindrome","🟢 Essential Easy","Two pointers","Ignore punctuation/case and test palindrome.","Move inward, skipping non-alphanumeric characters.","def valid_palindrome(s):", "def valid_palindrome(s):\n    left,right=0,len(s)-1\n    while left<right:\n        while left<right and not s[left].isalnum(): left+=1\n        while left<right and not s[right].isalnum(): right-=1\n        if s[left].lower()!=s[right].lower(): return False\n        left+=1; right-=1\n    return True", "assert valid_palindrome('A man, a plan, a canal: Panama') and not valid_palindrome('race a car')", "Time O(n); Space O(1)", "Forgetting to move pointers after a successful comparison."),
        ("Two Sum II","🟠 Essential Medium","Two pointers","Find 1-indexed pair in a sorted array.","Sum too small → move left; too large → move right.","def two_sum_sorted(numbers, target):", "def two_sum_sorted(numbers,target):\n    left,right=0,len(numbers)-1\n    while left<right:\n        total=numbers[left]+numbers[right]\n        if total==target:return [left+1,right+1]\n        if total<target:left+=1\n        else:right-=1\n    return []", "assert two_sum_sorted([2,7,11,15],9)==[1,2]", "Time O(n); Space O(1)", "Returning zero-based indices."),
        ("3Sum","🟠 Essential Medium","Sort + two pointers","Return unique triples summing to zero.","Fix one sorted value and solve Two Sum II on the suffix.","def three_sum(nums):", "def three_sum(nums):\n    nums=sorted(nums); result=[]\n    for i,a in enumerate(nums):\n        if i and a==nums[i-1]:continue\n        left,right=i+1,len(nums)-1\n        while left<right:\n            total=a+nums[left]+nums[right]\n            if total<0:left+=1\n            elif total>0:right-=1\n            else:\n                result.append([a,nums[left],nums[right]]); left+=1; right-=1\n                while left<right and nums[left]==nums[left-1]:left+=1\n    return result", "assert sorted(three_sum([-1,0,1,2,-1,-4]))==[[-1,-1,2],[-1,0,1]]", "Time O(n²); Space O(n) for sorted copy", "Failing to skip duplicate anchors/results."),
        ("Best Time to Buy and Sell Stock","🟢 Essential Easy","Sliding/min prefix","Maximize later price minus earlier price.","Track minimum price before current day.","def max_profit(prices):", "def max_profit(prices):\n    best=0; minimum=float('inf')\n    for price in prices:\n        minimum=min(minimum,price); best=max(best,price-minimum)\n    return best", "assert max_profit([7,1,5,3,6,4])==5 and max_profit([])==0", "Time O(n); Space O(1)", "Allowing a sell before the buy."),
        ("Longest Substring Without Repeating Characters","🟠 Essential Medium","Sliding window","Find longest substring with unique characters.","Jump left only when the previous duplicate lies inside the current window (`seen[ch] >= left`).","def longest_unique(s):", "def longest_unique(s):\n    left=best=0; seen={}\n    for right,ch in enumerate(s):\n        if ch in seen and seen[ch]>=left:left=seen[ch]+1\n        seen[ch]=right; best=max(best,right-left+1)\n    return best", "assert longest_unique('abcabcbb')==3 and longest_unique('abba')==2", "Time O(n); Space O(k)", "Moving left backward for an old duplicate."),
        ("Valid Parentheses","🟢 Essential Easy","Stack","Validate nested bracket pairs.","Closing brackets must match the latest unmatched opener.","def valid_parentheses(s):", "def valid_parentheses(s):\n    pairs={')':'(',']':'[','}':'{'}; stack=[]\n    for ch in s:\n        if ch in pairs:\n            if not stack or stack.pop()!=pairs[ch]:return False\n        else:stack.append(ch)\n    return not stack", "assert valid_parentheses('([])') and not valid_parentheses('([)]')", "Time O(n); Space O(n)", "Popping an empty stack or ignoring leftovers."),
        ("Binary Search","🟢 Essential Easy","Binary search","Return index of target in sorted data.","Maintain invariant that target, if present, is in inclusive `[left,right]`.","def binary_search(nums, target):", "def binary_search(nums,target):\n    left,right=0,len(nums)-1\n    while left<=right:\n        mid=(left+right)//2\n        if nums[mid]==target:return mid\n        if nums[mid]<target:left=mid+1\n        else:right=mid-1\n    return -1", "assert binary_search([-1,0,3,5,9,12],9)==4 and binary_search([],1)==-1", "Time O(log n); Space O(1)", "Using `<` rather than `<=` with inclusive bounds."),
        ("Find Minimum in Rotated Sorted Array","🟠 Essential Medium","Binary search","Find minimum in a rotated distinct sorted array.","Compare mid with right; minimum remains in the unsorted half.","def find_min_rotated(nums):", "def find_min_rotated(nums):\n    left,right=0,len(nums)-1\n    while left<right:\n        mid=(left+right)//2\n        if nums[mid]>nums[right]:left=mid+1\n        else:right=mid\n    return nums[left]", "assert find_min_rotated([3,4,5,1,2])==1 and find_min_rotated([1])==1", "Time O(log n); Space O(1)", "Discarding mid when it may be the minimum."),
        ("Invert Binary Tree","🟢 Essential Easy","DFS","Swap every node's children.","Process node, then recursively invert both subtrees.","def invert_tree(root):", "def invert_tree(root):\n    if root is None:return None\n    root.left,root.right=invert_tree(root.right),invert_tree(root.left)\n    return root", "r=TreeNode(1,TreeNode(2),TreeNode(3)); assert invert_tree(r).left.val==3", "Time O(n); recursion Space O(h)", "Losing one child by overwriting before swapping."),
        ("Maximum Depth of Binary Tree","🟢 Essential Easy","DFS","Return maximum root-to-leaf node count.","Depth is 1 plus maximum child depth.","def max_depth(root):", "def max_depth(root):\n    return 0 if root is None else 1+max(max_depth(root.left),max_depth(root.right))", "assert max_depth(TreeNode(1,TreeNode(2)))==2 and max_depth(None)==0", "Time O(n); Space O(h)", "Wrong empty-tree base depth."),
        ("Same Tree","🟢 Essential Easy","DFS","Test structural and value equality.","Both absent is true; exactly one absent is false.","def same_tree(p, q):", "def same_tree(p,q):\n    if p is None or q is None:return p is q\n    return p.val==q.val and same_tree(p.left,q.left) and same_tree(p.right,q.right)", "assert same_tree(TreeNode(1),TreeNode(1)) and not same_tree(TreeNode(1),TreeNode(2))", "Time O(n); Space O(h)", "Checking values before handling None."),
        ("Balanced Binary Tree","🟠 Essential Medium","Postorder DFS","Check every subtree height difference <= 1.","Return height and a failure sentinel in one traversal.","def is_balanced(root):", "def is_balanced(root):\n    def height(node):\n        if node is None:return 0\n        left=height(node.left)\n        if left<0:return -1\n        right=height(node.right)\n        if right<0 or abs(left-right)>1:return -1\n        return 1+max(left,right)\n    return height(root)>=0", "assert is_balanced(TreeNode(1,TreeNode(2),TreeNode(3)))", "Time O(n); Space O(h)", "Recomputing heights at every node makes O(n²)."),
        ("Climbing Stairs","🟢 Essential Easy","Dynamic programming","Count ways using steps of 1 or 2.","State is ways to reach current step; transition sums prior two.","def climb_stairs(n):", "def climb_stairs(n):\n    if n<=1:return 1\n    prev2=prev1=1\n    for _ in range(2,n+1):prev2,prev1=prev1,prev1+prev2\n    return prev1", "assert climb_stairs(3)==3 and climb_stairs(1)==1", "Time O(n); Space O(1)", "Returning the stale state variable."),
        ("House Robber","🟠 Essential Medium","Dynamic programming","Maximize nonadjacent sum.","At each house choose skip previous result or take current plus two-back.","def house_robber(nums):", "def house_robber(nums):\n    prev2=prev1=0\n    for value in nums:prev2,prev1=prev1,max(prev1,prev2+value)\n    return prev1", "assert house_robber([2,7,9,3,1])==12 and house_robber([])==0", "Time O(n); Space O(1)", "Updating one state before using its old value."),
        ("Coin Change","🔵 Optional","Dynamic programming","Minimum coins totaling amount, or -1.","`dp[a]` is minimum coins for subtotal a; relax from smaller subtotal.","def coin_change(coins, amount):", "def coin_change(coins,amount):\n    dp=[amount+1]*(amount+1); dp[0]=0\n    for subtotal in range(1,amount+1):\n        for coin in coins:\n            if coin<=subtotal:dp[subtotal]=min(dp[subtotal],1+dp[subtotal-coin])\n    return -1 if dp[amount]>amount else dp[amount]", "assert coin_change([1,2,5],11)==3 and coin_change([2],3)==-1", "Time O(amount·coins); Space O(amount)", "Missing unreachable-state handling."),
    ]
    for i, p in enumerate(problems, 1): cells += lc_exercise(i, *p)
    cells += [md("""
    ## BFS and iterative DFS reference

    ```python
    # BFS level order
    queue = deque([root])
    while queue:
        node = queue.popleft()

    # iterative DFS
    stack = [root]
    while stack:
        node = stack.pop()
    ```

    Recursion is concise; an explicit stack avoids recursion-depth limits. Queue order produces level order; stack order pursues the most recently discovered branch.

    ## Difficulty strategy

    Master every 🟢 Essential Easy, then 🟠 Essential Medium. Treat 🔵 Optional as breadth after the core patterns are automatic.
    """)]
    cells += footer(["Name the bottleneck before the pattern.", "Maintain an explicit invariant.", "Test duplicates and boundaries."], ["Coding before clarifying.", "Silent off-by-one changes.", "Stating complexity without considering sorting."], quiz_for("leetcode"), ["I can solve all essential easy problems unaided.", "I can explain eight main patterns.", "I can state and defend an invariant."])
    write_notebook("07_LeetCode_Patterns_for_AI_Engineers.ipynb", cells)


def notebook_08() -> None:
    cells = intro("08 — AI Engineer Python Mock Interview", ["Simulate a full interview under time pressure", "Debug and communicate aloud", "Score readiness objectively"], "90 minutes interview + 60 minutes review", ["Instructions", "Round 1 fundamentals", "Round 2 debugging", "Round 3 coding", "Round 4 NumPy/pandas", "Round 5 code review", "Scoring"], "Notebooks 01–07")
    cells += [md("""
    ## Instructions

    Use a timer, speak aloud, and do not open reveal sections until the round ends. Clarify assumptions, give brute force first, test manually, and state time/space complexity.

    ## Round 1 — Python fundamentals (15 minutes)

    1. List vs tuple?  
    2. Dictionary vs set?  
    3. `append` vs `extend`?  
    4. `sort` vs `sorted`?  
    5. `is` vs `==`?  
    6. Shallow vs deep copy?  
    7. What is a generator?  
    8. What does `yield` do?  
    9. List comprehension vs generator expression?  
    10. What is `defaultdict`?  
    11. Why use `deque` for BFS?  
    12. Mutable vs immutable?  
    13. Why must dictionary keys be hashable?  
    14. What is the mutable-default trap?  
    15. What does average O(1) dict lookup mean?

    <details><summary>Reveal model answers</summary>

    1. Lists are mutable dynamic arrays; tuples are immutable sequences and may be hashable. 2. Dict maps keys to values; set stores unique values. 3. Append adds one object; extend iterates and adds each. 4. Sort mutates/returns None; sorted creates a list. 5. Identity vs value. 6. New outer container/shared nested values vs recursively independent graph. 7–8. Lazy stateful iterator created by a function using yield. 9. Eager list vs lazy iterator. 10. Dict subclass invoking a missing-value factory. 11. O(1) popleft. 12. Whether object state can change. 13. Stable bucket placement. 14. Defaults evaluate once. 15. Expected constant scaling under ordinary hashing, not a worst-case guarantee.
    </details>
    """), md("""
    ## Round 2 — Debugging (20 minutes)

    For each example: identify the bug, explain why, fix it, and state complexity. Broken functions are defined but deliberately not invoked.
    """)]
    broken = [
        ("mutable default", "def broken_add(x, items=[]):\n    items.append(x)\n    return items", "def fixed_add(x, items=None):\n    if items is None: items=[]\n    items.append(x); return items\nassert fixed_add(1)==[1] and fixed_add(2)==[2]", "Default list persists between calls. O(1) amortized per append."),
        ("dictionary key mismatch", "def broken_lookup(d, user_id):\n    return d[str(user_id)]", "def fixed_lookup(d, user_id):\n    return d.get(user_id)\nassert fixed_lookup({1:'A'},1)=='A'", "Do not coerce unless the schema uses string keys. Average O(1)."),
        ("infinite pointers", "def broken_palindrome(s):\n    left,right=0,len(s)-1\n    while left<right:\n        if s[left]!=s[right]: return False", "def fixed_palindrome(s):\n    left,right=0,len(s)-1\n    while left<right:\n        if s[left]!=s[right]:return False\n        left+=1; right-=1\n    return True\nassert fixed_palindrome('aba')", "Pointers never move on matching characters. O(n)/O(1)."),
        ("range endpoint", "def broken_sum(nums):\n    total=0\n    for i in range(len(nums)-1): total+=nums[i]\n    return total", "def fixed_sum(nums):\n    return sum(nums)\nassert fixed_sum([1,2,3])==6", "The final index is excluded. O(n)/O(1)."),
        ("wrong return", "def broken_fib(n):\n    a,b=0,1\n    for _ in range(n): a,b=b,a+b\n    result=[]\n    return result", "def fixed_fib(n):\n    a,b=0,1\n    for _ in range(n):a,b=b,a+b\n    return a\nassert fixed_fib(6)==8", "Final state is `a`, not the unused list. O(n)/O(1)."),
        ("modify during iteration", "def broken_remove_even(nums):\n    for x in nums:\n        if x%2==0: nums.remove(x)\n    return nums", "def fixed_remove_even(nums):\n    return [x for x in nums if x%2]\nassert fixed_remove_even([2,2,3])==[3]", "Removal shifts and skips elements. O(n) solution/output O(n)."),
        ("identity", "def broken_equal(a,b):\n    return a is b", "def fixed_equal(a,b):\n    return a == b\nassert fixed_equal([1],[1])", "`is` checks identity. Value comparison is O(n) for lists."),
        ("duplicate loss", "def broken_two_sum(nums,target):\n    positions={x:i for i,x in enumerate(nums)}\n    for x in nums:\n        if target-x in positions:return [positions[x],positions[target-x]]", "def fixed_two_sum(nums,target):\n    seen={}\n    for i,x in enumerate(nums):\n        if target-x in seen:return [seen[target-x],i]\n        seen[x]=i\n    return []\nassert fixed_two_sum([3,3],6)==[0,1]", "One-pass ordering prevents using one index twice. O(n)/O(n)."),
        ("NumPy shape mismatch", "def broken_linear(X,W):\n    return X*W  # X=(batch,features), W=(features,out)", "import numpy as np\ndef fixed_linear(X,W):\n    return X @ W\nassert fixed_linear(np.ones((2,3)),np.ones((3,4))).shape==(2,4)", "Need matrix multiplication, not incompatible elementwise broadcasting. O(bfo)."),
        ("pandas precedence", "def broken_filter(df):\n    return df[df['age']>30 & df['active']]", "import pandas as pd\ndef fixed_filter(df):\n    return df[(df['age']>30) & df['active']]\nassert len(fixed_filter(pd.DataFrame({'age':[31,20],'active':[True,True]})))==1", "Parenthesize each comparison before `&`. O(n)/O(n) output."),
    ]
    for i, (title, bad, fixed, explanation) in enumerate(broken, 1):
        cells += [md(f"### Debugging exercise {i}: {title}\n\n**Broken code**"), code(bad), md("<details><summary>Hint</summary>Trace a minimal boundary or duplicate case.</details>\n\n#### Fix and explanation"), code(fixed), md(explanation)]
    cells += [md("""
    ## Round 3 — Coding (50 minutes)

    ### Problem A — Easy, 10 minutes
    Return the first repeated model ID, or `None`. Test empty and duplicate inputs. Target O(n) time.
    """), code("""
    def first_repeated_model_id(model_ids):
        # TODO
        pass
    """), md("""
    ### Problem B — Medium, 20 minutes
    Return the length of the longest contiguous run of predictions with score at least `threshold`.
    """), code("""
    def longest_confident_run(scores, threshold):
        # TODO
        pass
    """), md("""
    ### Problem C — AI data processing, 20 minutes

    Given prediction dictionaries, group by label, calculate each average confidence, and return the top label. Handle empty input. Define a deterministic tie rule.
    """), code("""
    def top_average_label(predictions):
        # TODO
        pass
    """), md("### Round 3 solutions"), code("""
    from collections import defaultdict

    def first_repeated_model_id(model_ids):
        seen=set()
        for model_id in model_ids:
            if model_id in seen:return model_id
            seen.add(model_id)
        return None

    def longest_confident_run(scores, threshold):
        best=current=0
        for score in scores:
            current=current+1 if score>=threshold else 0
            best=max(best,current)
        return best

    def top_average_label(predictions):
        if not predictions:return None
        grouped=defaultdict(list)
        for prediction in predictions:grouped[prediction['label']].append(prediction['score'])
        averages={label:sum(scores)/len(scores) for label,scores in grouped.items()}
        return min(averages, key=lambda label:(-averages[label],label))

    assert first_repeated_model_id([1,2,1])==1
    assert longest_confident_run([.8,.9,.2,.9],.8)==2
    assert top_average_label([{'label':'cat','score':.91},{'label':'dog','score':.82},{'label':'cat','score':.77}])=='cat'
    """), md("""
    **Complexity:** each solution is O(n) time; first/grouping use O(n) or O(k) space, while the run uses O(1). Common mistakes: missing empty behavior, resetting the wrong state, and nondeterministic ties.

    ## Round 4 — NumPy / pandas (20 minutes)

    Implement cosine similarity, reshape flat image batches, normalize rows, filter/group a DataFrame, fill age with a supplied training median, and left-join predictions to metadata.
    """), code("""
    import numpy as np
    import pandas as pd

    def cosine_similarity(a, b):
        # TODO: calculate safely for zero vectors
        pass

    def reshape_images(flat, height, width):
        # TODO: reshape while preserving the batch dimension
        pass

    def normalize_rows(X):
        # TODO: return unit-length rows and guard zero rows
        pass

    def prepare_frame(frame, predictions, training_age_median):
        # TODO: fill age, filter score, group labels, and left-join predictions
        pass
    """), md("### Round 4 solutions"), code("""
    def cosine_similarity(a,b):
        denominator=np.linalg.norm(a)*np.linalg.norm(b)
        return float(np.dot(a,b)/denominator) if denominator else 0.0

    def reshape_images(flat, height, width):
        return flat.reshape(flat.shape[0],height,width)

    def normalize_rows(X):
        norms=np.linalg.norm(X,axis=1,keepdims=True)
        return X/np.where(norms==0,1,norms)

    def prepare_frame(frame, predictions, training_age_median):
        clean=frame.assign(age=frame['age'].fillna(training_age_median))
        clean=clean.loc[clean['score']>=.5]
        summary=clean.groupby('label')['score'].mean()
        joined=clean.merge(predictions,on='user_id',how='left',suffixes=('_observed','_predicted'),validate='many_to_one')
        return summary,joined

    assert np.isclose(cosine_similarity(np.array([1.,0.]),np.array([1.,0.])),1)
    assert normalize_rows(np.array([[3.,4.]])).shape==(1,2)
    """), md("""
    ## Round 5 — Clean-code review (10 minutes)

    Refactor this working code. Identify weak names, duplicated sorting, nesting, and mutation of caller data.

    ```python
    def f(x):
        r = {}
        for w in x:
            if tuple(sorted(w)) in r:
                r[tuple(sorted(w))].append(w)
            else:
                r[tuple(sorted(w))] = [w]
        x.clear()
        return list(r.values())
    ```

    <details><summary>Review guidance</summary>Rename, use `defaultdict`, compute key once, and avoid clearing the input.</details>
    """), code("""
    def group_anagrams_clean(words):
        groups=defaultdict(list)
        for word in words:
            key=tuple(sorted(word))
            groups[key].append(word)
        return list(groups.values())

    original=['eat','tea']
    assert len(group_anagrams_clean(original))==1 and original==['eat','tea']
    """), md("""
    ## Scoring

    | Category | Points |
    |---|---:|
    | Python Fundamentals | /20 |
    | Data Structures | /20 |
    | Problem Solving | /20 |
    | NumPy / pandas | /15 |
    | Code Quality | /10 |
    | Complexity Analysis | /10 |
    | Communication | /5 |
    | **Total** | **/100** |

    **90–100 Strong · 75–89 Interview Ready · 60–74 Needs Targeted Review · <60 Review Fundamentals**
    """)]
    cells += footer(["A mock interview measures communication as well as correctness.", "Debug from a minimal failing case.", "Use the score to target the next review."], ["Looking at solutions early.", "Skipping complexity.", "Ignoring shape/join assumptions."], quiz_for("mock"), ["I completed every round under time.", "I scored at least 75.", "I can name my weakest two areas."])
    write_notebook("08_AI_Engineer_Python_Mock_Interview.ipynb", cells)


def rapid_bank() -> list[tuple[str, str]]:
    return [
        # Core collections (1–20)
        ("Which collection gives average O(1) membership?", "A set."),
        ("Which is immutable: list or tuple?", "Tuple."),
        ("What does `dict.get` help avoid?", "`KeyError`, while supplying a default."),
        ("Does `sorted` mutate its input?", "No; it returns a new list."),
        ("Does `list.sort` return the sorted list?", "No; it mutates and returns `None`."),
        ("`append([2,3])` adds how many elements?", "One: the list object itself."),
        ("What does `extend([2,3])` do?", "Adds two elements by iterating the argument."),
        ("Typical list membership complexity?", "O(n)."),
        ("Typical set membership complexity?", "Average O(1)."),
        ("Typical list append complexity?", "Amortized O(1)."),
        ("Why is list insertion at zero O(n)?", "Existing references must shift."),
        ("What type should map model IDs to objects?", "Dictionary."),
        ("What type should represent an immutable coordinate?", "Tuple."),
        ("Can a list usually be a dict key?", "No; it is mutable and unhashable."),
        ("When is a tuple hashable?", "When all its elements are hashable."),
        ("`remove` vs `discard` on a set?", "`remove` raises if absent; `discard` does not."),
        ("What does `a & b` mean for sets?", "Intersection."),
        ("What does `a - b` mean for sets?", "Values in a but not b."),
        ("What does negative index -1 select?", "The final element."),
        ("What does slice end mean?", "It is exclusive."),
        # References/functions (21–40)
        ("What does `b = a` do for a list?", "Aliases the same object."),
        ("What does a shallow copy share?", "Nested referenced objects."),
        ("What does deepcopy do?", "Recursively copies the reachable object graph."),
        ("When are default arguments evaluated?", "Once, when `def` executes."),
        ("Safe mutable-default pattern?", "Default to `None`, allocate inside."),
        ("What is LEGB?", "Local, Enclosing, Global, Built-in scope lookup."),
        ("What does `nonlocal` rebind?", "A name in an enclosing function scope."),
        ("What does `global` rebind?", "A module-level name."),
        ("Are functions first-class in Python?", "Yes: assign, pass, and return them."),
        ("When prefer `def` over lambda?", "When logic needs a name, statements, or explanation."),
        ("What does `*args` collect?", "Extra positional arguments in a tuple."),
        ("What does `**kwargs` collect?", "Extra keyword arguments in a dictionary."),
        ("What does a function return without `return`?", "`None`."),
        ("What is `self`?", "The receiving instance by convention."),
        ("Class vs instance variable?", "Shared on class vs stored per instance."),
        ("Why prefer composition for RAG?", "Retriever and LLM remain independently replaceable."),
        ("What does a dataclass reduce?", "Boilerplate such as init and repr."),
        ("Do type hints enforce types by default?", "No."),
        ("Why catch specific exceptions?", "Avoid hiding unrelated programming errors."),
        ("Why use a context manager?", "Guaranteed resource cleanup."),
        # Collections/comprehensions (41–60)
        ("What does `yield` create?", "A generator function that produces values lazily."),
        ("Iterable vs iterator?", "An iterable can produce an iterator; an iterator tracks traversal state."),
        ("List comprehension vs generator?", "Eager materialization vs lazy production."),
        ("Trailing `if` in a comprehension?", "Filters inputs."),
        ("Inline `a if c else b`?", "Selects an output value."),
        ("What does Counter model?", "A frequency mapping."),
        ("What does `most_common(3)` return?", "Three highest-frequency `(item,count)` pairs."),
        ("What does defaultdict need?", "A zero-argument missing-value factory."),
        ("A defaultdict surprise?", "Reading a missing key inserts it."),
        ("Best standard queue?", "`collections.deque`."),
        ("What does deque.popleft remove?", "The front/leftmost item."),
        ("Why not list.pop(0) for BFS?", "It shifts items and costs O(n)."),
        ("Stack order?", "LIFO."),
        ("Queue order?", "FIFO."),
        ("Python heap type?", "Min-heap."),
        ("Heap push/pop complexity?", "O(log n)."),
        ("What does enumerate provide?", "Index-value pairs."),
        ("What does zip do?", "Pairs items and stops at the shortest unless strict mode is used."),
        ("What do any/all do?", "Short-circuit existential/universal truth checks."),
        ("How do nested lists sort by default?", "Lexicographically."),
        # NumPy (61–80)
        ("Why ndarray over a list for matrices?", "Homogeneous storage and vectorized numerical operations."),
        ("What does shape describe?", "Length of every array dimension."),
        ("What does ndim return?", "Number of dimensions."),
        ("What does size return?", "Total element count."),
        ("What does dtype describe?", "Element representation/type."),
        ("What does `x[:,0]` select?", "First column."),
        ("What does `x[0,:]` select?", "First row."),
        ("What is boolean masking?", "Selecting elements/rows where a boolean condition is true."),
        ("What is vectorization?", "Expressing whole-array operations without Python element loops."),
        ("What is broadcasting?", "Rules for combining compatible differently shaped arrays."),
        ("Broadcast dimensions are compared from where?", "From the right."),
        ("Broadcast-compatible dimensions?", "Equal or one of them is 1."),
        ("What does axis=0 reduction do on a matrix?", "Collapses rows, producing one result per column."),
        ("What does axis=1 reduction do?", "Collapses columns, producing one result per row."),
        ("`A * B` vs `A @ B`?", "Element-wise vs matrix multiplication."),
        ("Shape of `(b,f) @ (f,o)`?", "`(b,o)`."),
        ("flatten vs ravel?", "Flatten copies; ravel returns a view when possible."),
        ("Why subtract max before softmax?", "Numerical stability against overflow."),
        ("Cosine similarity denominator?", "Product of vector L2 norms."),
        ("Why seed random generation?", "Reproducible examples and tests."),
        # pandas (81–100)
        ("Series vs DataFrame selection syntax?", "One column name usually yields Series; a list of names yields DataFrame."),
        ("loc vs iloc?", "Labels vs integer positions."),
        ("Is a loc label slice endpoint inclusive?", "Yes."),
        ("Is an iloc slice endpoint inclusive?", "No."),
        ("Why parentheses around pandas conditions?", "Operator precedence with `&` and `|`."),
        ("How inspect missing counts?", "`df.isna().sum()`."),
        ("What is preprocessing leakage?", "Using validation/test information to fit transformations."),
        ("Where should imputation statistics be fitted?", "Training data only."),
        ("What is split-apply-combine?", "Group rows, aggregate/transform groups, combine results."),
        ("What is a left merge?", "All left rows plus matching right columns."),
        ("Why validate merge cardinality?", "Detect unintended duplicate-key row explosions."),
        ("Why prefer vectorized pandas operations?", "They are concise and typically faster."),
        ("Is apply always bad?", "No; use it when vectorized alternatives are unclear or unavailable."),
        ("How inspect class proportions?", "`value_counts(normalize=True)`."),
        ("Why remove duplicates before evaluation?", "They can leak and inflate metrics."),
        ("How parse dates?", "`pd.to_datetime`."),
        ("How extract month?", "`series.dt.month`."),
        ("How sort descending?", "`sort_values(..., ascending=False)`."),
        ("How select rows and chosen columns?", "`df.loc[mask, columns]`."),
        ("Why call copy after filtering before mutation?", "Make ownership explicit and avoid chained-assignment ambiguity."),
        # Algorithms/clean code (101–120)
        ("Two Sum optimal pattern?", "One-pass complement dictionary."),
        ("Valid palindrome pattern?", "Two pointers."),
        ("Longest unique substring pattern?", "Sliding window with last-seen positions."),
        ("Why require `seen[ch] >= left`?", "Only duplicates inside the active window force movement."),
        ("Valid parentheses structure?", "Stack."),
        ("BFS structure?", "Deque queue."),
        ("DFS structures?", "Recursion or explicit stack."),
        ("Binary search prerequisite?", "Sorted data or a monotonic predicate."),
        ("Binary search time?", "O(log n)."),
        ("When use a heap?", "Repeatedly retrieving an extreme/top-k without full sorting."),
        ("Three DP ingredients?", "State, base case, transition."),
        ("Climbing-stairs transition?", "`ways[i]=ways[i-1]+ways[i-2]`."),
        ("Set-based duplicate detection complexity?", "O(n) average time and O(n) space."),
        ("Sort-based grouping cost for n words length m?", "O(n·m log m)."),
        ("What should `n` mean in complexity?", "Define it explicitly for the input."),
        ("Auxiliary vs output space?", "Temporary working storage vs required returned storage."),
        ("`is` vs `==`?", "Identity vs value equality."),
        ("Idiomatic None check?", "`x is None`."),
        ("Four basic test categories?", "Normal, empty, duplicate, boundary."),
        ("First live-coding step?", "Clarify requirements and examples."),
    ]


def cheat_sheet() -> None:
    cells = intro("Python Interview Cheat Sheet", ["Refresh the highest-yield syntax in 15–20 minutes", "Recall core algorithm templates", "Run a 120-question self-check"], "15–20 minutes + optional quiz", ["Data structures", "Patterns", "NumPy", "pandas", "Complexity and traps", "AI examples", "120-question bank", "Final checklist"], "Notebooks 01–08")
    cells += [md("""
    ## Data structures

    🔴 **Must Know**

    ```python
    nums = []; nums.append(x); nums.pop()
    d = {}; d[key] = value; value = d.get(key, default)
    seen = set(); seen.add(x)
    from collections import Counter, defaultdict, deque
    count = Counter(nums)
    groups = defaultdict(list)
    queue = deque(); queue.append(x); queue.popleft()
    ```

    Use list for ordered mutable data, dict for key→value, set for membership/uniqueness, tuple for an immutable composite key, deque for FIFO, and heap for repeated extremes.

    ## Patterns

    ```python
    # Frequency
    count = {}
    for x in nums: count[x] = count.get(x, 0) + 1

    # Two pointers
    left, right = 0, len(nums) - 1
    while left < right: ...

    # Sliding window
    left = 0
    for right in range(len(s)): ...

    # BFS / DFS
    queue = deque([root])
    while queue: node = queue.popleft()
    stack = [root]
    while stack: node = stack.pop()

    # Binary search
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        ...
    ```
    """), md("""
    ## NumPy

    ```python
    x.shape; x.reshape(...); x.mean(axis=0)
    x.sum(axis=1); x.argmax(axis=1)
    x * y     # element-wise
    x @ y     # matrix multiplication
    x[x > 0]  # boolean mask
    ```

    `axis=0` collapses rows → one value per column. `axis=1` collapses columns → one value per row. Broadcasting aligns shapes from the right; dimensions must match or one must be 1.

    ## pandas

    ```python
    df.head(); df.shape; df.info()
    df["column"]
    df[df["age"] > 30]
    df.groupby("label").size()
    df.sort_values("score")
    pd.merge(a, b, on="id", how="left")
    df.isna().sum(); df.drop_duplicates()
    ```
    """), md("""
    ## Complexity and traps

    ```text
    List index O(1)            List append O(1) amortized
    List search O(n)           List sort O(n log n)
    Dict/set lookup O(1) avg   Deque append/popleft O(1)
    Heap push/pop O(log n)     Binary search O(log n)

    list.pop(0) → O(n); use deque for a queue
    b = a → same object
    sorted(x) → new list
    x.sort() → mutates, returns None
    dict[key] → KeyError if missing; dict.get → fallback
    is → identity; == → value
    mutable default → shared state; use None
    ```

    ## AI examples

    ```python
    chunk = {"text": "...", "page": 4, "embedding": [0.1, 0.2]}
    documents_by_source = defaultdict(list)
    embeddings = np.zeros((32, 768))
    similarity = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
    high_confidence = [p for p in predictions if p["score"] >= 0.8]
    payload = {"question": "...", "top_k": 5}

    def batches(items, size):
        for i in range(0, len(items), size):
            yield items[i:i + size]
    ```
    """)]
    cells += [code("""
    from collections import Counter, defaultdict, deque
    import numpy as np
    import pandas as pd

    nums = [3, 1, 3]
    assert Counter(nums)[3] == 2
    queue = deque([1, 2]); assert queue.popleft() == 1
    matrix = np.array([[1, 2], [3, 4]])
    assert np.array_equal(matrix.sum(axis=0), np.array([4, 6]))
    frame = pd.DataFrame({"label": ["cat", "dog", "cat"]})
    assert frame["label"].value_counts().loc["cat"] == 2
    """)]
    cells += exercise(
        "Cheat-sheet Two Sum challenge",
        "Return the two indices whose values sum to target; return an empty list if absent.",
        "def cheat_two_sum(nums, target):\n    # TODO: Write your solution here\n    pass",
        "def cheat_two_sum(nums, target):\n    seen = {}\n    for index, value in enumerate(nums):\n        complement = target - value\n        if complement in seen:\n            return [seen[complement], index]\n        seen[value] = index\n    return []\n\nassert cheat_two_sum([2, 7, 11, 15], 9) == [0, 1]",
        "Input: nums=[2,7,11,15], target=9\nOutput: [0,1]",
        "A dictionary can remember values already visited.",
        "Check the complement before storing the current value so one index is not reused.",
        "Time O(n); Space O(n)",
        "Storing first and then matching an element with itself.",
        "🔴 Interview Challenge",
    )
    bank = rapid_bank()
    assert len(bank) == 120
    question_md = "\n".join(f"{i}. **{q}** <details><summary>Answer</summary>{a}</details>" for i, (q, a) in enumerate(bank, 1))
    cells += [md("## 120-question rapid-fire bank\n\n" + question_md), md("""
    ## Final checklist

    ### Python Core
    - [ ] I choose list, dict, set, and tuple quickly.
    - [ ] I understand references, mutability, shallow/deep copying.
    - [ ] I explain append/extend, sort/sorted, and is/==.
    - [ ] I write functions/classes and avoid mutable defaults.
    - [ ] I understand generators.

    ### Collections
    - [ ] I use Counter, defaultdict, deque, and heapq.
    - [ ] I explain stack vs queue.

    ### NumPy
    - [ ] I predict shapes and axes.
    - [ ] I understand indexing, broadcasting, vectorization, `*` vs `@`.
    - [ ] I calculate cosine similarity.

    ### pandas
    - [ ] I inspect, filter, fill, group, merge, and inspect class balance.
    - [ ] I prevent preprocessing leakage and validate joins.

    ### Interview coding
    - [ ] I recognize hash map, set, pointers, window, stack, BFS, DFS, binary search, heap, and DP.
    - [ ] I state time/space complexity and test edge cases.
    - [ ] I explain my approach while coding.

    > **If you can solve the essential exercises without looking at the solutions, explain your complexity, and clearly describe why you selected each data structure, your Python foundation is strong enough for the coding portion of many AI Engineer interviews.**
    """)]
    cells += footer(["Choose structures by required operations.", "Treat shape and complexity as part of correctness.", "Communicate before and during coding."], ["Memorizing code without invariants.", "Ignoring mutation and edge cases.", "Fitting preprocessing on test data."], quiz_for("cheat"), ["I can answer at least 100/120 rapidly.", "I can reproduce core templates.", "I am ready to run the mock interview."])
    write_notebook("Python_Interview_Cheat_Sheet.ipynb", cells)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    notebook_01()
    notebook_02()
    notebook_03()
    notebook_04()
    notebook_05()
    notebook_06()
    notebook_07()
    notebook_08()
    cheat_sheet()
    print(f"Generated 9 notebooks in {OUT.resolve()}")


if __name__ == "__main__":
    main()
