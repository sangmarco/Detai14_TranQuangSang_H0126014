"""Kiểm tra nhanh tính đúng đắn và tính ổn định của Merge-Sort."""
import random
import unittest
from algorithms import merge_sort, quick_sort, quick_sort_threeway, partition


class SortTests(unittest.TestCase):
    def test_all_algorithms(self):
        samples = [[], [1], [2, 1], [3, 3, 3], [0, -1, -1, 9], list(range(30)), list(range(30, 0, -1))]
        rng = random.Random(2026)
        for n in (0, 1, 2, 10, 50, 100):
            for _ in range(30):
                samples.append([rng.randint(-50, 50) for _ in range(n)])
        for a in samples:
            expected = sorted(a)
            self.assertEqual(merge_sort(a), expected)
            self.assertEqual(quick_sort(a), expected)
            self.assertEqual(quick_sort(a, random_pivot=True), expected)
            self.assertEqual(quick_sort_threeway(a), expected)

    def test_partition(self):
        values = [1, 3, 4, 7, 8, 2, 6, 5]
        pivot = 5
        p = partition(values, 0, len(values) - 1)
        self.assertEqual(values[p], pivot)
        self.assertTrue(all(x <= pivot for x in values[:p]))
        self.assertTrue(all(x > pivot for x in values[p + 1:]))
        self.assertEqual(sorted(values), list(range(1, 9)))

    def test_merge_stability(self):
        class K:
            def __init__(self, key, seq):
                self.key, self.seq = key, seq
            def __le__(self, other):
                return self.key <= other.key
        values = [K(2, 'a'), K(1, 'b'), K(2, 'c'), K(1, 'd')]
        result = merge_sort(values)
        self.assertEqual([x.seq for x in result], ['b', 'd', 'a', 'c'])

    def test_long_sorted_input(self):
        values = list(range(2000))
        self.assertEqual(quick_sort(values), values)
        self.assertEqual(quick_sort_threeway(values), values)

    def test_does_not_change_input(self):
        values = [3, 1, 2, 1]
        initial = values.copy()
        for algorithm in (merge_sort, quick_sort, quick_sort_threeway):
            self.assertEqual(algorithm(values), [1, 1, 2, 3])
            self.assertEqual(values, initial)

    def test_all_permutations_four_elements(self):
        from itertools import permutations
        for values in permutations((1, 2, 3, 4)):
            expected = [1, 2, 3, 4]
            self.assertEqual(merge_sort(values), expected)
            self.assertEqual(quick_sort(values), expected)
            self.assertEqual(quick_sort(values, random_pivot=True, seed=99), expected)
            self.assertEqual(quick_sort_threeway(values, seed=99), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
