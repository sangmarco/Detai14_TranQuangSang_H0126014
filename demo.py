"""Demo ngắn: Merge-Sort, chọn pivot, Quick-Sort và ví dụ cận dưới."""
import argparse
from math import factorial, log2, ceil
from algorithms import merge_sort, partition, quick_sort, quick_sort_threeway

DAY = [1, 3, 4, 7, 8, 5, 6, 2]


def show_merge():
    print('MERGE-SORT: chia đôi, sắp xếp từng nửa, rồi trộn')
    print('Ban dau: ', DAY)
    print('Hai nua: ', DAY[:4], '|', DAY[4:])
    print('Da sap:  ', merge_sort(DAY[:4]), '|', merge_sort(DAY[4:]))
    print('Ket qua: ', merge_sort(DAY))


def show_pivot():
    a = DAY.copy()
    chosen = a.index(5)
    print('PIVOT NGAU NHIEN (MINH HOA): gia su da chon vi tri', chosen)
    print('Ban dau: ', a)
    a[chosen], a[-1] = a[-1], a[chosen]
    print('Doi pivot ve cuoi:', a)
    p = partition(a, 0, len(a) - 1)
    print('Phan hoach:', a[:p], '|', a[p], '|', a[p + 1:])
    print('Hai nhom chua nhat thiet duoc sap xep!')
    print('Quick pivot cuoi: ', quick_sort(DAY))
    print('Quick pivot random (seed=14):', quick_sort(DAY, random_pivot=True, seed=14))


def show_threeway():
    a = [1, 3, 5, 4, 7, 8, 5, 6, 2, 5]
    print('QUICK 3 PHIA: ', a)
    print('Vi du chon pivot = 5')
    print('Ba vung: [1,3,4,2] | [5,5,5] | [7,8,6]')
    print('Ket qua:', quick_sort_threeway(a))


def show_lower():
    print('CAY QUYET DINH VA CAN DUOI')
    for n in (3, 4, 5, 6):
        permutations = factorial(n)
        minimum = ceil(log2(permutations))
        print(f'n={n}: n!={permutations}; 2^{minimum-1} < {permutations} <= 2^{minimum}; it nhat {minimum} so sanh (xau nhat)')
    print('Voi n=4: 4!=24; 2^4=16 (khong du); 2^5=32 (co the du).')
    print('Day la gioi han duoi, KHONG phai moi dau vao deu can 5 lan.')


def main():
    parser = argparse.ArgumentParser(description='Minh hoa De tai 14')
    parser.add_argument('--part', choices=['all', 'merge', 'pivot', 'threeway', 'lower'], default='all')
    part = parser.parse_args().part
    tasks = [('merge', show_merge), ('pivot', show_pivot), ('threeway', show_threeway), ('lower', show_lower)]
    for name, action in tasks:
        if part == 'all' or part == name:
            print('\n' + '=' * 58)
            action()
    expected = sorted(DAY)
    assert merge_sort(DAY) == quick_sort(DAY) == quick_sort(DAY, random_pivot=True) == quick_sort_threeway(DAY) == expected
    print('\nKiem tra: ket qua trung voi sorted() cua Python.')


if __name__ == '__main__':
    main()
