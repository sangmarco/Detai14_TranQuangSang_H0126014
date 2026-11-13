# Đề tài 14 – Merge-Sort, Quick-Sort và cận dưới của bài toán sắp xếp
Học viên: Trần Quang Sang - H0126014 - 
Giảng viên: TS. Phạm Minh Chuẩn

Dự án Python minh họa hai thuật toán sắp xếp theo phương pháp **chia để trị**, cách chọn **pivot** trong Quick-Sort, và **cận dưới của sắp xếp dựa trên phép so sánh**.

Đây là mã nguồn phục vụ bài tập cá nhân môn *Cấu trúc dữ liệu và Giải thuật nâng cao*. Mục tiêu là **dễ đọc, dễ chạy, đúng thuật toán và có thể kiểm chứng bằng thực nghiệm**.

## 1. Nội dung chính

| Nội dung | Hàm / lệnh | Ý tưởng |
|---|---|---|
| Merge-Sort | `merge_sort()` | Chia đôi dãy, sắp xếp từng nửa rồi trộn |
| Quick-Sort (pivot cuối) | `quick_sort()` | Lấy phần tử cuối làm chốt, phân hoạch hai phía |
| Quick-Sort (pivot ngẫu nhiên) | `quick_sort(..., random_pivot=True)` | Chọn một vị trí pivot ngẫu nhiên tại mỗi lần phân hoạch |
| Quick-Sort ba phía | `quick_sort_threeway()` | Chia thành các vùng nhỏ hơn, bằng và lớn hơn pivot |
| Cận dưới | `python demo.py --part lower` | Minh họa giới hạn so sánh bằng cây quyết định |
| Benchmark | `benchmark.py` | Đo thời gian và so sánh với `sorted()` của Python |

Các hàm sắp xếp **trả về danh sách mới**, không thay đổi danh sách đầu vào. Quick-Sort sử dụng `stack` thay cho đệ quy trực tiếp để tránh lỗi giới hạn đệ quy ở những đầu vào chia lệch.

## 2. Yêu cầu

- **Python 3.9 trở lên**.
- **Không cần cài thêm thư viện**: chỉ sử dụng thư viện chuẩn Python.
- Có thể chạy trong Visual Studio Code hoặc Terminal/PowerShell.

Kiểm tra phiên bản:

```bash
python --version
```

Trên Windows, nếu lệnh `python` không hoạt động, thử `py -3 --version` và thay `python` bằng `py -3` trong các ví dụ bên dưới.

## 3. Chạy demo

Mở Terminal trong thư mục dự án (nơi chứa `demo.py`), sau đó chạy:

```bash
python demo.py
```

Hoặc:

```bash
python demo.py --part merge       # Chia và trộn trong Merge-Sort
python demo.py --part pivot       # Chọn pivot, đổi về cuối và phân hoạch
python demo.py --part threeway    # Minh họa ba vùng khi có số trùng
python demo.py --part lower       # Cây quyết định và cận dưới
```

**Ví dụ chung:** `A = [1, 3, 4, 7, 8, 5, 6, 2]`.

Trong phần pivot, ví dụ **giả sử** lần chọn ngẫu nhiên lấy số `5` để dễ giải thích trên bảng. Đây là lựa chọn minh họa cố định; chức năng chọn ngẫu nhiên **thực sự** nằm trong `quick_sort(..., random_pivot=True)`.

Sau phân hoạch, minh họa cho ra:

```text
[1, 3, 4, 2] | 5 | [7, 6, 8]
```

Hai vùng hai bên **chưa nhất thiết được sắp xếp hoàn chỉnh**; Quick-Sort tiếp tục xử lý các vùng đó.

## 4. Kiểm thử tính đúng đắn

```bash
python -m unittest -v test_algorithms
```

Bộ kiểm thử so sánh kết quả với `sorted()` trên nhiều loại đầu vào, kiểm tra phân hoạch Lomuto, tính ổn định của Merge-Sort và khả năng xử lý dãy tăng dài của Quick-Sort.

Kết quả đúng sẽ có dòng cuối là `OK`.

## 5. Đo thời gian chạy (benchmark)

Chạy thử nhanh:

```bash
python benchmark.py --sizes 100 300 --repeats 2 --output outputs/benchmark_thu.csv
```

Chạy theo cấu hình của dữ liệu mẫu trong kho lưu trữ:

```bash
python benchmark.py --sizes 300 800 1500 --repeats 5 --output outputs/benchmark_moi.csv
```

Chương trình chạy trên **5 dạng đầu vào**: ngẫu nhiên, tăng dần, giảm dần, gần có thứ tự và nhiều giá trị trùng; đo **5 phương pháp** (4 thuật toán tự cài và `sorted()`), dùng `time.perf_counter_ns()` và lấy **trung vị** các lượt đo, đơn vị mili giây (ms).

Kết quả chạy mới được lưu trong `outputs/` và **không ghi đè** dữ liệu mẫu trong `results/`. Các file trong `outputs/` mặc định không được đưa lên GitHub bởi `.gitignore`.

### Kết quả mẫu đã có

Bảng dưới lấy từ [`results/ket_qua_benchmark.csv`](results/ket_qua_benchmark.csv), với **n = 1.500**, **5 lượt đo** trên Python 3.13.5 / Linux. Đây là số liệu của một môi trường cụ thể, không phải tốc độ cố định của thuật toán.

| Thuật toán | Dãy tăng dần (ms) | Nhiều số trùng (ms) |
|---|---:|---:|
| Merge-Sort | 2,190 | 1,846 |
| Quick-Sort pivot cuối | 81,605 | 15,932 |
| Quick-Sort pivot ngẫu nhiên | 1,735 | 16,524 |
| Quick-Sort ba phía | 2,525 | 0,473 |
| Python `sorted()` | 0,006 | 0,069 |

**Nhận xét:** Pivot cuối rất bất lợi khi dãy đã tăng dần. Phân hoạch ba phía hữu ích khi có nhiều phần tử trùng. Tuy nhiên, thời gian đo thay đổi theo máy, phiên bản Python, tải hệ thống và kích thước dữ liệu. Kết quả đo không thay thế chứng minh độ phức tạp.

Thông tin môi trường của kết quả mẫu: [`results/moi_truong_thu_nghiem.txt`](results/moi_truong_thu_nghiem.txt).

## 6. Ý nghĩa độ phức tạp và cận dưới

| Thuật toán | Thời gian trường hợp xấu nhất | Ghi chú |
|---|---|---|
| Merge-Sort | `Θ(n log n)` | Ổn định; cần thêm bộ nhớ `O(n)` |
| Quick-Sort pivot cuối | `Θ(n²)` | Có thể chia rất lệch với dãy đã tăng/giảm |
| Quick-Sort pivot ngẫu nhiên | `Θ(n²)` | Kỳ vọng `Θ(n log n)` với các khóa phân biệt |
| Quick-Sort ba phía | Có thể `Θ(n²)` | Phù hợp khi nhiều khóa giống nhau; pivot chọn ngẫu nhiên |

**Cận dưới** không phải độ phức tạp của một thuật toán cụ thể. Với **mọi thuật toán sắp xếp chỉ dựa trên so sánh** và dữ liệu có khóa phân biệt, số phép so sánh trong **trường hợp xấu nhất** phải đạt ít nhất bậc `Ω(n log n)`.

Ví dụ với **4 phần tử phân biệt**: có `4! = 24` hoán vị. Mỗi phép so sánh có hai kết quả; 4 phép so sánh phân biệt tối đa `2⁴ = 16` khả năng, nên chưa đủ. Vì `2⁵ = 32 ≥ 24`, ta thu được giới hạn dưới **ít nhất 5 phép so sánh** trong trường hợp xấu nhất. Đây là lập luận theo **cây quyết định**. Không có nghĩa mọi đầu vào đều cần đúng 5 phép so sánh.

Trong code, `seed=14` được dùng để **tái lập** cùng chuỗi pivot ngẫu nhiên khi chạy lại. Thay đổi `seed` sẽ tạo một chuỗi lựa chọn khác; dùng seed cố định không làm mất ý nghĩa phân tích kỳ vọng khi xét các khả năng lựa chọn pivot.

## 7. Cấu trúc thư mục

```text
merge-quick-sort-de-tai-14/
├── README.md
├── .gitignore
├── algorithms.py                # Cài đặt 4 cách sắp xếp
├── demo.py                      # Minh họa phục vụ thuyết trình
├── benchmark.py                 # Đo thời gian và ghi CSV
├── test_algorithms.py           # Kiểm thử bằng unittest
└── results/
    ├── ket_qua_benchmark.csv    # Kết quả đo mẫu (75 dòng dữ liệu)
    └── moi_truong_thu_nghiem.txt
```

## 8. Tài liệu tham khảo

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. Wiley. Chương 12: Sorting and Selection.

