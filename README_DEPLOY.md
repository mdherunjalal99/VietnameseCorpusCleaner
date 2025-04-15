# Hướng dẫn Deploy Vietnamese Corpus Filter trên Render

Đây là các bước để triển khai ứng dụng lọc corpus tiếng Việt lên nền tảng Render.

## Bước 1: Chuẩn bị tài khoản Render

1. Truy cập [Render.com](https://render.com/) và đăng ký tài khoản
2. Đăng nhập vào tài khoản Render của bạn

## Bước 2: Kết nối với GitHub

1. Tải dự án lên GitHub repository của bạn
2. Trong bảng điều khiển Render, chọn "New" > "Web Service"
3. Kết nối với GitHub repository đã tạo

## Bước 3: Cấu hình Web Service

Khi thiết lập dịch vụ web mới, sử dụng các cài đặt sau:

- **Name**: vietnamese-corpus-filter (hoặc tên bạn muốn)
- **Environment**: Python
- **Region**: Chọn vùng gần vị trí của bạn nhất
- **Branch**: main (hoặc nhánh bạn muốn deploy)
- **Build Command**: `pip install -r render-requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`

Hoặc sử dụng file `render.yaml` có sẵn trong dự án.

## Bước 4: Biến môi trường

Thêm biến môi trường sau:
- `PYTHON_VERSION`: 3.11.0

## Bước 5: Triển khai

1. Nhấp vào "Create Web Service"
2. Render sẽ bắt đầu quá trình build và deploy ứng dụng của bạn
3. Sau khi triển khai hoàn tất, ứng dụng của bạn sẽ có sẵn tại URL được cung cấp (thường có dạng https://your-app-name.onrender.com)

## Cấu trúc dự án

Đảm bảo rằng repository của bạn có cấu trúc sau:

```
vietnamese-corpus-filter/
├── main.py
├── vietnamese_corpus_filter.py
├── render-requirements.txt
├── render.yaml
└── templates/
    └── index.html
```

## Xử lý sự cố

- Nếu gặp lỗi trong quá trình triển khai, kiểm tra logs trong bảng điều khiển Render
- Đảm bảo các thư viện đã được liệt kê đầy đủ trong file `render-requirements.txt`
- Xác nhận rằng port được cấu hình đúng trong file `main.py` để sử dụng biến môi trường `PORT`

## Giới hạn của Render Free Tier

Lưu ý rằng với gói miễn phí của Render:
- Dịch vụ sẽ spin down sau 15 phút không hoạt động
- Có giới hạn về số lượng giờ sử dụng miễn phí mỗi tháng
- Dịch vụ miễn phí không phù hợp để xử lý file corpus quá lớn

Để xử lý corpus lớn, bạn nên sử dụng phiên bản command line trên máy tính cá nhân.