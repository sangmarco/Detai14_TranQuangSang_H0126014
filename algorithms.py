"""Các thuật toán sắp xếp của Đề tài 14; trả về danh sách mới."""
import random


def merge_sort(values):
    a = list(values)
    temp = a.copy()

    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        i, j = lo, mid
        for k in range(lo, hi):
            if j == hi or (i < mid and a[i] <= a[j]):
                temp[k] = a[i]
                i += 1
            else:
                temp[k] = a[j]
                j += 1
        a[lo:hi] = temp[lo:hi]

    sort(0, len(a))
    return a


def partition(a, lo, hi):
    """Lomuto: a[lo:p] <= pivot; a[p+1:hi+1] > pivot."""
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def quick_sort(values, *, random_pivot=False, seed=14):
    a = list(values)
    rng = random.Random(seed)
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            if random_pivot:
                k = rng.randint(lo, hi)
                a[k], a[hi] = a[hi], a[k]
            p = partition(a, lo, hi)
            left, right = (lo, p - 1), (p + 1, hi)
            left_size, right_size = p - lo, hi - p
            if left_size < right_size:
                if right[0] < right[1]:
                    stack.append(right)
                lo, hi = left
            else:
                if left[0] < left[1]:
                    stack.append(left)
                lo, hi = right
    return a


def quick_sort_threeway(values, *, seed=14):
    a = list(values)
    rng = random.Random(seed)
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            pivot = a[rng.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1
            left, right = (lo, lt - 1), (gt + 1, hi)
            left_size, right_size = lt - lo, hi - gt
            if left_size < right_size:
                if right[0] < right[1]:
                    stack.append(right)
                lo, hi = left
            else:
                if left[0] < left[1]:
                    stack.append(left)
                lo, hi = right
    return a
