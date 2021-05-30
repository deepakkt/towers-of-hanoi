# towers-of-hanoi
Towers of Hanoi in Python - both recursive and non-recursive

### Inspiration
Though Towers of Hanoi is a classical recursion problem, I couldn't find any non-recursive implementation of the solution. So this does both the recursive and non-recursive approaches and compares the time difference.

### Observations
Recursive runs a tad faster. It is undoubtedly more elegant and clean. The slowness of the non-recursive is due to the array manipulation of sub-ops. If you think the non-recursive bit can be implemented or optimized better, please let me know as an issue comment

### Timings
```
15 stacks
Completed in 32767 ops
Recursive => 0.08284
Non Recursive => 3.19260
```
