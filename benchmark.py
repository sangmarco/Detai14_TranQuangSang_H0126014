"""Đo thời gian 4 cách sắp xếp; chỉ dùng thư viện chuẩn Python."""
import argparse
import csv
import platform
import random
import statistics
import sys
import time
from pathlib import Path
from algorithms import merge_sort, quick_sort, quick_sort_threeway


def make_data(n, kind, seed):
    rng = random.Random(seed)
    if kind == 'random':
        return [rng.randint(-100000, 100000) for _ in range(n)]
    if kind == 'ascending':
        return list(range(n))
    if kind == 'descending':
        return list(range(n, 0, -1))
    if kind == 'nearly_sorted':
        a = list(range(n))
        for _ in range(max(1, n // 20)):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if kind == 'duplicates':
        return [rng.randrange(5) for _ in range(n)]
    raise ValueError(kind)


def run(output, sizes, repeats):
    algorithms = {
        'merge': merge_sort,
        'quick_last': quick_sort,
        'quick_random': lambda a: quick_sort(a, random_pivot=True, seed=14),
        'quick_threeway': quick_sort_threeway,
        'python_sorted': sorted,
    }
    kinds = ('random', 'ascending', 'descending', 'nearly_sorted', 'duplicates')
    rows = []
    for kind in kinds:
        for n in sizes:
            values = make_data(n, kind, seed=2026 + n)
            expected = sorted(values)
            for name, algorithm in algorithms.items():
                measurements = []
                for _ in range(repeats):
                    start = time.perf_counter_ns()
                    result = algorithm(values)
                    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
                    assert result == expected, f'Sai ket qua: {name}, {kind}, {n}'
                    measurements.append(elapsed_ms)
                median = statistics.median(measurements)
                rows.append((kind, n, name, repeats, round(median, 5)))
                print(f'{kind:14} n={n:4} {name:15} {median:9.3f} ms')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('data_type', 'n', 'algorithm', 'repeats', 'median_ms'))
        writer.writerows(rows)
    env = output.with_name('moi_truong_thu_nghiem.txt')
    env.write_text(f'Python: {sys.version.split()[0]}\nOS: {platform.platform()}\nCPU: {platform.processor()}\nSizes: {sizes}\nRepeats: {repeats}\nTime: perf_counter_ns; summary: median (ms)\n', encoding='utf-8')
    print('\nDa luu:', output, 'va', env)
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sizes', nargs='+', type=int, default=[300, 800, 1500])
    parser.add_argument('--repeats', type=int, default=5)
    parser.add_argument('--output', default='ket_qua_benchmark.csv')
    args = parser.parse_args()
    run(args.output, args.sizes, args.repeats)
