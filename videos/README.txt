Đặt file video hero vào thư mục này với đúng hai tên sau:

  hero.mp4    H.264 / AAC, tỉ lệ 16:9, khuyến nghị 1920x1080, dưới 8 MB
  hero.webm   VP9 / Opus, cùng nội dung  (không bắt buộc, nhưng nhẹ hơn ~30%)

Không cần sửa HTML. Trang tự nhận file khi có.

Lệnh nén gợi ý (cần ffmpeg):

  ffmpeg -i goc.mov -vf scale=1920:1080 -c:v libx264 -crf 26 -preset slow \
         -c:a aac -b:a 96k -movflags +faststart hero.mp4

  ffmpeg -i goc.mov -vf scale=1920:1080 -c:v libvpx-vp9 -crf 34 -b:v 0 \
         -c:a libopus -b:a 96k hero.webm

Nếu video có lời nói, hãy thêm file phụ đề hero.en.vtt vào cùng thư mục
và báo lại — tôi sẽ nối vào thẻ <track> cho người khiếm thính.

Trong lúc chưa có video, trang hiển thị ảnh poster tĩnh và tự ẩn nút bật tiếng.
