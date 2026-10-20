# Gradescope Setup - CSE 568 Project 01: Graph Coloring

This source package is the instructor/autograder package for Project 01.

## Files included

- `setup.sh`
- `run_autograder`
- `requirements.txt`
- `graphs/`
- `deap/` lightweight DEAP-compatible shim used by the autograder

The source package intentionally does **not** include a solved `student_solution.py`.

## Student submission

Students should upload exactly one Python solution file, preferably:

```text
student_solution.py
```

For compatibility, the autograder also accepts `P01_solution.py` or a single submitted `.py` file. If multiple `.py` files are submitted and neither preferred filename is present, the submission fails with a clear message.

## Grading

The autograder loads the student's submitted file directly from `/autograder/submission`. It does not import `student_solution.py` from `/autograder/source`, which prevents accidental false passes caused by a reference solution being left in the source zip.

Point breakdown:

```text
Q1: init_graph builds the graph correctly                         30 points
Q2: eval_graph scores valid, invalid, and partial colorings       35 points
Q3: run_ga returns a high best fitness                            35 points
Total                                                            100 points
```

## Validation checks performed

- A blank/template file with `NotImplementedError` receives `0 / 100`.
- The reference solution receives `100 / 100`.
- If a solved `student_solution.py` is accidentally placed in `/autograder/source`, the autograder still refuses to use it unless the student actually submits a Python file.

## Setup notes

The package is self-contained and does not require internet access during setup. The included `deap/` shim implements the subset of DEAP used by the Project 01 template and reference solution.
