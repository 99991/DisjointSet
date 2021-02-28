# Disjoint-set / union-find data structure implementation in pure Python

This data structure is useful for merging disjoint sets of discrete elements. You can read more about it on [https://en.wikipedia.org/wiki/Disjoint-set_data_structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure).

```python
from disjoint_sets import DisjointSets

s = DisjointSets(5)

# Initially, the DisjointSets data structure contains 5 sets.
# {0: [0], 1: [1], 2: [2], 3: [3], 4: [4]}
# For efficiency reasons, the "sets" are actually lists.
print("Initial sets:")
print(s.items())
print()

# Merge set with element 0 and set with element 1.
s.union(0, 1)

# {0: [0, 1], 2: [2], 3: [3], 4: [4]}
print("Sets after 0 and 1 are merged:")
print(s.items())
print()
# 0 is the representative root node for the sets with values [0, 1].
# Values of merged sets have the same representative root values.
root0 = s.find(0)
root1 = s.find(1)
assert(root0 == root1)

# Can also merge directly by root nodes, which is faster if root nodes are
# known. Otherwise, the union function will search for the root nodes.
root3 = s.find(3)
root4 = s.find(4)

# The union functions return which node was removed and which was kept.
# The root belonging to the larger set will be kept.
# If both sets have the same size, the first set is kept.
kept_root, removed_root = s.union_roots(root4, root3)
print("Merging set with roots", root3, "and", root4)
print("Kept root:", kept_root)
print("Removed root:", removed_root)

# {0: [0, 1], 2: [2], 4: [3, 4]}
print(s.items())
print()

s.union(1, 4)

# {0: [0, 1, 3, 4], 2: [2]}
print("After merging sets with values 1 and 4:")
print(s.items())
print()

# Now everything is merged.
s.union(2, 3)

# {0: [0, 1, 2, 3, 4]}
print("After merging sets with values 2 and 3:")
print(s.items())
print()
```

# Is it worth it?

Probably not. Python is not the fastest language. Therefore, data structures which are implemented in pure Python do not fare too well against native data structures.

The following logarithmic plot shows a benchmark of a naive implementation of disjoint sets using lists (`naive`) against the union-find data structure for merging sets using their representative root nodes (`union`), merging sets given two values in those sets (`union + find`) and finding the two sets corresponding to two values (`find 2 values`).

Probably the most interesting comparison here would be `naive` against `union + find`, unless you keep track of set representatives manually (which is possible for some algorithms, but cumbersome). For small numbers of sets, the naive implementation outperforms the union-find data structure. The break-even point occurs at approximately 20,000 sets, which is likely higher than the number in most practical applications that I could come up with.

![Benchmark](https://raw.githubusercontent.com/99991/DisjointSet/main/benchmark.png)

