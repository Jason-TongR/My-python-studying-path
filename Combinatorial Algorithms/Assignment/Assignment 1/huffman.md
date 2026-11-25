# Programming Assignment: Huffman Codes
### Combinatorial Algorithms
### Guangdong Technion Israel Institute of Technology

## 🧩 Problem

Alice wants to send a long text to Bob over a channel in which every bit costs money. Writing every character with the same number of bits wastes bits on a text in which a few characters are very frequent, so Alice wants to give frequent characters short codewords and rare characters long ones. Bob must be able to recover the text exactly, from the bits alone.

In this assignment you will implement **Huffman coding** from scratch: you will count the frequencies of the characters of a text, build the optimal prefix code by Huffman's greedy algorithm, encode the text, decode it again, and package everything so that the compressed text carries the code it needs. You will build the whole pipeline as a collection of **small, independent modules** that you can test one by one, and you will explain how it works by **tracing its execution** on concrete inputs.

The protocol is the following. Alice compresses her text into a string of bits that starts with a description of her code tree (the **header**), followed by the encoded text (the **payload**). Bob receives only this string of bits, rebuilds the code tree from the header, and decodes the payload.

> **Groups.** This assignment must be completed in groups. All members of the group must be able to present and defend the project and the design and implementation choices they made.

> **Specifications and traces.** Every function carries its specification as `# require:` and `# ensure:` comments, the structure of the code must make the algorithm visible, and the report explains the code by **execution traces** (see the Submission section).

## 🏗️ Design: modules and layers

Your implementation must be organised in **layers**, listed below from top to bottom. A module may use only the modules in the rows **below** it, never those above it, and only the driver programs may print.

| Layer | Module | Functions | Responsibility |
|---|---|---|---|
| drivers | `table.py`, `compress.py`, `decompress.py` | none (they only call the package) | read the command line and print; nothing else |
| codec | `codec.py` | `compress`, `decompress`, `encode`, `decode` | turn texts into bits and bits into texts |
| header | `header.py` | `tree2bits`, `bit2tree` | write a tree as bits and read it back |
| codes | `codes.py` | `codewords`, `cost`, `budget`, `prefixfree` | read a code off a tree and measure it |
| builder | `builder.py` | `build` (and your helpers) | Huffman's greedy algorithm |
| trees | `trees.py` | `leaves`, `depths`, `follow` | manipulate trees |
| frequencies | `frequencies.py` | `frequencies` | count the characters of a text |

The following rules are part of the assignment, and they are graded.

- **One responsibility per function.** If you need the word "and" to describe what a function does, split it. Small helper functions with descriptive names are encouraged; a function should fit on one screen (about 20 lines).
- **Pure functions.** No function inside the package prints, reads input, uses global variables, or modifies its arguments.
- **No duplicated logic.** For example, reading the codewords off a tree is done once, in `codewords`, and every module that needs codewords calls it.
- **Each module can be tested alone**, without the modules above it.
- **Specification first.** Write the `# require:` and `# ensure:` comments of a function before its body, and write the body so that the specification is true.

## 📐 Algorithms

- A **tree** is either a **leaf**, a string with exactly one character, or an **internal node**, a pair `(left, right)` of two trees (the representation used in the lectures). A tree is a leaf exactly when `isinstance(tree, str)`.
- A **code** is a dictionary from characters to codewords `dict[str, str]`.
- A **codeword** is a string of `'0'` and `'1'`.
- Going left in a tree appends `'0'` and going right appends `'1'`.

> **Note.** A string of length 1 is what other languages call a *char*. Python has no separate type for it, so type hints use `str`.

You must implement the functions below, in the module indicated. Each example shows a call and its result.

### Frequencies: `frequencies`

```python
def frequencies(text: str) -> dict[str, int]:
    # require: text is not empty
    # ensure: the keys are exactly the characters of text, in the order of their first
    #         appearance; each value is the number of occurrences of its key;
    #         the values add up to len(text)
```

**Example:** `frequencies("abracadabra")` gives `{'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}`.

### Huffman's algorithm: `build`

```python
def build(freq: dict[str, int]) -> Tree:
    # require: freq has at least two keys, and every frequency is positive
    # ensure: the leaves of the result are exactly the keys of freq, each once;
    #         every internal node has two children;
    #         the code given by the tree has the smallest cost B among all prefix codes
```

This is the greedy algorithm of the lectures: start with one leaf per character of `freq`, and repeatedly merge the **two lightest** trees into a new tree whose frequency is the sum of theirs, until a single tree is left; that tree is the result. How you represent the trees that are waiting to be merged, and how you find the two lightest ones, is your design choice (`bisect` and `heapq` are available if you want a sorted structure).

**Tie-breaking.** Several trees can have the same frequency, so the rule for choosing among them is part of the specification: it makes every correct solution produce **the same tree**. The leaves are created in the **alphabetical order of their characters** (the order of `sorted(freq)`), and each merged tree is created after all the trees that existed before the merge. Among trees of equal frequency, the one created **earlier** is chosen first. Of the two trees chosen for a merge, the **first** becomes the **left** child and the **second** the **right** child of the new tree. Different tie-breaking rules give different codes of the same cost, but you must follow this one.

**Examples:**
- `build({'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5})` gives `('a', (('c', 'b'), (('f', 'e'), 'd')))`.
- `build(frequencies("abracadabra"))` gives `('a', (('c', 'd'), ('b', 'r')))`.

### Manipulating trees: `leaves`, `depths`, `follow`

```python
def leaves(tree: Tree) -> list[str]:
    # ensure: the result lists the leaves of tree from left to right

def depths(tree: Tree) -> dict[str, int]:
    # ensure: the keys are the leaves of tree, from left to right;
    #         the value of a leaf is the number of edges from the root to it

def follow(tree: Tree, bits: str) -> Tree:
    # require: bits describes a path from the root of tree that does not go below a leaf
    # ensure: the result is the subtree reached from the root by going left on '0' and right on '1'
```

**Examples,** for `tree = ('a', (('c', 'b'), (('f', 'e'), 'd')))`:
- `leaves(tree)` gives `['a', 'c', 'b', 'f', 'e', 'd']`.
- `depths(tree)` gives `{'a': 1, 'c': 3, 'b': 3, 'f': 4, 'e': 4, 'd': 3}`.
- `follow(tree, "1101")` gives `'e'`, and `follow(tree, "11")` gives `(('f', 'e'), 'd')`.

### Codes: `codewords`, `cost`, `budget`, `prefixfree`

```python
def codewords(tree: Tree) -> dict[str, str]:
    # ensure: the keys are the leaves of tree, from left to right;
    #         the codeword of a leaf is the labels of the path from the root to it
    #         ('0' for left, '1' for right)

def cost(freq: dict[str, int], codes: dict[str, str]) -> int:
    # require: codes has a codeword for every key of freq
    # ensure: the result is the sum over all characters c of freq[c] * len(codes[c]),
    #         the number of bits needed to encode a text with these frequencies

def budget(freq: dict[str, int]) -> int:
    # require: freq has at least two keys
    # ensure: the result is b * (the sum of the frequencies), where b is the smallest
    #         number of bits with 2**b >= the number of characters (a fixed-length code)

def prefixfree(codes: dict[str, str]) -> bool:
    # ensure: the result is True exactly when no codeword is a prefix of another codeword
```

Compute `b` in `budget` with a loop; the `math` module is not allowed.

**Examples,** with `freq = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}` and `codes` the code of its tree:
- `codewords(tree)` gives `{'a': '0', 'c': '100', 'b': '101', 'f': '1100', 'e': '1101', 'd': '111'}`.
- `cost(freq, codes)` gives `224`, and `budget(freq)` gives `300`.
- `prefixfree({'a': '0', 'b': '10', 'c': '11'})` gives `True`, and `prefixfree({'a': '0', 'b': '01'})` gives `False`.

### Encoding and decoding: `encode`, `decode`

```python
def encode(text: str, codes: dict[str, str]) -> str:
    # require: codes has a codeword for every character of text
    # ensure: the result is the concatenation of the codewords of the characters of text, in order

def decode(bits: str, tree: Tree) -> str:
    # require: bits is the encoding of some text with the code of tree
    # ensure: the result is that text; that is, encode(result, codewords(tree)) == bits
```

`decode` must **walk the tree**: starting at the root, go left or right according to each bit; when a leaf is reached, output its character and return to the root. It must not search the table of codewords.

**Example,** with the tree of `"abracadabra"` and its code `{'a': '0', 'c': '100', 'd': '101', 'b': '110', 'r': '111'}`: `encode("abracadabra", codes)` gives `'01101110100010101101110'` (23 bits), and `decode` of that string gives back `"abracadabra"`.

### The header: `tree2bits`, `bit2tree`

For the receiver to rebuild the tree, the tree itself must be written in bits. We use a **preorder** description:

- an **internal node** is written as `'0'`, followed by the description of its left subtree and then that of its right subtree;
- a **leaf** is written as `'1'`, followed by the **7-bit binary ASCII code** of its character.

A tree with `n` leaves therefore takes `(2n − 1) + 7n` bits.

```python
def tree2bits(tree: Tree) -> str:
    # ensure: the result is the preorder description of tree, of length (2n - 1) + 7n

def bit2tree(bits: str, i: int = 0) -> tuple[Tree, int]:
    # require: bits[i:] starts with the description of a tree (it may continue with other bits)
    # ensure: the result is (tree, j), where tree is the tree described starting at position i
    #         and j is the position right after that description
```

The second result of `bit2tree` is what makes the header **self-delimiting**: the decoder knows where the header ends and the payload begins without any separator or length field.

**Examples:**
- `tree2bits(('a', ('b', 'c')))` gives `'01110000101110001011100011'` (26 bits).
- `bit2tree('01110000101110001011100011')` gives `(('a', ('b', 'c')), 26)`. If the string continues with other bits, the result is the same.

### Compression: `compress`, `decompress`

```python
def compress(text: str) -> str:
    # require: text consists of printable ASCII characters (codes 32 to 126),
    #          with at least two distinct characters
    # ensure: the result is the header of the Huffman tree of text followed by the encoding of text;
    #         its length is (2n - 1) + 7n + B, where B is the cost of the code

def decompress(bits: str) -> str:
    # require: bits is the result of compress on some text
    # ensure: the result is that text
```

**Example:** `compress("abracadabra")` gives

```
0111000010011100011111001000111000101111001001101110100010101101110
```

which has 67 bits: a header of 44 bits followed by a payload of 23 bits. `decompress` of this string gives back `"abracadabra"`.

## ⚠️ Constraints

| Item | Constraint |
|---|---|
| command line args | Assume all inputs are valid and in the right format; no need to perform checks |
| Text | Printable ASCII only: codes 32–126, with at least two distinct characters |
| Python | Version 3.10 or later; standard library only |
| Imports | Inside the package, only `bisect`, `heapq`, `sys` and `typing` (for type hints). The optional test file (see the bonus section) may import any standard module |
| Not allowed | Whatever is not explicitly permitted, ask if you have doubts |
| Tie-breaking | Exactly the rule of `build`: leaves created in alphabetical order, ties resolved in favour of the tree created earlier, the first tree chosen is the left child |
| Trees | Leaves are one-character strings, and internal nodes are pairs `(left, right)` (tuples) |
| Bits | Strings of the characters `'0'` and `'1'` (we do not pack bits into bytes) |
| Output functions | `print` only in the three driver programs; never inside the package |
| Purity | No function modifies its arguments, reads input, or uses global variables |
| Execution traces | Produced from **your** code, with your own names (see the report requirements) |

## 💻 Implementation

Your implementation must have three driver programs, one per operation:

```bash
python3 table.py      <text>
python3 compress.py   <text>
python3 decompress.py <bits>
```

When the text contains spaces or punctuation, surround it with quotes in the shell. The drivers only read the command line, call functions of the package, and print.

- `table.py` prints one line per distinct character, in increasing order of the characters, with `repr(character)`, its frequency and its codeword, separated by one space; then a last line `cost B fixed F`, with `B` the cost of the Huffman code and `F` the cost of a fixed-length code.
- `compress.py` prints the compressed bit string, and `decompress.py` prints the recovered text. Nothing else is printed.

**Expected output:**

```
$ python3 table.py abracadabra
'a' 5 0
'b' 2 110
'c' 1 100
'd' 1 101
'r' 2 111
cost 23 fixed 33

$ python3 compress.py abracadabra
0111000010011100011111001000111000101111001001101110100010101101110

$ python3 decompress.py 0111000010011100011111001000111000101111001001101110100010101101110
abracadabra

$ python3 table.py 'to be or not to be'
' ' 5 10
'b' 2 010
'e' 2 011
'n' 1 1100
'o' 4 00
'r' 1 1101
't' 3 111
cost 47 fixed 54

$ python3 compress.py 'to be or not to be'
0011101111011100010111001010101000000011101110111100101111010011100100100111000110110110000111101110010010011

$ python3 decompress.py 0011101111011100010111001010101000000011101110111100101111010011100100100111000110110110000111101110010010011
to be or not to be
```

## 🧪 Bonus Points: Tests

This section is **optional**: a submission without it is complete and is graded as such, and a submission with it earns **bonus points**. To earn them, submit a file `tests.py` that runs with `python3 tests.py` and checks your package. Besides examples of each function (including those of this document), it should contain the following **property tests**, run on a collection of texts that includes texts with spaces and punctuation. Each property is a consequence of an idea from the lectures:

| Property | Idea it checks |
|---|---|
| `prefixfree(codewords(build(freq)))` holds | codes are read off the leaves of a tree |
| `decode(encode(text, codes), tree) == text` and `decompress(compress(text)) == text` | prefix codes decode without separators; the header is self-delimiting |
| the leaves of the tree are exactly the characters, each once, and `depths(tree)` equals the codeword lengths | the tree and the code are the same object |
| `cost(freq, codes)` equals the sum of the weights of the internal nodes of the tree | the cost is the sum of the **merges** |
| `len(compress(text))` equals `(2n − 1) + 7n + cost(freq, codes)` | the size of header and payload |
| `cost(freq, codes) <= budget(freq)` | Huffman never loses to a fixed-length code |

## 🧱 File Structure

There may be other files, but at least you should have:

```
.
├── table.py             ← driver: prints the code table of a text
├── compress.py          ← driver: compresses a text
├── decompress.py        ← driver: decompresses a bit string
├── huffman/
│   ├── __init__.py
│   ├── frequencies.py   ← frequencies
│   ├── trees.py         ← leaves, depths, follow
│   ├── builder.py       ← build and its helpers
│   ├── codes.py         ← codewords, cost, budget, prefixfree
│   ├── header.py        ← tree2bits, bit2tree
│   └── codec.py         ← encode, decode, compress, decompress
├── tests.py             ← (optional, for bonus points) examples and property tests
└── report.pdf           ← written report (see below)
```

## 📦 Submission

Submit a single `.zip` file containing **both** of the following items.

### 1. Source Code

Your Python implementation must run on a standard Unix system with the standard library only. Beyond correctness, the following are required:

- The code must follow the layered design above and the modularization rules (one responsibility per function, pure functions, no duplicated logic).
- Every function must have a header comment describing its purpose, arguments and return value, followed by its `# require:` and `# ensure:` comments.
- Use clear, descriptive names for functions and variables.
- Include all files necessary to run the programs (and the tests, if you submit them for the bonus).
- The programs must be easy to test: inputs are passed as command-line arguments, outputs go to standard output, nothing else is printed.

**You will lose points if any of the above is not satisfied.**

### 2. Report (PDF)

Submit a PDF report covering the following items. **We will not grade a submission without a report.**

- **Team members.** A list of names and student IDs, with a description of each member's contribution to the project.
- **Design.** The module diagram of your solution, and one or two sentences on the responsibility of each module and why each function sits where it does. Mention any helper you added and the reason.
- **Specifications.** The `require` and `ensure` clauses of every function (a table is fine), and for **each clause** a justification of why you added it. For every `require` clause, say what would go wrong without it (an input for which the function fails or returns a wrong result). For every `ensure` clause, say why it is needed: which other function relies on it, or which property of Huffman coding it expresses. Do not just restate the clause: explain it.
- **Explanation.** A description of how and why each algorithm works. Explain in particular: why the greedy choice of `build` is correct (the **exchange argument**, in your own words); why the codewords read off a tree form a prefix code; why the encoded text needs **no separators** between codewords; why the header is **self-delimiting**; why the cost of the tree equals the sum of the weights of its internal nodes; and why different tie-breaking rules change the code but not its cost (which is why this assignment fixes the rule).
- **Execution traces.** This is the core of the report; see below.
- **Reflection.** A brief explanation of: why sender and receiver must share the tree, and how the header affects the compression of short and of long texts (use your numbers: for which texts does compressing not pay off?); and why Huffman's code is not unique although its cost is.

Do not include the full source code listing in the report. You may include short excerpts where they help explain a specific implementation detail. Clear presentation matters: **you will lose points if any of the above is not covered.**

#### Execution traces: what is required

An **execution trace** shows, step by step, **how your implementation of a function works** on a concrete input: the values of the variables of your code after each iteration of a loop or at each recursive call, together with a sentence explaining **what the step does, why, and which line or idea of your code is responsible**. A list of printed values without explanation is **not** a trace and will not be graded as one.

Every trace must satisfy the following.

- It is produced from **your code**, using **your variable and function names**. You can get the values from a debugger or from temporary prints, which you must remove from the submitted code.
- It states the **call** (function and arguments) and the **returned value**, and checks the returned value against the `ensure` clause.
- You **justify your choice of inputs**: say what each input is meant to show.

You must include traces for the following.

1. **`frequencies`** on a text of your own with at least 8 characters and a repeated character: the dictionary after each character.
2. **`build`** on `{'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}`: the trees waiting to be merged at the start and after each of the five iterations, the two trees merged (in the order chosen), and the tree created.
3. **`build`** on a text of your own that produces **a tie** between equal frequencies: show where the tie occurs and how the tie-breaking rule resolves it, and say what would change with a different rule.
4. **`codewords`** on the tree of trace 2: every recursive call with the value of its `prefix`, and what it returns.
5. **`encode` and `decode`** on a short text that contains at least a **letter, a space and a punctuation mark**: for `decode`, for each bit the node reached and the output so far, marking the moments at which the walk **returns to the root**.
6. **`tree2bits` and `bit2tree`** on a tree with at least 4 leaves: the recursion of both, with the value of the position `i` in every call of `bit2tree`, and the position returned at the end.
7. **`compress` and `decompress`** on the text of trace 5: the length of the header, of the payload, and of the whole string, compared with 7 bits per character and with a fixed-length code.

**An example of the style of a trace** (for an input that you may *not* use in your report). We trace `build({'x': 3, 'y': 1, 'z': 2})`. This implementation keeps the trees waiting to be merged as triples `(frequency, creation number, tree)` in a list sorted by the first two components; the leaves get the creation numbers 0, 1, 2 in alphabetical order, and each merged tree gets the next number. Your representation may differ, and your traces must use your own. Here the list holds `(1, 1, 'y')`, `(2, 2, 'z')` and `(3, 0, 'x')`.

| iteration | merged (first, second) | created | waiting afterwards |
|---|---|---|---|
| 1 | `(1, 1, 'y')`, `(2, 2, 'z')` | `(3, 3, ('y', 'z'))` | `(3, 0, 'x')`, `(3, 3, ('y', 'z'))` |
| 2 | `(3, 0, 'x')`, `(3, 3, ('y', 'z'))` | `(6, 4, ('x', ('y', 'z')))` | `(6, 4, ('x', ('y', 'z')))` |

*Iteration 1 merges the first two entries of the sorted list, `y` and `z`, which are the two lightest, as the greedy choice requires, and `y` comes first, so it is the left child; the new entry is inserted in its sorted place. In iteration 2 the two entries both have frequency 3: the tie is resolved by the creation numbers, 0 for `x` and 3 for the new tree, so `x` was created earlier, comes first and becomes the left child. The loop ran `n − 1 = 2` times and one entry is left, so the function returns `('x', ('y', 'z'))`, whose leaves are exactly `x`, `y`, `z`. The invariant (the trees in the queue have disjoint leaves that together are all the characters, and their frequencies add up to 6) held after every iteration.*

## 📄 License

This project is part of the 2026 edition of the Combinatorial Algorithms course at the Guangdong Technion Israel Institute of Technology.

copyright (C) 2026 Valentin Cassano
