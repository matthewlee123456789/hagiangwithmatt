# QUẢNG CÁO & BỐ CỤC 3 CỘT

## 1. BỐ CỤC

Từ **1280px trở lên**, trang chia ba cột dọc:

```
│  20%  │        57%        │  20%  │
│ TOUR  │   NỘI DUNG WEB    │ SẢN   │
│  160  │                   │ PHẨM  │
│ ×600  │                   │ 160×600│
```

Dưới 1280px, hai dải tự ẩn và nội dung trở về 1 cột như cũ. Đây là chủ ý — laptop 13 inch không đủ chỗ cho ba cột.

**Vùng chạy:** bắt đầu từ phần **Hành trình**, cuộn theo màn hình, dừng lại khi hết phần **Blog**. Không tràn xuống Liên hệ và Footer.

Nền các section vẫn tràn hết chiều ngang màn hình. Chỉ phần chữ co lại 57%. Nếu để cả nền co theo, trang sẽ trông như một hộp trắng giữa hai vùng trống.

---

## 2. SỬA NỘI DUNG QUẢNG CÁO

Mở `js/ads.js`, phần đầu file:

```js
var ADS = [
  {
    side:'left',
    img:'assets/ad-ha-giang-01.jpg',
    kicker:'Đi cùng Chef',
    title:'Tour Hà Giang',
    line:'Tới tận nơi có nọng heo đen cao nguyên đá Đồng Văn và gà đen H'Mông Tây Bắc.',
    list:['Cao nguyên đá Đồng Văn','Chợ phiên vùng cao','Ăn tại bếp nhà sàn'],
    cta:'Xem hành trình',
    url:'https://hagiangwithmatt.com'      // ← THAY LINK THẬT
  },
  ...
```

**Bắt buộc thay hai ô `url`.** Ô bên trái đang đoán từ tab trình duyệt của bạn, ô bên phải đang trỏ tạm về form liên hệ.

### Giới hạn chữ

| Ô | Tối đa |
|---|---|
| `kicker` | 20 ký tự |
| `title` | 22 ký tự |
| `line` | 90 ký tự |
| mỗi dòng `list` | 30 ký tự |
| `cta` | 16 ký tự |

Thẻ cao cố định 600px. Viết dài hơn sẽ bị cắt mất phần dưới.

---

## 3. ẢNH BANNER

| Thông số | Giá trị |
|---|---|
| Kích thước | **320 × 380px** |
| Định dạng | JPG |
| Dung lượng | Dưới 60KB |
| Tên file | `ad-ha-giang-01.jpg` · `ad-san-pham-01.jpg` |

Vùng ảnh trong thẻ chỉ cao 190px và rộng 160px. Chép ảnh thật đè lên hai file có sẵn, giữ nguyên tên.

**Chọn ảnh:** một chủ thể duy nhất, chiếm ít nhất nửa khung, tông tối trầm. Ảnh toàn cảnh nhiều chi tiết sẽ thành mớ nhiễu ở kích thước này.

- **Banner trái (tour):** một khúc cua đèo, mái nhà trình tường, hoặc bếp lửa nhà sàn
- **Banner phải (sản phẩm):** cận cảnh lạp sườn treo gác bếp, hũ mật ong bạc hà — ảnh sản phẩm cận cảnh luôn hiệu quả hơn ảnh phong cảnh

---

## 4. CƠ CHẾ

**Tự đổi tông theo nền.** Qua các section nền vỏ trứng sáng, thẻ chuyển sang nền sáng chữ đậm.

**Có nút đóng.** Bấm ✕ thì cả hai dải biến mất, nội dung giãn về full width, và nhớ suốt phiên duyệt.

**Nhãn "Tài trợ"** hiện phía trên. Nên giữ.

**Liên kết có `rel="sponsored"`** đúng chuẩn Google. Thiếu nó, Google có thể coi là liên kết mua bán và phạt thứ hạng cả hai trang.

**Tắt hoàn toàn:** đổi thành `var ADS = [];` hoặc xoá dòng `<script src="js/ads.js">` trong các file HTML. Muốn tắt riêng trang nào thì xoá dòng đó ở trang ấy — nên cân nhắc bỏ ở `services.html` và `press.html`, hai trang mà khách B2B đọc kỹ nhất.

---

## 5. XEM THỬ

Chép vào `C:\xampp\htdocs\`, bật Apache, vào `http://localhost/chefminh/`.

**Phóng to cửa sổ hết cỡ.** Màn hình nhỏ hơn 1280px sẽ không thấy quảng cáo — nhấn **Ctrl + dấu trừ** về 80% hoặc 67% là hiện ra.
