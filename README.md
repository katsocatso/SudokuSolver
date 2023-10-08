# Documentation

## Input Format
Input should be given as one row per line, each cell separated by spaces. Note that 0's represent blank cells in the puzzle.
easy.txt, medium.txt, hard.txt, and evil.txt contain correctly formatted input for the easy, medium, hard, and evil puzzles.
The answers to these puzzles are contained in <difficulty>-answer.txt where difficulty is the respective difficulty.

## Version A
To run Version A, use the following command:
```python sudokuA.py < <input.txt>```
where <input.txt> is your input file.

## Version B
To run Version B, use the following command:
```python sudokuB.py < <input.txt>```
where <input.txt> is your input file.

## Version C
To run Version C, use the following command:
```python sudokuC.py < <input.txt>``` 
where <input.txt> is your input file.

## Good to Knows
While the program is running, it will print out the number of nodes each time it is incremented. This is just for me to know when it is a good time to quit the program if the node count is too high, feel free to comment that line out.

The program prints out the solved puzzle and execution time at the end, or that the puzzle is unsolvable if that is the case.