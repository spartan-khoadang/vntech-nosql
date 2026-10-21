# NoSQL — Phần 1 · Nền tảng

Slide thuyết trình (HTML) về NoSQL: NoSQL là gì, vì sao cần NoSQL khi đã có SQL, và bốn loại NoSQL phổ biến. Phần 2 (use cases) sẽ được thêm sau.

## Chạy local

Slide được tải từ `sections/*.html` bằng `fetch`, nên cần HTTP (không mở trực tiếp file):

```bash
python3 -m http.server 8000
# mở http://localhost:8000
```

## Phím tắt

| Phím | Tác dụng |
|---|---|
| → / Space / Enter | Bước / slide tiếp theo |
| ← / Backspace | Lùi lại |
| N | Hiện / ẩn script (speaker notes) |
| O | Xem tổng quan tất cả slide |
| T | Đổi theme sáng / tối |
| F | Toàn màn hình |

Link trực tiếp tới một slide: `#<slide>.<bước>`, ví dụ `#9.0`.

## Cấu trúc

- `index.html` — loader, thứ tự các section
- `sections/` — nội dung slide; script nói nằm trong `<aside class="notes">` của từng slide
- `diagrams/` — diagram tương tác tạo bằng archify, nhúng qua iframe
- `SCRIPT-phan-1.md` — script đầy đủ, sinh bằng `python3 tools/build_script.py`
