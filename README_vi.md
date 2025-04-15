# Bộ lọc Corpus Tiếng Việt

Đây là công cụ Python để lọc corpus tiếng Việt bằng cách loại bỏ các câu có chứa:
- Từ viết tắt (ví dụ: "NBA", "GTVT", "U.S.A")
- Từ tiếng Anh

## Tính năng

- Đọc file văn bản với mã hóa UTF-8 (cần thiết cho các ký tự tiếng Việt)
- Giữ nguyên cấu trúc tài liệu (đoạn văn)
- Thông minh phát hiện từ viết tắt và từ tiếng Anh
- Tạo file đầu ra đã lọc với các câu không mong muốn đã bị loại bỏ

## Cài đặt

Không cần thư viện bổ sung. Script này chỉ sử dụng các thư viện chuẩn của Python 3.

## Cách sử dụng

Cách sử dụng cơ bản:

```bash
python vietnamese_corpus_filter.py input_file.txt
```

Điều này sẽ tạo ra file `input_file_filtered.txt` chứa nội dung đã được lọc.

Để chỉ định tên file đầu ra khác, sử dụng tùy chọn `-o`:

```bash
python vietnamese_corpus_filter.py input_file.txt -o output_file.txt
```

Để hiển thị thông tin chi tiết về quá trình lọc, sử dụng tùy chọn `-v`:

```bash
python vietnamese_corpus_filter.py input_file.txt -v
```

## Giải thích thuật toán

Script này sử dụng hai hàm chính để xác định nội dung cần lọc:

1. `is_abbreviation()`: Phát hiện từ viết tắt dựa trên các quy tắc:
   - Từ viết hoa hoàn toàn với 2+ ký tự (ví dụ: NBA, FLC)
   - Từ có dấu chấm giữa các chữ cái (ví dụ: U.S.A)
   - Từ có chữ hoa không ở đầu (ví dụ: iPhone, MacBook)

2. `is_english_word()`: Phát hiện từ tiếng Anh dựa trên đặc điểm:
   - Chỉ chứa các ký tự ASCII (không có dấu tiếng Việt)
   - Không phải là từ ngắn thông dụng trong tiếng Việt

## Ví dụ

Input:
```
Xin chào, đây là một văn bản mẫu tiếng Việt để kiểm tra.
FLC và NBA là các từ viết tắt đáng lẽ sẽ bị lọc bỏ.
Đây là một câu hoàn toàn bằng tiếng Việt và không có từ viết tắt.
```

Output:
```
Xin chào, đây là một văn bản mẫu tiếng Việt để kiểm tra.
Đây là một câu hoàn toàn bằng tiếng Việt và không có từ viết tắt.
```