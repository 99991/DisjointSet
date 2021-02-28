class DisjointSets:
    def __init__(self, n):
        self.sizes = [1] * n
        self.parents = list(range(n))
        self.n = n

    def find_root(self, i):
        parent = i
        while parent != self.parents[parent]:
            parent = self.parents[parent]
        return parent

    def find(self, i):
        root = self.find_root(i)

        # Replace parents of nodes on path with root node
        while i != root:
            tmp = self.parents[i]
            self.parents[i] = root
            i = tmp

        return root

    def union_roots(self, root1, root2):
        # If not unioned yet ...
        if root1 == root2: return

        self.n -= 1

        # ... union smaller set into larger set.
        s1 = self.sizes[root1]
        s2 = self.sizes[root2]
        if s1 >= s2:
            self.sizes[root1] += s2
            self.parents[root2] = root1
            return root1, root2
        else:
            self.sizes[root2] += s1
            self.parents[root1] = root2
            return root2, root1

    def union(self, i, j):
        root1 = self.find(i)
        root2 = self.find(j)

        return self.union_roots(root1, root2)

    def items(self):
        return groupby(range(len(self.sizes)), lambda i: self.find(i))

    def keys(self):
        return self.items().keys()

    def values(self):
        return self.items().values()

    def __len__(self):
        return self.n

def groupby(values, key):
    groups = {}
    for value in values:
        k = key(value)
        if k in groups:
            groups[k].append(value)
        else:
            groups[k] = [value]
    return groups

class NaiveDisjointSets:
    def __init__(self, n):
        self.sets = [[i] for i in range(n)]
        self.counter = 0

    def union_by_index(self, i1, i2):
        if i1 == i2: return

        set1 = self.sets[i1]
        set2 = self.sets[i2]

        if len(set1) > len(set2):
            set1.extend(set2)
            self.counter += len(set2)
            del self.sets[i2]
        else:
            set2.extend(set1)
            self.counter += len(set1)
            del self.sets[i1]

    def __len__(self):
        return len(self.sets)

    def __getitem__(self, i):
        return self.sets[i]

    def __iter__(self):
        yield from self.sets

def benchmark():
    import random
    import time

    random.seed(0)

    print("Running benchmark (this might take a while).\n")

    times = []
    sizes = [2**i for i in range(5, 20)]
    for n in sizes:
        print("Benchmarking size", n)

        ds_smart = DisjointSets(n)
        ds_naive = NaiveDisjointSets(n)

        times.append([0.0] * 4)

        while len(ds_naive) > 1:
            # Randomly choose two sets.
            i1 = random.randrange(len(ds_naive))
            i2 = random.randrange(len(ds_naive))

            set1 = ds_naive[i1]
            set2 = ds_naive[i2]

            # Randomly choose two values from sets.
            value1 = random.choice(set1)
            value2 = random.choice(set2)

            # Union sets.

            t = [0.0] * 4

            t[0] = time.perf_counter()

            ds_naive.union_by_index(i1, i2)

            t[1] = time.perf_counter()

            root1 = ds_smart.find(value1)
            root2 = ds_smart.find(value2)

            t[2] = time.perf_counter()

            ds_smart.union_roots(root1, root2)

            t[3] = time.perf_counter()

            for i in range(3):
                times[-1][i] += t[i + 1] - t[i]
            times[-1][-1] += t[3] - t[1]

    import matplotlib.pyplot as plt
    times = list(zip(*times))
    labels = ["naive", "find 2 sets", "union", "union + find"]
    for t, label in zip(times, labels):
        plt.loglog(sizes, t, label=label)
    plt.legend()
    plt.xlabel("Number of disjoint sets")
    plt.ylabel("Time [seconds]")
    plt.savefig("benchmark.png", dpi=300)
    plt.show()

def test():
    import random
    import time

    random.seed(0)

    for n in range(100):
        ds_smart = DisjointSets(n)
        ds_naive = NaiveDisjointSets(n)

        while len(ds_naive) > 1:
            # Randomly choose two sets.
            i1 = random.randrange(len(ds_naive))
            i2 = random.randrange(len(ds_naive))

            set1 = ds_naive[i1]
            set2 = ds_naive[i2]

            # Randomly choose two values from sets.
            value1 = random.choice(set1)
            value2 = random.choice(set2)

            # Union sets.
            ds_naive.union_by_index(i1, i2)
            ds_smart.union(value1, value2)

            # Check if equal.
            sets1 = frozenset(frozenset(s) for s in ds_naive)
            sets2 = frozenset(frozenset(s) for s in ds_smart.values())

            assert(sets1 == sets2)

    print("Tests passed.\n")

def example():
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

if __name__ == "__main__":
    example()
    test()
    benchmark()
