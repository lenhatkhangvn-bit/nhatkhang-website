# Website Nhật Khang

CÔNG TY TNHH KIẾN TRÚC XÂY DỰNG NHẬT KHANG – Hoàn thiện & Nội thất căn hộ Đà Nẵng.
Web tĩnh (HTML/CSS/JS) chạy trên GitHub Pages.

## Cấu trúc
- `index.html` – trang chủ (thẻ dự án tự sinh giữa `<!-- CARDS:START -->` … `<!-- CARDS:END -->`)
- `_src/du-an/<slug>.json` – **nội dung bài dự án** (sửa ở đây, không sửa HTML trong `du-an/`)
- `_tools/build.py` – sinh `du-an/*.html`, thẻ dự án trang chủ, `sitemap.xml`, `robots.txt`
- `assets/` – CSS, JS, hình ảnh (ảnh ≤ 1600 px, JPG chất lượng ~80)

## Đăng bài mới
1. Thêm ảnh vào `assets/img/` (tên không dấu, vd `s2-79m2-1.jpg`)
2. Tạo `_src/du-an/<slug>.json` theo mẫu bài có sẵn (thêm `"draft": true` nếu chưa muốn đăng)
3. `python3 _tools/build.py`
4. Commit & push → web tự cập nhật sau ~4 phút

Khi gắn tên miền riêng: sửa `SITE_URL` trong `_tools/build.py`, chạy lại build.
Không đưa giá vốn, hệ số, lợi nhuận, tên chủ nhà hay mã căn lên web.
