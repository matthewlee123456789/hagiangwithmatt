<?php
/* ============================================================
   NHẬN THÔNG TIN TỪ FORM — DÙNG KHI CHẠY THỬ TRÊN XAMPP
   ------------------------------------------------------------
   File này chỉ hoạt động khi có PHP (XAMPP, hosting thường).
   GitHub Pages KHÔNG chạy PHP — ở đó trang sẽ tự chuyển sang
   phương án khác, không lỗi.

   Thông tin khách điền sẽ được ghi vào: lien-he.csv
   Mở file đó bằng Excel để xem.
   ============================================================ */

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Chỉ nhận POST']);
    exit;
}

$raw  = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) { $data = $_POST; }

if (empty($data)) {
    echo json_encode(['success' => false, 'message' => 'Không có dữ liệu']);
    exit;
}

/* Làm sạch: bỏ thẻ HTML, cắt độ dài, gộp xuống dòng */
$clean = [];
foreach ($data as $k => $v) {
    if (!is_scalar($v)) continue;
    $k = mb_substr(strip_tags((string)$k), 0, 120);
    $v = mb_substr(strip_tags((string)$v), 0, 2000);
    $v = str_replace(["\r\n", "\r", "\n"], ' | ', $v);
    $clean[$k] = $v;
}

$file   = __DIR__ . '/lien-he.csv';
$isNew  = !file_exists($file);

$row = [
    date('Y-m-d H:i:s'),
    $clean['subject'] ?? '',
    $clean['need'] ?? '',
    $clean['Họ và tên'] ?? ($clean['name'] ?? ''),
    $clean['Email'] ?? ($clean['email'] ?? ''),
    $clean['Số điện thoại'] ?? ($clean['phone'] ?? ''),
    $clean['Zalo (nếu có)'] ?? ($clean['zalo'] ?? ''),
];

/* Các trường còn lại gộp vào một cột ghi chú */
$known = ['subject','need','from_name','access_key','Họ và tên','name','Email','email',
          'Số điện thoại','phone','Zalo (nếu có)','zalo'];
$extra = [];
foreach ($clean as $k => $v) {
    if (!in_array($k, $known, true) && $v !== '') $extra[] = "$k: $v";
}
$row[] = implode(' — ', $extra);

$fh = fopen($file, 'a');
if ($fh === false) {
    echo json_encode(['success' => false, 'message' => 'Không ghi được file']);
    exit;
}
flock($fh, LOCK_EX);
if ($isNew) {
    fwrite($fh, "\xEF\xBB\xBF"); // BOM để Excel đọc đúng tiếng Việt
    fputcsv($fh, ['Thời gian','Chủ đề','Nhu cầu','Họ tên','Email','Điện thoại','Zalo','Chi tiết']);
}
fputcsv($fh, $row);
flock($fh, LOCK_UN);
fclose($fh);

echo json_encode(['success' => true, 'message' => 'Đã lưu vào lien-he.csv']);
