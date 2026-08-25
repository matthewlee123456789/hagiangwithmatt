# Chef Minh Nguyễn — Website (bản demo)

HTML + CSS + JavaScript thuần. Không framework, không bước build khi chạy.

```
chef-minh/
├── index.html          Trang chủ (hero video, ẩm thực, 4 trụ, academy, truyền thông, blog, form)
├── the-chef.html       Hành trình + triết lý
├── cuisine.html        5 món, bấm vào mở cửa sổ câu chuyện
├── services.html       Tư vấn · Trải nghiệm · Thương hiệu
├── academy.html        2 khóa học
├── press.html          Truyền thông & thành tích
├── blog.html           Danh sách bài viết
├── blog/
│   ├── sous-vide.html
│   ├── dry-aging.html
│   └── nuoc-dung.html
├── css/style.css
├── js/main.js
├── assets/             ảnh + video hero
└── build.py            script dựng lại các trang (không cần khi chạy web)
```

**Xem demo:** giải nén, mở `index.html` bằng trình duyệt. Cần mạng để tải font Google.

---

## 1. FORM ĐĂNG KÝ — THÔNG TIN KHÁCH ĐI ĐÂU

### Hiện tại (chưa cấu hình)

Nút "Gửi thông tin" **mở ứng dụng email trên máy khách** với nội dung điền sẵn. Khách phải bấm Send lần nữa. Máy không có ứng dụng mail thì **không có gì xảy ra**. Đây chỉ là chế độ tạm để demo chạy được.

### Bật chế độ thật (5 phút, miễn phí, không giới hạn)

1. Vào https://web3forms.com
2. Nhập `thaiminhchef@gmail.com`, bấm **Create Access Key**
3. Mở email lấy Access Key
4. Mở `js/main.js`, tìm dòng đầu file:
   ```js
   var FORM_ACCESS_KEY = '';          // ← dán Access Key vào đây
   ```
5. Dán key vào giữa hai dấu nháy. Lưu. Xong.

Từ lúc đó, mọi thông tin khách điền sẽ **gửi thẳng về hộp thư `thaiminhchef@gmail.com`**, kèm dòng tiêu đề phân loại sẵn (Đăng ký học / Hợp tác thương hiệu / Tư vấn nhà hàng / Đặt trải nghiệm). Khách thấy dòng xác nhận ngay trên trang, không phải rời đi đâu cả.

### Nếu sau này muốn lưu lead vào bảng

Web3Forms chỉ gửi email, không lưu trữ. Khi lượng inquiry lớn, chuyển sang **Google Apps Script** để ghi vào Google Sheet đồng thời gửi mail. Lúc đó chỉ cần đổi `FORM_ENDPOINT` sang URL của Apps Script.

---

## 2. VIDEO Ở HERO — BA ĐIỀU CẦN BIẾT

**Video không tự phát tiếng được.** Chrome, Safari, Firefox đều chặn video tự chạy có âm thanh — đây là quy định của trình duyệt, không phải lỗi code. Cách duy nhất hoạt động: video khởi động ở chế độ tắt tiếng, kèm nút **"Đang tắt tiếng"** ở góc dưới phải để khách tự bật. Nút đã có sẵn.

**Logo trong video bị trùng với logo trang.** Video kết thúc bằng chính con dấu Chef Minh, đặt giữa khung, kèm dòng chữ "TEAM VIETNAM". Nếu để nguyên và chồng thêm con dấu SVG lên, sẽ có hai logo cùng lúc, cộng thêm hai dòng chữ cạnh tranh nhau. Cách xử lý:

- **Bỏ con dấu SVG khỏi hero** (vẫn giữ ở header và footer).
- Phủ tối video ~80% và làm mờ nhẹ 2px, để video còn lại phần lửa và ánh vàng làm không khí, không còn đọc được như một logo.

Muốn tăng/giảm độ tối, sửa `.hero__video::after` trong `css/style.css`.

**Chuyển động ở hero** đã được điều chỉnh so với yêu cầu ban đầu, có lý do:

| Yêu cầu | Đã làm | Vì sao |
|---|---|---|
| Chữ tên nhấp nháy | Chữ trượt lên + dải ánh vàng quét qua mỗi 5,5 giây | Chữ nhấp nháy vi phạm chuẩn tiếp cận WCAG 2.3.1 và làm chữ khó đọc. Ánh vàng quét qua vẫn tạo điểm nhấn mà không gây khó chịu |
| Nội dung tự chạy từng chữ, chạy hết thì dừng | Đúng như vậy | |
| Hai nút nhấp nháy | Viền vàng lan ra rồi tan, lệch nhịp nhau | Cùng lý do trên |

Ai bật chế độ giảm chuyển động trong hệ điều hành sẽ thấy trang tĩnh hoàn toàn.

---

## 3. NHỮNG CHỖ CẦN BỔ SUNG

Nội dung tạm nằm trong ngoặc vuông `[...]`.

| Chỗ | Cần gì |
|---|---|
| `the-chef.html` | Tiểu sử và các mốc thời gian — hiện trống hoàn toàn |
| `press.html` | **Link bài báo thật.** Nút "Đọc bài viết" đang khoá vì chưa có URL |
| `index.html` mục 15 năm | Số học viên đã đào tạo (số thật) |
| Footer | Link Facebook / Instagram / YouTube / TikTok |
| `blog/*.html` | Chef đọc, sửa và duyệt 3 bài viết trước khi đăng |

---

## 4. VIỆC CẦN XÁC NHẬN — QUAN TRỌNG

1. **Tên trên giấy chứng nhận.** Bằng Best Master Chef Awards 2024 ghi **NGUYEN THAI MINH**, và email là `thaiminhchef@`. Nhưng bản brief ban đầu ghi tên thật là **Nguyễn Văn Minh**. Cần xác nhận tên nào đúng để dùng thống nhất trên toàn trang và trong hồ sơ năng lực.

2. **Ảnh gà đen H'Mông** hiện là ảnh gà sống lấy từ một trang web khác, **có watermark của họ ở góc** (mình đã cắt bỏ phần watermark). Đây là ảnh của bên thứ ba, không phải ảnh món của Chef. Dùng lâu dài là rủi ro bản quyền. Nên thay bằng ảnh món thật hoặc ảnh Chef tự chụp.

3. **Ảnh nọng heo** đã cắt logo Top Chef Vietnam. Cắt logo chỉ là xử lý bố cục — quyền sử dụng hình ảnh từ chương trình truyền hình vẫn phải hỏi nhà sản xuất.

4. **Ảnh gỏi tái tôm sú** trông giống thịt heo áp chảo hơn là tôm sú tái. Nhờ Chef xem lại.

5. **Ảnh khóa học.** Ảnh khóa nâng cao đang dùng ảnh lễ trao giải DigiCook — không phải ảnh lớp học. Nên thay bằng ảnh Chef đang dạy.

6. **Nội dung hợp tác với One River** đang để `[CẦN XÁC NHẬN]`.

7. **3 bài blog** do bên thiết kế soạn từ kiến thức bếp phổ thông, đang có banner cảnh báo màu đỏ ở đầu mỗi bài. Chef phải đọc và duyệt, rồi xoá dòng `<p class="draft-note">…</p>` trong mỗi file.

---

## 5. SONG NGỮ

Trang chủ, điều hướng, footer, form và 5 câu chuyện món có đầy đủ VI/EN. Các trang con (hành trình, dịch vụ, truyền thông, blog) hiện **chỉ có tiếng Việt** — bấm EN vẫn đổi được menu và footer nhưng nội dung giữ nguyên. Sẽ bổ sung khi nội dung tiếng Việt chốt xong, vì dịch trước rồi sửa sau là làm hai lần.

---

## 6. ĐƯA LÊN GITHUB PAGES (khi sẵn sàng)

1. Tạo repository **Public**.
2. Upload **toàn bộ** thư mục, giữ nguyên cấu trúc. Thiếu `assets/`, `css/` hay `js/` là trang vỡ.
3. Settings → Pages → Deploy from a branch → `main` → `/ (root)`.
4. Gắn `chefminhnguyen.com` ở mục Custom domain, rồi trỏ DNS:
   - `A` → `185.199.108.153` · `185.199.109.153` · `185.199.110.153` · `185.199.111.153`
   - `CNAME` `www` → `<tài-khoản>.github.io`
5. Tick **Enforce HTTPS** sau khi DNS nhận.

> Video hero nặng 3,6 MB. GitHub Pages tải được nhưng lần đầu vào bằng 4G sẽ hơi chậm. Nếu cần, mình nén xuống ~1,5 MB mà gần như không giảm chất lượng.

---

## 7. KỸ THUẬT

- Font: **EB Garamond** (tiêu đề) + **Be Vietnam Pro** (thân chữ) — đều hỗ trợ đầy đủ dấu tiếng Việt.
- Con dấu là **SVG vẽ lại tạm** trong khối `<svg>` đầu mỗi trang (`#seal-mini`, `#stalk`). Thay bằng vector thật khi có, giữ `viewBox="0 0 200 200"` và `currentColor`.
- Chạy `python3 build.py` để dựng lại toàn bộ trang sau khi sửa khối dùng chung (header, footer, danh sách món, khóa học, truyền thông).
- Tôn trọng `prefers-reduced-motion`. Đóng cửa sổ món bằng phím `Esc`.

### Bảng màu

| Biến | Mã | Vai trò |
|---|---|---|
| `--lacquer` | `#120E0C` | Nền then |
| `--gold` | `#C6A664` | Vàng lá — màu thương hiệu |
| `--shell` | `#E8E1D3` | Vỏ trứng — nền sáng |
| `--cinnabar` | `#8C2318` | Đỏ son — chỉ làm điểm nhấn |

---

## 8. HỆ CHUYỂN ĐỘNG

Toàn bộ hiệu ứng nằm ở `css/motion.css` và `js/motion.js`. Chúng **tự tìm các thành phần có sẵn rồi gắn hiệu ứng** — không cần thêm class vào HTML. Sửa hoặc xoá hai file này là trang trở về trạng thái tĩnh, không hỏng gì.

| Hiệu ứng | Ở đâu | Ghi chú |
|---|---|---|
| Vạch tiến độ cuộn | Mép trên mọi trang | Chuyển từ đỏ son sang vàng |
| Màn chuyển trang | Khi bấm sang trang khác | Con dấu xoay trong lúc chờ |
| Chữ lộ dần bằng mặt nạ | Mọi tiêu đề lớn | Không phải fade, mà cắt dần từ dưới lên |
| Ảnh lộ dần + trôi | Ảnh món, khoá học, truyền thông | Ảnh trôi ngược chiều cuộn trong khung |
| Nghiêng 3D theo con trỏ | Thẻ món, 4 trụ, khoá học, truyền thông | Tối đa 5,5° kèm vệt sáng vàng bám con trỏ |
| Nút hút theo con trỏ | Nút chính ở hero và form | Dịch tối đa 5px |
| Bông lúa tự vẽ | Dấu phân cách phần triết lý | Nét vẽ dần theo chiều dài thật của path |
| Con dấu chìm xoay | Nền phần triết lý | Xoay chậm theo vị trí cuộn |
| Số 15 nhô lên | Phần 15 năm | Trôi ngược chiều cuộn |
| Hero rời đi | Khi cuộn khỏi hero | Chữ trôi lên và mờ dần |

**Vì sao không dùng three.js / WebGL:** nội dung chính của trang là ảnh món và câu chuyện; 3D thật sẽ cạnh tranh chứ không hỗ trợ. Thư viện WebGL nặng 500KB–1MB, cộng video nữa thì khách dùng 4G bỏ đi trước khi trang tải xong, và GPU chạy liên tục làm nóng máy. Các hiệu ứng ở trên tạo cảm giác chiều sâu tương đương nhưng chỉ tốn ~18KB và dùng thuần `transform` với `opacity` — hai thuộc tính duy nhất trình duyệt xử lý bằng GPU mà không phải tính lại bố cục.

**Hiệu năng:** mọi tính toán theo cuộn gom vào **một vòng lặp `requestAnimationFrame` duy nhất**. Hiệu ứng nghiêng chỉ bật trên máy có chuột thật; điện thoại và máy tính bảng không chạy phần này. Ai bật chế độ giảm chuyển động trong hệ điều hành sẽ thấy trang tĩnh hoàn toàn.

**Video hero đã nén** từ 3,6 MB xuống 915 KB (960px, CRF 30, faststart). Vì video bị phủ tối 80% và làm mờ 2px nên mắt thường không thấy khác biệt.

---

## 9. TỆP DÀNH CHO GITHUB PAGES

| Tệp | Việc |
|---|---|
| `CNAME` | Đã ghi sẵn `chefminhnguyen.com`. Đổi nếu dùng tên miền khác |
| `.nojekyll` | Tắt xử lý Jekyll của GitHub, tránh lỗi bỏ qua file |
| `404.html` | Trang báo lỗi có thiết kế, GitHub Pages tự dùng |
| `sitemap.xml` | Danh sách 10 trang cho Google |
| `robots.txt` | Trỏ tới sitemap |
| `lien-he.php` | Chỉ dùng khi chạy XAMPP. Để lại trên GitHub cũng không sao |

---

## 10. BẢN QUYỀN ẢNH — CẦN KIỂM TRA TRƯỚC KHI CÔNG BỐ

| Ảnh | Vấn đề |
|---|---|
| `mon-04-nong-heo.jpg` | Chụp trong chương trình Top Chef Vietnam, đã cắt logo. Cắt logo **không** thay thế được việc xin phép nhà sản xuất |
| `chef-portrait.jpg` · `chef-wide.jpg` | Cùng vấn đề. Áo bếp và tạp dề vẫn còn logo Top Chef |
| `press-topchef.jpg` · `press-sieubep-*.jpg` · `press-digicook.jpg` | Ảnh từ các chương trình truyền hình |
| `blog-dry-age.jpg` · `blog-sous-vide.jpg` | **Trông giống ảnh tư liệu lấy từ internet**, không phải ảnh Chef tự chụp. Ảnh sous-vide còn có thiết bị mang nhãn hiệu Anova, nhiều khả năng là ảnh quảng cáo của hãng |
| `blog-nuoc-dung.jpg` | Ảnh nồi nước dùng, có vẻ là ảnh Chef tự chụp — an toàn |

Ảnh của bên thứ ba dùng trên trang thương mại có thể bị yêu cầu gỡ hoặc đòi bồi thường. Nên thay bằng ảnh Chef tự chụp, hoặc mua bản quyền, hoặc dùng ảnh miễn phí từ Unsplash / Pexels.

---

Thiết kế: **mattdesignwebsite**
