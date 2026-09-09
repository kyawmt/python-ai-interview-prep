Create a **complete set of Jupyter Notebooks for Python interview preparation for an AI Engineer role**.

The notebooks must focus on the Python knowledge most useful for **AI Engineer / Machine Learning Engineer / Applied AI Engineer interviews**.

Cover these areas:

1. Lists, dictionaries, sets, and tuples
2. Functions and classes
3. Comprehensions
4. `collections`
5. NumPy basics
6. pandas basics
7. Writing clean Python code
8. LeetCode-style problem solving

The purpose is **active practice**, not passive reading.

Every notebook should contain:

- concise theory
- visual explanations where useful
- executable examples
- exercises
- interview questions
- coding challenges
- solutions hidden or placed after the exercises
- common mistakes
- time and space complexity where relevant
- AI/ML-related examples where appropriate

The learner already knows basic Python but needs a **structured interview refresher and hands-on practice**.

The final result should help the learner confidently write Python during live coding interviews and understand Python code commonly used in AI applications.

---

# 1. Create These Notebooks

Create the following notebook files:

```text
python_ai_interview/
│
├── 01_Python_Data_Structures.ipynb
├── 02_Functions_Classes_and_Python_Core.ipynb
├── 03_Comprehensions_and_Collections.ipynb
├── 04_NumPy_for_AI_Engineers.ipynb
├── 05_Pandas_for_AI_Engineers.ipynb
├── 06_Clean_Python_and_Interview_Patterns.ipynb
├── 07_LeetCode_Patterns_for_AI_Engineers.ipynb
├── 08_AI_Engineer_Python_Mock_Interview.ipynb
└── Python_Interview_Cheat_Sheet.ipynb
```

The notebooks should build progressively.

Avoid unnecessary duplication, but reinforce important concepts where repetition helps learning.

---

# 2. Notebook Teaching Format

For every major topic, use the following structure:

## Concept

Explain what it is.

## Why It Matters

Explain why an AI Engineer should know it.

## Syntax

Show minimal Python syntax.

## Example

Provide a small executable example.

## How Python Executes It

Explain important behavior such as:

- mutability
- references
- hashing
- iteration
- copying
- lookup

## Complexity

Where appropriate show:

```text
Time: O(...)
Space: O(...)
```

## Common Interview Mistake

Show typical bugs.

## Interview Question

Provide a question an interviewer may ask.

## Exercise

Give an executable exercise with:

```python
# TODO: Write your solution here
```

## Solution

Place the solution after the exercise in a clearly separated section.

Do not immediately reveal the answer above the exercise.

---

# 3. Notebook 01 — Python Data Structures

Create:

```text
01_Python_Data_Structures.ipynb
```

This should be one of the most important notebooks.

Cover:

# Lists

Explain:

```python
nums = [1, 2, 3]
```

Cover:

- indexing
- negative indexing
- slicing
- append
- extend
- insert
- remove
- pop
- sort
- `sorted`
- reverse
- membership
- iteration
- copying

Explain differences between:

```python
nums.sort()
```

and:

```python
sorted(nums)
```

Explain:

```python
nums.append([4, 5])
```

vs:

```python
nums.extend([4, 5])
```

Explain complexity:

| Operation | Typical Complexity |
|---|---|
| Index access | O(1) |
| Append | amortized O(1) |
| Pop from end | O(1) |
| Insert beginning | O(n) |
| Membership | O(n) |
| Sort | O(n log n) |

Explain why Python lists behave like dynamic arrays.

---

# 4. List References and Copying

Make this important.

Explain:

```python
a = [1, 2, 3]
b = a

b.append(4)
```

Show why both change.

Compare:

```python
b = a
```

```python
b = a.copy()
```

```python
b = a[:]
```

and:

```python
import copy
b = copy.deepcopy(a)
```

Explain:

- reference
- shallow copy
- deep copy

Use nested-list examples.

---

# 5. List Slicing

Explain:

```python
nums[start:end:step]
```

Examples:

```python
nums[:3]
nums[2:]
nums[::-1]
nums[::2]
```

Include interview exercises.

---

# 6. Dictionaries

Explain:

```python
user = {
    "name": "Alice",
    "age": 30
}
```

Cover:

- create
- read
- update
- delete
- membership
- iteration
- keys
- values
- items
- `get`
- `setdefault`

Explain:

```python
d[key]
```

vs:

```python
d.get(key)
```

Explain average complexity:

```text
Lookup: O(1)
Insert: O(1)
Delete: O(1)
```

Explain that these are average-case hash-table operations.

---

# 7. Hash Tables

Explain conceptually:

```text
Key
 ↓
hash()
 ↓
bucket/location
 ↓
value
```

Explain why dictionaries are useful for:

- counting
- lookup
- caching
- grouping
- mapping IDs to objects

Connect this directly to LeetCode problems.

---

# 8. Dictionary Counting Pattern

Show:

```python
count = {}

for x in nums:
    count[x] = count.get(x, 0) + 1
```

Then compare with:

```python
from collections import Counter

count = Counter(nums)
```

Explain when each is useful.

---

# 9. Sets

Explain:

```python
seen = set()
```

Cover:

- add
- remove
- discard
- membership
- union
- intersection
- difference

Explain average lookup:

```text
O(1)
```

Compare:

```python
x in list
```

typically:

```text
O(n)
```

versus:

```python
x in set
```

typically:

```text
O(1)
```

Explain why sets are heavily used in interview problems.

---

# 10. Set Interview Patterns

Show:

## Duplicate detection

```python
seen = set()

for x in nums:
    if x in seen:
        ...
    seen.add(x)
```

## Unique values

```python
unique = set(nums)
```

## Intersection

```python
set(a) & set(b)
```

Provide exercises.

---

# 11. Tuples

Explain:

```python
point = (3, 5)
```

Cover:

- immutable
- indexing
- unpacking
- returning multiple values
- dictionary keys

Explain why:

```python
[1, 2]
```

cannot normally be dictionary key while:

```python
(1, 2)
```

can, assuming its contents are hashable.

Connect to problems such as Group Anagrams:

```python
key = tuple(sorted(word))
```

Explain why converting the sorted list to a tuple makes it usable as a dictionary key.

---

# 12. Mutable vs Immutable

Create comparison:

| Type | Mutable? |
|---|---|
| list | Yes |
| dict | Yes |
| set | Yes |
| tuple | No |
| str | No |
| int | No |

Explain why this matters for:

- function arguments
- dictionary keys
- bugs
- copying

---

# 13. Data Structure Selection

Create scenario exercises:

> Need fast membership lookup?

Use:

```text
set
```

> Need key → value mapping?

Use:

```text
dict
```

> Need ordered mutable sequence?

Use:

```text
list
```

> Need immutable sequence usable as dictionary key?

Use:

```text
tuple
```

Include at least **15 selection questions**.

---

# 14. Notebook 02 — Functions, Classes, and Python Core

Create:

```text
02_Functions_Classes_and_Python_Core.ipynb
```

Cover:

# Functions

```python
def add(a, b):
    return a + b
```

Explain:

- parameters
- arguments
- return values
- default arguments
- keyword arguments
- variable-length arguments

---

# 15. `*args` and `**kwargs`

Explain:

```python
def func(*args):
    ...
```

and:

```python
def func(**kwargs):
    ...
```

Show realistic examples.

Explain:

```python
func(1, 2, 3)
```

and:

```python
func(name="Alice", age=30)
```

---

# 16. Mutable Default Argument Trap

Make this a high-priority Python interview topic.

Bad:

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

Explain why state persists across calls.

Better:

```python
def add_item(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items
```

Provide exercise.

---

# 17. Scope

Explain:

- local
- enclosing
- global
- built-in

Introduce LEGB.

Show examples.

Explain `global` and `nonlocal` briefly.

---

# 18. First-Class Functions

Explain that functions can be:

- assigned to variables
- passed into other functions
- returned from functions

Example:

```python
def apply(fn, x):
    return fn(x)
```

Connect to:

- callbacks
- sorting keys
- ML pipelines

---

# 19. Lambda

Explain:

```python
lambda x: x * 2
```

Use:

```python
items.sort(key=lambda x: x[1])
```

Explain when normal `def` is clearer.

---

# 20. Classes

Explain:

```python
class ModelConfig:
    def __init__(self, name, temperature):
        self.name = name
        self.temperature = temperature
```

Cover:

- class
- instance
- `self`
- attributes
- methods
- constructor

---

# 21. Instance vs Class Variables

Explain with code.

Show common mistake involving mutable class variables.

---

# 22. Inheritance

Explain:

```python
class BaseModel:
    ...

class LLMModel(BaseModel):
    ...
```

Keep concise.

Explain:

- inheritance
- method overriding
- `super()`

Do not overemphasize deep inheritance hierarchies.

---

# 23. Composition

Show:

```python
class RAGService:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
```

Explain why composition is often better than unnecessary inheritance.

This example should be particularly relevant to AI engineering.

---

# 24. Dataclasses

Explain:

```python
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    page: int
    source: str
```

Explain advantages over writing boilerplate classes manually.

---

# 25. Type Hints

Cover:

```python
def embed(text: str) -> list[float]:
    ...
```

Also:

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    ...
```

Use modern Python typing where appropriate.

Explain that type hints improve:

- readability
- IDE support
- static checking

but generally are not runtime enforcement by themselves.

---

# 26. Exceptions

Explain:

```python
try:
    ...
except ValueError:
    ...
finally:
    ...
```

Discuss:

- raising exceptions
- specific vs broad exceptions

Example:

```python
raise ValueError("chunk_size must be positive")
```

---

# 27. Context Managers

Explain:

```python
with open("file.txt") as f:
    text = f.read()
```

Explain why `with` is useful for resource cleanup.

Connect to:

- files
- database transactions
- model inference contexts

---

# 28. Iterators and Generators

Cover:

```python
for item in items:
```

Explain iterable vs iterator conceptually.

Show generator:

```python
def batches(items, batch_size):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
```

Explain benefits:

- lazy evaluation
- memory efficiency

Connect to large AI datasets.

---

# 29. Notebook 03 — Comprehensions and `collections`

Create:

```text
03_Comprehensions_and_Collections.ipynb
```

Cover comprehensively:

# List Comprehension

```python
squares = [x * x for x in range(10)]
```

Compare with normal loop.

---

# 30. Conditional Comprehension

Show:

```python
evens = [
    x
    for x in nums
    if x % 2 == 0
]
```

Then:

```python
labels = [
    "positive" if x > 0 else "negative"
    for x in nums
]
```

Explain difference between filtering and conditional expression.

---

# 31. Dictionary Comprehension

```python
squares = {
    x: x * x
    for x in range(5)
}
```

Use examples such as mapping IDs.

---

# 32. Set Comprehension

```python
lengths = {
    len(word)
    for word in words
}
```

---

# 33. Generator Expressions

```python
total = sum(
    x * x
    for x in nums
)
```

Compare:

```python
[x * x for x in nums]
```

vs:

```python
(x * x for x in nums)
```

Explain memory difference.

---

# 34. Comprehension Readability

Show examples where comprehensions become too complex.

Bad:

```python
...
```

Refactor into normal loop.

Emphasize:

> Short comprehensions are Pythonic. Complex nested logic is often clearer as ordinary code.

---

# 35. `collections`

Make this a major interview section.

Cover:

```python
from collections import (
    Counter,
    defaultdict,
    deque
)
```

Spend most time on these three.

---

# 36. Counter

Explain:

```python
from collections import Counter

count = Counter(nums)
```

Show:

```python
count.most_common(3)
```

Use interview applications:

- frequency counting
- Top K Frequent Elements
- anagrams

---

# 37. defaultdict

Explain:

```python
from collections import defaultdict

groups = defaultdict(list)

for word in words:
    key = tuple(sorted(word))
    groups[key].append(word)
```

Explain why this avoids:

```python
if key not in groups:
    groups[key] = []
```

Connect directly to Group Anagrams.

---

# 38. deque

Explain:

```python
from collections import deque

queue = deque()
```

Cover:

```python
append()
appendleft()
pop()
popleft()
```

Complexities.

Explain why:

```python
list.pop(0)
```

is inefficient.

Compare:

```text
Stack:
list + pop()

Queue:
deque + popleft()
```

Connect directly to:

- BFS
- DFS
- tree traversal

---

# 39. Stack vs Queue

Create visual examples.

Stack:

```text
push
 ↓
[3]
[2]
[1]

pop()
→ 3
```

Queue:

```text
1 → 2 → 3

popleft()
→ 1
```

Explain:

```python
stack.pop()
```

→ LIFO.

```python
queue.popleft()
```

→ FIFO.

---

# 40. Other Useful Standard Library Tools

Briefly cover:

```python
heapq
```

```python
bisect
```

```python
enumerate
```

```python
zip
```

```python
any
```

```python
all
```

```python
sorted(key=...)
```

```python
min(..., key=...)
```

```python
max(..., key=...)
```

These should be concise but practical.

---

# 41. `enumerate`

Explain:

Bad:

```python
for i in range(len(nums)):
    print(i, nums[i])
```

Often cleaner:

```python
for i, value in enumerate(nums):
    print(i, value)
```

---

# 42. `zip`

Example:

```python
for name, score in zip(names, scores):
    ...
```

Explain common use.

---

# 43. Sorting

Make this important.

Explain:

```python
nums.sort()
```

mutates list.

```python
sorted(nums)
```

returns new list.

Show custom sorting:

```python
items.sort(
    key=lambda x: x[1]
)
```

For nested lists:

```python
arr = [
    [2, 3],
    [1, 5],
    [2, 1]
]

arr.sort()
```

Explain lexicographic ordering:

1. Compare first element.
2. If tied, compare second.
3. Continue if necessary.

---

# 44. Notebook 04 — NumPy for AI Engineers

Create:

```text
04_NumPy_for_AI_Engineers.ipynb
```

Focus on NumPy knowledge relevant to ML and AI interviews.

Do not turn this into a numerical-computing course.

---

# 45. Arrays

Explain:

```python
import numpy as np

x = np.array([1, 2, 3])
```

Compare:

```text
Python list
vs
NumPy ndarray
```

Explain:

- homogeneous numerical representation
- vectorized operations
- efficient numerical computation

---

# 46. Shape and Dimension

Cover:

```python
x.shape
x.ndim
x.size
x.dtype
```

Example:

```python
x = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```

Explain:

```text
shape = (2, 3)
```

---

# 47. Array Creation

Cover:

```python
np.zeros()
np.ones()
np.arange()
np.linspace()
np.random.randn()
```

Use ML-oriented examples.

---

# 48. Indexing and Slicing

Cover 1D and 2D.

```python
x[0]
x[:, 0]
x[0, :]
x[:2, 1:]
```

Visualize rows and columns.

---

# 49. Boolean Masking

Show:

```python
x[x > 0]
```

Example:

```python
scores[scores >= 0.5]
```

Explain usefulness in ML preprocessing.

---

# 50. Vectorization

Compare:

Python loop:

```python
result = []

for x in nums:
    result.append(x * 2)
```

with:

```python
result = arr * 2
```

Explain why NumPy vectorization is important.

---

# 51. Broadcasting

Make this important.

Explain:

```python
matrix + scalar
```

and:

```python
matrix + vector
```

Show shapes visually.

Example:

```text
(3, 4)
+
(4,)
```

Explain broadcast compatibility conceptually.

Provide exercises.

---

# 52. Reshape

Cover:

```python
x.reshape(...)
```

```python
x.flatten()
```

```python
x.ravel()
```

Explain practical examples.

---

# 53. Axis

Make this especially clear.

Example matrix:

```text
1 2 3
4 5 6
```

Show:

```python
x.sum(axis=0)
```

→ column-wise reduction.

```python
x.sum(axis=1)
```

→ row-wise reduction.

Explain visually.

---

# 54. Aggregation

Cover:

```python
np.sum
np.mean
np.std
np.min
np.max
np.argmax
```

Connect to ML tasks.

---

# 55. Matrix Multiplication

Explain:

```python
A @ B
```

versus:

```python
A * B
```

Make this a major interview distinction.

Show:

```text
* → element-wise multiplication

@ → matrix multiplication
```

Connect to neural networks:

```text
X @ W + b
```

---

# 56. Dot Product

Show:

```python
np.dot(a, b)
```

Explain simple vector dot product.

Connect to:

- neural networks
- cosine similarity
- embeddings

---

# 57. NumPy Interview Exercises

Include at least **20 exercises**, such as:

- normalize a vector
- standardize columns
- find max value by row
- calculate cosine similarity
- reshape image data
- filter predictions
- matrix multiplication
- one-hot encoding manually

---

# 58. Notebook 05 — pandas for AI Engineers

Create:

```text
05_Pandas_for_AI_Engineers.ipynb
```

Focus on data analysis and preprocessing expected for AI/ML interviews.

---

# 59. DataFrame Basics

Explain:

```python
import pandas as pd

df = pd.DataFrame(...)
```

Cover:

```python
df.head()
df.shape
df.columns
df.dtypes
df.info()
df.describe()
```

---

# 60. Selecting Columns and Rows

Cover:

```python
df["age"]
```

```python
df[["age", "income"]]
```

```python
df.loc[]
```

```python
df.iloc[]
```

Clearly explain `loc` vs `iloc`.

---

# 61. Filtering

Examples:

```python
df[df["age"] > 30]
```

Multiple conditions:

```python
df[
    (df["age"] > 30)
    & (df["country"] == "SG")
]
```

Explain why parentheses are necessary.

---

# 62. Missing Data

Cover:

```python
df.isna()
df.isna().sum()
df.dropna()
df.fillna()
```

Explain:

- mean
- median
- mode
- domain-specific handling

Connect to ML leakage:

Fit preprocessing statistics using training data.

---

# 63. Sorting

```python
df.sort_values(
    "score",
    ascending=False
)
```

---

# 64. GroupBy

Make important.

Show:

```python
df.groupby("country")["salary"].mean()
```

Then:

```python
df.groupby("country").agg(
    mean_salary=("salary", "mean"),
    users=("salary", "count")
)
```

Explain split-apply-combine concept.

---

# 65. Merge

Explain:

```python
pd.merge(
    users,
    predictions,
    on="user_id",
    how="left"
)
```

Connect to SQL JOIN.

Create visual comparison.

---

# 66. Apply vs Vectorized Operations

Show:

```python
df["income"] * 1.1
```

preferred where possible over:

```python
df["income"].apply(...)
```

Explain vectorization.

Do not say `apply` is always bad.

---

# 67. `value_counts`

Show:

```python
df["label"].value_counts()
```

and:

```python
df["label"].value_counts(
    normalize=True
)
```

Connect to class imbalance analysis.

---

# 68. Duplicates

Cover:

```python
df.duplicated()
df.drop_duplicates()
```

Explain why duplicate records can affect ML evaluation.

---

# 69. Datetime Basics

Briefly show:

```python
pd.to_datetime(...)
```

and extracting:

```python
df["date"].dt.year
df["date"].dt.month
df["date"].dt.dayofweek
```

Connect to feature engineering.

---

# 70. pandas ML Mini Exercise

Create a small synthetic dataset.

Tasks:

1. Inspect shape.
2. Identify missing values.
3. Remove duplicates.
4. Fill missing age with median.
5. Calculate target distribution.
6. Filter a subset.
7. Group by category.
8. Join predictions.
9. Create a new feature.
10. Export clean result.

---

# 71. Notebook 06 — Clean Python and Interview Patterns

Create:

```text
06_Clean_Python_and_Interview_Patterns.ipynb
```

Focus on writing Python that is easy to explain during interviews.

---

# 72. Naming

Compare:

Bad:

```python
a = {}
x = []
```

Better:

```python
frequency = {}
results = []
```

Explain clear names improve live interview communication.

---

# 73. Small Functions

Compare one 50-line function with several small functions.

Explain:

- testability
- readability
- debugging

---

# 74. Early Returns

Bad:

```python
if root:
    ...
```

Better:

```python
if not root:
    return None
```

Explain reducing nested logic.

---

# 75. Avoid Repeated Work

Example:

Bad:

```python
if sorted(word) in groups:
    groups[sorted(word)].append(word)
```

Better:

```python
key = tuple(sorted(word))

if key in groups:
    ...
```

Explain:

- cleaner
- avoids recomputation
- creates a usable immutable key

---

# 76. Pythonic but Readable

Show good uses of:

- `enumerate`
- `zip`
- `defaultdict`
- `Counter`
- comprehensions

Warn against excessively clever one-liners.

---

# 77. Input Edge Cases

Teach checking:

- empty input
- one element
- duplicates
- negative numbers
- `None` when appropriate
- very large input

Create checklist.

---

# 78. Complexity Analysis

Teach how to state complexity.

Example:

```python
seen = set()

for x in nums:
    if x in seen:
        return True
    seen.add(x)
```

Explain:

```text
Time: O(n)
Space: O(n)
```

Compare nested loops:

```text
O(n²)
```

sorting:

```text
O(n log n)
```

dictionary/set lookups:

average:

```text
O(1)
```

---

# 79. Common Python Complexity Table

Create:

| Operation | Complexity |
|---|---|
| list index | O(1) |
| list append | amortized O(1) |
| list membership | O(n) |
| list sort | O(n log n) |
| dict lookup | average O(1) |
| set lookup | average O(1) |
| deque append/popleft | O(1) |
| heap push/pop | O(log n) |

---

# 80. Common Python Interview Bugs

Create examples covering:

## Infinite pointer loop

For example forgetting:

```python
left += 1
right -= 1
```

## Wrong range endpoint

```python
range(2, len(nums) - 1)
```

when final index is needed.

## Wrong return variable

Calculating into:

```python
prev1
```

but returning an unused array.

## Mutable default arguments

## Modifying list while iterating

## `is` vs `==`

## Off-by-one errors

## Dictionary key mismatch

## Forgetting to handle duplicate elements

Provide debugging exercises.

---

# 81. `is` vs `==`

Explain:

```python
a == b
```

compares values.

```python
a is b
```

checks object identity.

Use:

```python
x is None
```

as standard example.

---

# 82. Truthiness

Explain:

```python
if not nums:
```

instead of:

```python
if len(nums) == 0:
```

Explain false-like values:

- `None`
- `False`
- `0`
- `""`
- `[]`
- `{}`

---

# 83. Notebook 07 — LeetCode Patterns for AI Engineers

Create:

```text
07_LeetCode_Patterns_for_AI_Engineers.ipynb
```

The goal is **not to solve hundreds of LeetCode problems**.

Teach the reusable patterns most likely to appear in software/AI Engineer interviews.

Cover:

1. Hash map
2. Set
3. Two pointers
4. Sliding window
5. Stack
6. Queue / BFS
7. DFS
8. Binary search
9. Heap
10. Basic dynamic programming

Spend more time on the first eight.

---

# 84. Pattern 1 — Hash Map

Use:

**Two Sum**

Start with brute force:

```text
O(n²)
```

Then hash map:

```text
O(n)
```

Explain step-by-step.

---

# 85. Pattern 2 — Frequency Map

Use:

**Valid Anagram**

and:

**Group Anagrams**

Show approaches:

- sorting key
- character-count key

Explain tuple keys.

---

# 86. Pattern 3 — Set

Use:

**Contains Duplicate**

Explain why set reduces lookup from linear to average constant time.

---

# 87. Pattern 4 — Two Pointers

Use:

**Valid Palindrome**

Show:

```text
L →       ← R
```

Move pointers inward.

Include punctuation skipping.

Make sure implementation correctly moves pointers after comparisons.

---

# 88. Pattern 5 — Sliding Window

Use:

**Longest Substring Without Repeating Characters**

Visualize:

```text
a b c a b c b b
L     R
```

Explain:

- left pointer
- right pointer
- seen dictionary
- why previous duplicate index must be inside current window

Specifically explain condition:

```python
seen[ch] >= left
```

---

# 89. Pattern 6 — Stack

Use:

**Valid Parentheses**

Explain LIFO visually.

---

# 90. Pattern 7 — BFS

Use binary tree traversal.

Show:

```python
queue = deque([root])

while queue:
    node = queue.popleft()
```

Explain why queue produces level-order traversal.

---

# 91. Pattern 8 — DFS

Show iterative:

```python
stack = [root]

while stack:
    node = stack.pop()
```

Explain why stack produces depth-first traversal.

Compare:

```text
Stack + pop()
→ DFS

Queue + popleft()
→ BFS
```

---

# 92. Recursive vs Iterative DFS

Show both.

Explain:

- recursion is concise
- explicit stack avoids recursion-depth issues

---

# 93. Binary Search

Use:

```text
sorted array
```

Show:

```python
while left <= right:
    mid = (left + right) // 2
```

Explain invariants.

Include:

- exact target search
- lower-bound concept
- rotated-array intuition briefly if appropriate

---

# 94. Heap

Explain:

```python
import heapq
```

Python heap is a min-heap.

Cover:

```python
heapq.heappush()
heapq.heappop()
```

Use:

**Top K Frequent Elements**

or:

**Kth Largest Element**

Explain when heap is useful.

---

# 95. Dynamic Programming Basics

Keep this concise.

Use:

**Climbing Stairs**

Show recurrence:

```text
dp[i] = dp[i-1] + dp[i-2]
```

Then:

**House Robber**

```text
dp[i] =
max(
    dp[i-1],
    dp[i-2] + nums[i]
)
```

Explain:

- state
- transition
- base case

Do not turn this notebook into a full DP course.

---

# 96. Interview Problem-Solving Framework

For every coding question teach:

```text
1. Clarify the problem
2. Give simple example
3. State brute-force solution
4. Identify bottleneck
5. Choose data structure/pattern
6. Write code
7. Test manually
8. Discuss complexity
9. Mention edge cases
```

Make this highly visible.

---

# 97. Think-Aloud Example

Provide an interview-style walkthrough for Two Sum.

Example structure:

> I could compare every pair, which would take O(n²). Since I need to repeatedly ask whether the complement has already appeared, a dictionary gives average O(1) lookup. I'll scan once, store each value and index, and check whether `target - current` already exists.

Use similar explanations for several problems.

---

# 98. Required LeetCode Practice Problems

Include guided exercises for at least:

### Arrays / Hashing

1. Contains Duplicate
2. Valid Anagram
3. Two Sum
4. Group Anagrams
5. Top K Frequent Elements

### Two Pointers

6. Valid Palindrome
7. Two Sum II
8. 3Sum

### Sliding Window

9. Best Time to Buy and Sell Stock
10. Longest Substring Without Repeating Characters

### Stack

11. Valid Parentheses

### Binary Search

12. Binary Search
13. Find Minimum in Rotated Sorted Array

### Trees

14. Invert Binary Tree
15. Maximum Depth of Binary Tree
16. Same Tree
17. Balanced Binary Tree

### Dynamic Programming

18. Climbing Stairs
19. House Robber
20. Coin Change

For each problem provide:

- problem summary
- pattern
- intuition
- starter code
- hints
- solution
- complexity
- common mistakes

---

# 99. Difficulty Strategy

Label each:

🟢 Essential Easy

🟠 Essential Medium

🔵 Optional

The focus should be interview patterns, not accumulating problem count.

---

# 100. Notebook 08 — AI Engineer Python Mock Interview

Create:

```text
08_AI_Engineer_Python_Mock_Interview.ipynb
```

Simulate a realistic Python interview.

Divide into rounds.

---

# 101. Round 1 — Python Fundamentals

Ask approximately 15 short questions such as:

- list vs tuple?
- dictionary vs set?
- `append` vs `extend`?
- `sort` vs `sorted`?
- `is` vs `==`?
- shallow vs deep copy?
- what is a generator?
- what is `defaultdict`?
- why use `deque`?
- what does `yield` do?
- list comprehension vs generator?
- mutable vs immutable?

Do not immediately show answers.

Include a reveal section afterward.

---

# 102. Round 2 — Debugging

Provide 10 broken code examples.

Ask learner to:

1. identify bug
2. explain why
3. fix it
4. state complexity

Examples should include:

- dictionary key bugs
- pointer bugs
- off-by-one loops
- mutable default arguments
- wrong return value
- list modification
- NumPy shape mismatch

---

# 103. Round 3 — Coding

Give 3 timed problems:

### Problem A

Easy — 10 minutes.

### Problem B

Medium — 20 minutes.

### Problem C

AI-related data-processing task — 20 minutes.

Example AI problem:

Given:

```python
predictions = [
    {"label": "cat", "score": 0.91},
    {"label": "dog", "score": 0.82},
    {"label": "cat", "score": 0.77},
    ...
]
```

Ask:

- group by label
- calculate average confidence
- return top label
- handle empty input

---

# 104. Round 4 — NumPy / pandas

Include tasks:

- calculate vector similarity
- reshape arrays
- normalize rows
- filter DataFrame
- group data
- handle missing values
- join predictions with metadata

---

# 105. Round 5 — Clean-Code Review

Show working but poor-quality code.

Ask learner to refactor.

Focus on:

- names
- duplicated calculations
- deep nesting
- unnecessary data structures
- hidden side effects

---

# 106. Mock Interview Scoring

Create score categories:

```text
Python Fundamentals       /20
Data Structures           /20
Problem Solving           /20
NumPy / pandas            /15
Code Quality              /10
Complexity Analysis       /10
Communication             /5

Total                     /100
```

Give readiness levels:

```text
90–100
Strong

75–89
Interview Ready

60–74
Needs Targeted Review

<60
Review Fundamentals
```

---

# 107. Python Interview Cheat Sheet Notebook

Create:

```text
Python_Interview_Cheat_Sheet.ipynb
```

This should be suitable for a **15–20 minute review immediately before an interview**.

Include compact sections.

---

# 108. Data Structures Cheat Sheet

```python
# List
nums = []
nums.append(x)
nums.pop()

# Dictionary
d = {}
d[key] = value
value = d.get(key, default)

# Set
seen = set()
seen.add(x)

# Queue
from collections import deque
q = deque()
q.append(x)
q.popleft()

# Counter
from collections import Counter
count = Counter(nums)

# defaultdict
from collections import defaultdict
groups = defaultdict(list)
```

---

# 109. Common Patterns Cheat Sheet

## Frequency

```python
count = {}

for x in nums:
    count[x] = count.get(x, 0) + 1
```

## Two Pointers

```python
left = 0
right = len(nums) - 1

while left < right:
    ...
```

## Sliding Window

```python
left = 0

for right in range(len(s)):
    ...
```

## BFS

```python
queue = deque([root])

while queue:
    node = queue.popleft()
```

## DFS

```python
stack = [root]

while stack:
    node = stack.pop()
```

## Binary Search

```python
left = 0
right = len(nums) - 1

while left <= right:
    mid = (left + right) // 2
```

---

# 110. NumPy Cheat Sheet

Include:

```python
x.shape
x.reshape(...)
x.mean(axis=0)
x.sum(axis=1)
x.argmax(axis=1)

x * y
x @ y

x[x > 0]
```

Explain axis very briefly.

---

# 111. pandas Cheat Sheet

Include:

```python
df.head()
df.shape
df.info()

df["column"]

df[df["age"] > 30]

df.groupby("label").size()

df.sort_values("score")

pd.merge(a, b, on="id")

df.isna().sum()

df.drop_duplicates()
```

---

# 112. Complexity Cheat Sheet

```text
List index             O(1)
List append            O(1) amortized
List search            O(n)
List sort              O(n log n)

Dict lookup            O(1) average
Set lookup             O(1) average

Deque append           O(1)
Deque popleft          O(1)

Heap push/pop          O(log n)

Binary search          O(log n)
```

---

# 113. Common Interview Traps Cheat Sheet

Include:

```text
list.pop(0)
→ O(n)
→ use deque for queue

b = a
→ same object

sorted(x)
→ returns new list

x.sort()
→ modifies list, returns None

dict[key]
→ KeyError if missing

dict.get(key)
→ safe default

is
→ identity

==
→ value equality
```

---

# 114. AI Engineer Python Examples

Throughout all notebooks, include examples relevant to AI work.

Examples:

## Chunk metadata

```python
chunk = {
    "text": "...",
    "page": 4,
    "embedding": [...]
}
```

## Group documents

```python
documents_by_source = defaultdict(list)
```

## Embedding matrix

```python
embeddings.shape
```

## Cosine similarity

```python
similarity = ...
```

## Prediction filtering

```python
high_confidence = [
    pred
    for pred in predictions
    if pred["score"] >= 0.8
]
```

## Batch generator

```python
def batches(items, size):
    ...
```

## FastAPI-style payload

```python
payload = {
    "question": "...",
    "top_k": 5
}
```

The examples should make Python practice feel connected to actual AI engineering.

---

# 115. Exercise Requirements

Across all notebooks create at least:

- 40 Python fundamentals exercises
- 20 NumPy exercises
- 20 pandas exercises
- 20 LeetCode-style problems
- 10 debugging exercises
- 1 full mock interview

Use difficulty labels:

🟢 Easy

🟠 Medium

🔴 Interview Challenge

---

# 116. Exercise Structure

Each exercise should look like:

## Exercise

**Goal**

Clear description.

**Example**

```text
Input:
...

Output:
...
```

**Starter Code**

```python
def solution(...):
    # TODO
    pass
```

**Hint 1**

Collapsed if possible.

**Hint 2**

Collapsed if possible.

**Solution**

Place after the exercise.

**Complexity**

```text
Time:
Space:
```

**Common Mistake**

Explain one likely bug.

---

# 117. Testing

Teach lightweight testing.

Example:

```python
assert two_sum(
    [2, 7, 11, 15],
    9
) == [0, 1]
```

Encourage testing:

- normal case
- empty case
- duplicates
- boundary case

For some exercises include:

```python
def run_tests():
    ...
```

---

# 118. Visualization Requirements

Since this is Jupyter, use Markdown diagrams and lightweight Python output where useful.

Prioritize visual explanations for:

1. list references
2. hash tables
3. stack
4. queue
5. BFS
6. DFS
7. two pointers
8. sliding window
9. binary search
10. NumPy dimensions
11. broadcasting
12. matrix multiplication
13. pandas JOINs
14. dynamic programming state transitions

Do not require heavy visualization dependencies.

Use matplotlib only when a plot genuinely helps.

---

# 119. Notebook Navigation

At the top of every notebook include:

- notebook objectives
- estimated study/practice time
- prerequisites
- section table of contents
- interview-priority labels

At the end include:

- key takeaways
- mistakes to avoid
- 10 rapid-fire interview questions
- readiness checklist

---

# 120. Priority Labels

Use:

🔴 **Must Know**

🟠 **Important**

🟢 **Good to Know**

## 🔴 Must Know

- list
- dict
- set
- tuple
- mutability
- references
- functions
- comprehensions
- `Counter`
- `defaultdict`
- `deque`
- sorting
- complexity
- NumPy shapes
- NumPy indexing
- broadcasting
- matrix multiplication
- pandas filtering
- pandas groupby
- pandas merge
- hash-map patterns
- two pointers
- sliding window
- BFS
- DFS
- binary search

## 🟠 Important

- generators
- dataclasses
- decorators at a basic level
- exceptions
- context managers
- heap
- basic DP
- pandas datetime
- connection between Python structures and AI data pipelines

## 🟢 Good to Know

- metaclasses
- advanced decorators
- descriptors
- Python internals
- advanced NumPy stride internals

Do not spend interview-preparation time on obscure Python language features.

---

# 121. Interview Questions

Across the notebook collection include at least **100 short interview questions**.

Examples:

> List vs tuple?

> Set vs dictionary?

> Why are dictionary lookups usually O(1)?

> Why must dictionary keys be hashable?

> What is mutable vs immutable?

> Shallow copy vs deep copy?

> `append` vs `extend`?

> `sort` vs `sorted`?

> `is` vs `==`?

> Generator vs list?

> What does `yield` do?

> Why use `deque` instead of list for BFS?

> What is `defaultdict`?

> What is `Counter`?

> What does `enumerate` do?

> What does `zip` do?

> NumPy `*` vs `@`?

> What is broadcasting?

> What does `axis=0` mean?

> `loc` vs `iloc`?

> `WHERE`-style filtering in pandas?

> What is the time complexity of set lookup?

> BFS vs DFS?

> When would you use a heap?

For each provide:

- short answer
- interview-quality answer where necessary

---

# 122. Rapid-Fire Quiz

Create a combined question bank with at least **120 questions**.

Examples:

> Which collection gives average O(1) membership lookup?

Set.

> Which type is immutable: list or tuple?

Tuple.

> What does `dict.get()` help avoid?

KeyError.

> Which collection is ideal for BFS?

`deque`.

> What does `popleft()` remove?

The leftmost/front item.

> Does `sorted()` mutate the input list?

No.

> Does `list.sort()` return the sorted list?

No. It sorts in place and returns `None`.

> What does `yield` create?

A generator function.

> What is NumPy broadcasting?

Rules for applying operations to compatible differently shaped arrays.

> `A * B` vs `A @ B`?

Element-wise vs matrix multiplication.

---

# 123. Final Readiness Checklist

Create a combined checklist.

## Python Core

- [ ] I can choose between list, dict, set, and tuple.
- [ ] I understand mutability.
- [ ] I understand references and copying.
- [ ] I can explain `append` vs `extend`.
- [ ] I can explain `sort` vs `sorted`.
- [ ] I can explain `is` vs `==`.
- [ ] I understand dictionary hashing at a high level.
- [ ] I can use functions and classes comfortably.
- [ ] I understand default arguments.
- [ ] I understand generators.

## Collections

- [ ] I can use `Counter`.
- [ ] I can use `defaultdict`.
- [ ] I can use `deque`.
- [ ] I understand stack vs queue.
- [ ] I can use `heapq` at a basic level.

## NumPy

- [ ] I understand arrays and shapes.
- [ ] I can index 1D and 2D arrays.
- [ ] I understand `axis`.
- [ ] I understand broadcasting.
- [ ] I understand vectorization.
- [ ] I know `*` vs `@`.
- [ ] I can calculate simple vector similarity.

## pandas

- [ ] I can inspect a DataFrame.
- [ ] I can filter rows.
- [ ] I can handle missing data.
- [ ] I can use `groupby`.
- [ ] I can merge DataFrames.
- [ ] I can inspect class distributions.

## Interview Coding

- [ ] I can use a hash map.
- [ ] I can use a set.
- [ ] I understand two pointers.
- [ ] I understand sliding window.
- [ ] I understand stack.
- [ ] I understand BFS.
- [ ] I understand DFS.
- [ ] I understand binary search.
- [ ] I understand a heap.
- [ ] I understand basic DP.
- [ ] I can state time complexity.
- [ ] I can state space complexity.
- [ ] I can test edge cases.
- [ ] I can explain my approach while coding.

---

# 124. Technical Requirements

The generated notebooks must:

- use Python 3.11+
- run cleanly in Jupyter
- be compatible with VS Code Jupyter notebooks
- not require a GPU
- avoid paid APIs
- avoid external credentials
- use small synthetic datasets where data is necessary
- contain reproducible random seeds where relevant

Required libraries should be limited primarily to:

```text
numpy
pandas
matplotlib
```

Use Python standard library for everything else where possible.

Provide an environment setup section with:

```bash
conda create -n python-ai-interview python=3.11 -y
conda activate python-ai-interview
pip install jupyter numpy pandas matplotlib ipykernel
python -m ipykernel install --user --name python-ai-interview --display-name "Python AI Interview"
```

Explain briefly why registering the environment as a Jupyter kernel is useful.

---

# 125. Code Quality Requirements

All code must:

- run from top to bottom
- use clear variable names
- avoid unnecessary abstractions
- follow modern Python style
- use type hints where they improve clarity
- include comments only where they add value
- avoid overly clever one-liners
- avoid hidden state between unrelated exercises

Solutions should prioritize **interview readability** over micro-optimizations.

---

# 126. Final Outcome

After completing this notebook collection, I should be able to confidently:

```text
Python Core
     ↓
Data Structures
     ↓
Standard Library
     ↓
NumPy / pandas
     ↓
Problem-Solving Patterns
     ↓
Clean Interview Code
     ↓
AI Engineer Interview
```

I should be able to:

- choose the correct Python data structure quickly
- understand Python references and mutability
- write functions and simple classes
- use comprehensions appropriately
- use `Counter`, `defaultdict`, and `deque`
- manipulate NumPy arrays
- perform basic pandas data analysis
- write clean Python
- debug common Python mistakes
- solve common interview coding patterns
- explain time and space complexity
- communicate my approach clearly during live coding
- apply Python concepts to practical AI-engineering tasks

Finish the final notebook with:

> **If you can solve the essential exercises without looking at the solutions, explain your complexity, and clearly describe why you selected each data structure, your Python foundation is strong enough for the coding portion of many AI Engineer interviews.**