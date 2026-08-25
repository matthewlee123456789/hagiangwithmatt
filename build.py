#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
"""Dựng toàn bộ trang HTML của chefminhnguyen.com từ các khối dùng chung."""
import os, re

NAV = [
    ('the-chef.html',  'nav.chef',    'Chef',         'chef'),
    ('cuisine.html',   'nav.cuisine', 'Ẩm thực',      'dish'),
    ('services.html',  'nav.services','Dịch vụ',      'service'),
    ('academy.html',   'nav.academy', 'Academy',      'book'),
    ('press.html',     'nav.press',   'Truyền thông', 'media'),
    ('blog.html',      'nav.blog',    'Blog',         'pen'),
]

SOCIAL = [
    ('fb',     'https://www.facebook.com/Minhnguyensg0110/', 'Facebook'),
    ('tiktok', '#',                                          'TikTok'),
    ('yt',     '#',                                          'YouTube'),
    ('zalo',   'https://zalo.me/0352118837',                 'Zalo'),
]

SEAL_DEFS = open('_seal.svg', encoding='utf-8').read()

# Từ điển sinh tự động cho nội dung các trang con
I18N = {}


def R(key, vi, en):
    """Ghi cặp Việt–Anh vào từ điển rồi trả về bản tiếng Việt."""
    I18N[key] = [vi, en]
    return vi


def head(title, desc, depth=0):
    up = '../' * depth
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#120E0C">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="vi_VN">
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAI8ElEQVR42k2XW48cVxHHf3X6dPfcd2Z3Z3dnfVl7bSe248hBApEL4vaEkBDihWde+QYREo+IJz4FEuITEMELT8SIBBMlSiC2Y3vtXa/3OjM79+k+p3g4PWtLI830dPepqn9V/etf8rvLW+oBvEdVEREAVBUPGBEEcN7jRRBVDIoieFUM4Iv3FueICCKCojjn8Mj5f947BEGL+0ZVQRUxBiOCqgLgURBBC2eMCKZ4Fg1GTXgUX7wnUBgGB8EhYzACBlD1sHBOFUEwAKKKeiVXDbEpRGIQFNSjAr7wGlHUCFFxiAIGBSOIeYVeuCcgBhBCXAUKhXEBrBYw50XkgoToi+jOv/HhM1e85kRWMHGEIrgsx+fB2SgxiBG8gngfUABECmS9IqqA4FWwGIPLc1jkXkC8nts1kcE7xc0cpVpM41qD8kqJyBqi2CAiZFmOy5Tx0YTu3oBxPyNODBKFmvEI3nuMmJCmgA1ewIb8Lx4EUc4RMEbIpjlx1XL57jqNzRrj7oTpKMNFEeMXI2ajOatXGsyHc+rrZdpvNJmcznny75dMJzlJOYY8x4g5r5NzaIsiBg+KoBIKRRAiGzGfOeqbFa798CIaGXY/P0IdrG03KddTpr0Zw8Mxk7M56zdWiBPL4YMeJo145xc3aV9pMh/OsEagqJdFXTgEp2C9BqOqQlHGGBGyccbKtSXW7yxz/KhPNnb0XozQXEHg5HEfVU9lpczgcEx9pczgZMr4dEZvf0TntuONH1wlLcfsfr5PXE0QBS3q4jzFqC88K9rICPOZo9opsXqzxf5Xp6zfWsar0rpYw3t48dUJlZWU9o0WrYtVyvWEJ5+8pLc/Iq4lGGtoXajyzT+fsfXeZdrXV8mmWci9hG4yIkSAdQUBWWNQQBzY1LD+dpvBixGr15aYjT0mjujtDam1y9z6yRVqyyWmwwzNc2zJcroz4OmnBwwPRyxdaGDimDe+d4mn9/e59sNthi/PmGceicw5CgDWABgpSEfJZ472Oy0mvSnHj045ehJRWa3Q3x0wH2Zce3+D1a0lVBQTCUYSiODC26uUaiX+9acv8blHjMHnOU6hu3fGlQ+u8NVfH5BWk4LspGBaYzCL3OQeW7OkSwnDowmSxpSXUoYHI/DB4Gw4Dy3rBfWgTlEH9fVq+C2COk93t4tHOH3apbdzwtLWEpVmiTx3RcoDaxpVxRX9r5mjspaSjTPqnTLVlRLzaU42nBOZ0L+j3hwMlJcS1q43aXSqVJdLpKWYwfEktFkE0/6UfJbRvNBgdXuZ0dGE9RttsmleMGbRhgtvPIEw0qWYaX9OuVWi1i4x78+JbOjhSIT52ZT2lSalesp8lIFCs1OltVlldDIBa3BeMXFE/+WQzp027a0mk96EeqceZkHBuCKCxXsWZGSsYKyS1mK6O2OyszmRVzLvAIO3hulZxuOP92hsVLBxqJtRb0a5XmLSnxWkJjgJM+bwwSlJHGOTiCixmNgUPajnQ45ixhAZIUos/Rdjjr/uovgwI4zBIxiBLPdsv9uhc7tNlFji2GIQTp8PmY0ybCSvDvaKmzu+ufeM4eGQKE1IYhvsG4OKYL0veLngAXVg04i0mZDPc7wqakI0LlfwcO+P/2N0OiGfOUC5+/NraA6j3hSbhEEUkIUoNvR3R8S1FBNFeB94R1TBKzbQr4TC9h7nlLSe0LqU0H82wsgcD3jnqayUMB6+/OgRSdVSa1dDup4NqLTKtC7V6O0NMbbgFBN0w9X3r5A2ymTTHJcHTlHVBeuaQMFG8K5oq9yR1lOaWw0URZ3HOc/6m8u8/bPr3PnpNs1OnfHJlP7LEePumPbVJS7d2cDNHAiFuoKNm6t0brcZHA8DollATTRQuvWFgIg09OKkO6fcihkeTRjsT6ivVujunWETy4svjph05zQ362y/e4F87rj4rVUG+2P+8vt7jE7GxLUYUXC5p7ZW5+RZn8hE1NYa9J/3cShxQf3qFYMPMikXQWIYvpxQbqYMXo4ZHk0wNiKpp3inzIYZjz7eZeezfa5/sMGPf30XG1kOHvaotyvYiiWfZrg8p9xIiUsxw4Mh+w9PKS9VOHp4QJxYvFdUDIjBijGoeoxXiAyzYcb4eEZ9rRzUkfE0Nuqc7vTwzvHer97iu7+8yWB/wkd/+ISH9/aoLpfZuN6ic2uVvf8ec/jwhPpmg8nphHyWcfHqCmf7fQYnQ5J6ymIQKCC/7XQ0pIGQO+eJrOH6jy5y8qjPxu0VQNj7/IT5cMbajSX6exMOHndxzmNLEd55fOZJ6wnNzTpiI7a/s4nmjuPnQ9o3Otz/86fMsxxjTKEXiyL0SEEMgvcKUUQ2U3b/c8T6rRV2Pzsim3lmgylxybL3xQnHOz2SiqVctaCetBRTqifUlku4zKHOEVvh6f192m+u8fDvD5iMppgoGHfqEQlayAZZHqaXIZCHSYTu7oCkFHPx7jonz8/IJjkiwvJWg0anyvGjHn4xwNKItRstDr7ucfpiQLNT58lnB1z7/jZP/rHD0eNjkkqKy10QIYWi9ih2kQzvNcBTtF1ciTl+3CObZlz+dodSNeZsb0B1uURlqUyjnbNzf59yK+HCW6tUllJWthqoFZYvNWhtLvP13x5x+OSUtJrgsjwYLhYZJWgC+c1GRxc963xBoYBTxQj4uSctJ2zcWaaxVmU+yhh3J1SbFU52uhBHVFslvFcqrRL15Qrd3SGPP91jNsmwJYv3/nxfMAvZv1BhH25sqLy2BpwvFoBBAps5JZ8HWb58aYnmeoXICnE5wXkNec89Z4cTDp90GZ1NSVILUZDjghTkxDntLwzKh+sb+vpOyOKmEYwPWmGxSqnz5JnHANZKMaQAr+SZC6M2DoraOVfsPsWuoZx7oAv7qmEvWKxji73Na7h2ryAJ3G0gLtugbjUMGxHACtZajISIvQv5jYpojQbYF8K7YAAQMFpEvMhLuNRQKIs60HC92PFy9TgNkb0KSXHOFz+Lrfm1xC6W3vMgJaBreA15Xss9IhgTFktjXj22WMWjQsg6LQa5vib2hXP4FwGJyKszCkVkRPg/OMcv1nHV0X0AAAAASUVORK5CYII=">
<link rel="apple-touch-icon" href="{up}assets/logo-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Be+Vietnam+Pro:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{up}assets/chef-portrait.jpg" fetchpriority="high">
<link rel="stylesheet" href="{up}css/site.css">
</head>
<body>
{SEAL_DEFS}
'''


def header(active='', depth=0):
    up = '../' * depth
    nav = '\n'.join(
        f'      <a href="{up}{h}" data-i="{ic}"{" class=\"is-active\"" if h == active else ""}><span data-i18n="{k}">{t}</span></a>'
        for h, k, t, ic in NAV)
    mnav = '\n'.join(
        f'    <a href="{up}{h}" data-i="{ic}"><span data-i18n="{k}">{t}</span></a>'
        for h, k, t, ic in NAV)
    return f'''<header class="hdr" id="hdr">
  <div class="wrap hdr__in">
    <a href="{up}index.html" class="brand" aria-label="Chef Minh Nguyễn — trang chủ">
      <img src="{up}assets/logo-32.png" alt="" width="32" height="32" decoding="async">
      <span class="brand__txt">CHEF MINH NGUYỄN</span>
    </a>
    <nav class="nav" aria-label="Điều hướng chính">
{nav}
    </nav>
    <div class="hdr__right">
      <div class="lang" role="group" aria-label="Ngôn ngữ">
        <button type="button" data-lang="vi" aria-pressed="true">VI</button>
        <span>/</span>
        <button type="button" data-lang="en" aria-pressed="false">EN</button>
      </div>
      <a href="{up}index.html#contact" class="btn" data-i="chat"><span data-i18n="nav.cta">Làm việc cùng Chef</span></a>
      <button class="burger" id="burger" aria-label="Mở menu" aria-expanded="false"><i></i><i></i><i></i></button>
    </div>
  </div>
</header>

<div class="mmenu" id="mmenu">
  <nav aria-label="Điều hướng di động">
{mnav}
    <a href="{up}index.html#contact" data-i="mail"><span data-i18n="nav.contact">Liên hệ</span></a>
  </nav>
  <a href="{up}index.html#contact" class="btn btn--solid" data-i="chat"><span data-i18n="nav.cta">Làm việc cùng Chef</span></a>
</div>
'''


def footer(depth=0):
    up = '../' * depth
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft__grid">
      <div class="ft__brand">
        <img src="{up}assets/logo-64.png" alt="Chef Minh Nguyễn" width="64" height="64" loading="lazy" decoding="async">
        <p data-i18n="ft.tag">Ẩm thực Việt, đọc lại bằng kỹ thuật hiện đại.</p>
        <div class="ft__social">
          <a href="https://www.facebook.com/Minhnguyensg0110/" target="_blank" rel="noopener" aria-label="Facebook" data-i="fb"></a>
          <a href="#" aria-label="TikTok" data-i="tiktok"></a>
          <a href="#" aria-label="YouTube" data-i="yt"></a>
          <a href="https://zalo.me/0352118837" target="_blank" rel="noopener" aria-label="Zalo" data-i="zalo"></a>
        </div>
      </div>
      <div>
        <h4 data-i18n="ft.h1">Chef</h4>
        <ul>
          <li><a href="{up}the-chef.html" data-i="clock"><span data-i18n="ft.l1">Hành trình</span></a></li>
          <li><a href="{up}the-chef.html#philosophy" data-i="star"><span data-i18n="ft.l2">Triết lý</span></a></li>
          <li><a href="{up}cuisine.html" data-i="dish"><span data-i18n="ft.l3">Ẩm thực</span></a></li>
        </ul>
      </div>
      <div>
        <h4 data-i18n="ft.h2">Dịch vụ</h4>
        <ul>
          <li><a href="{up}academy.html" data-i="book"><span data-i18n="ft.l4">Đào tạo</span></a></li>
          <li><a href="{up}services.html#brand" data-i="media"><span data-i18n="ft.l5">Thương hiệu</span></a></li>
          <li><a href="{up}services.html#consulting" data-i="service"><span data-i18n="ft.l6">Tư vấn</span></a></li>
          <li><a href="{up}services.html#experiences" data-i="users"><span data-i18n="ft.l7">Trải nghiệm</span></a></li>
          <li><a href="{up}blog.html" data-i18n="nav.blog">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4 data-i18n="ft.h3">Liên hệ</h4>
        <ul>
          <li><a href="mailto:thaiminhchef@gmail.com">thaiminhchef@gmail.com</a></li>
          <li><a href="tel:+84352118837">0352 118 837</a></li>
          <li><a href="https://zalo.me/0352118837" target="_blank" rel="noopener">Zalo: 0352 118 837</a></li>
          <li><a href="{up}index.html#contact" data-i="mail"><span data-i18n="ft.l8">Gửi yêu cầu</span></a></li>
        </ul>
      </div>
    </div>
    <div class="ft__base">
      <p>© <span id="yr">2026</span> Chef Minh Nguyễn. <span data-i18n="ft.rights">Bảo lưu mọi quyền.</span></p>
      <a class="sig" href="#" aria-label="Thiết kế bởi mattdesignwebsite">
        <i></i><span data-i18n="ft.by">Thiết kế</span> <b>mattdesignwebsite</b>
      </a>
    </div>
  </div>
</footer>

<div class="dock">
  <a href="https://www.facebook.com/Minhnguyensg0110/" target="_blank" rel="noopener" aria-label="Facebook" data-i="fb"></a>
  <a href="#" aria-label="TikTok" data-i="tiktok"></a>
  <a href="https://zalo.me/0352118837" target="_blank" rel="noopener" aria-label="Zalo" data-i="zalo"></a>
  <button class="dock__top" type="button" id="to-top" aria-label="Về đầu trang" data-i="up"></button>
</div>

<script src="{'../' * depth}js/site.js" defer></script>
</body>
</html>
'''


BIOMODAL = """<div class="modal" id="bio-modal" role="dialog" aria-modal="true" aria-labelledby="bio-title">
  <div class="modal__bg" data-close></div>
  <div class="modal__panel">
    <button class="modal__close" type="button" data-close aria-label="Đóng">✕</button>
    <div class="modal__body">
      <span class="idx" data-i18n="craft.eyebrow">Hành trình</span>
      <h3 id="bio-title" data-i18n="bio.title">Tiểu sử hoạt động và thành tích</h3>
      <p class="modal__sub" data-i18n="bio.sub">Chef Minh Nguyễn · 2008 → nay</p>
      {TIMELINE}
      <p class="eyebrow" style="margin-top:44px" data-i18n="bio.roles">Vai trò hiện tại</p>
      {ROLES}
    </div>
  </div>
</div>
"""

MODAL = '''<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal__bg" data-close></div>
  <div class="modal__panel">
    <button class="modal__close" type="button" data-close aria-label="Đóng">✕</button>
    <div class="modal__hero" id="modal-hero"></div>
    <div class="modal__body">
      <span class="idx" id="modal-idx"></span>
      <h3 id="modal-title"></h3>
      <p class="modal__sub" id="modal-sub"></p>
      <div class="modal__story" id="modal-story"></div>
      <div class="modal__alt" id="modal-alt"></div>
    </div>
  </div>
</div>
'''


def biomodal():
    R('bio.title', 'Tiểu sử hoạt động và thành tích', 'Career and achievements')
    R('bio.sub', 'Chef Minh Nguyễn · 2008 → nay', 'Chef Minh Nguyễn · 2008 → today')
    R('bio.roles', 'Vai trò hiện tại', 'Current roles')
    return BIOMODAL.replace('{TIMELINE}', bio_timeline()).replace('{ROLES}', bio_roles())


def pagehead(crumb_html, eyebrow, h1, lead='', key=''):
    """eyebrow / h1 / lead có thể là chuỗi (chỉ tiếng Việt) hoặc tuple (vi, en)."""
    def two(v, k):
        if isinstance(v, tuple):
            return 'data-i18n="%s">%s' % (k, R(k, v[0], v[1]))
        return '>%s' % v
    eb = two(eyebrow, key + '.eyebrow')
    hh = two(h1, key + '.h')
    lead_html = ''
    if lead:
        lead_html = '<p class="lead" %s</p>' % two(lead, key + '.lead')
    return f'''<section class="pagehead">
  <div class="wrap">
    <p class="crumb">{crumb_html}</p>
    <p class="eyebrow" {eb}</p>
    <h1 class="h-display" style="font-size:clamp(2.4rem,5.4vw,4rem)" {hh}</h1>
    {lead_html}
  </div>
</section>
'''



# ============================================================
# TIỂU SỬ — trích từ tệp Chef cung cấp
# ============================================================
BIO = [
    ('2008 – 2012', 'kitchen',
     ('Bén duyên với nghề bếp khi mới 14 tuổi, bắt đầu làm việc trong bếp nhà hàng của gia đình tại Nhà Bè, TP. Hồ Chí Minh.',
      'Came to the trade at fourteen, starting in the kitchen of the family restaurant in Nhà Bè, Ho Chi Minh City.')),
    ('2012 – 2014', 'kitchen',
     ('Bếp chính tại khách sạn Hương Sen, tiêu chuẩn 3 sao, trung tâm TP. Hồ Chí Minh.',
      'Head of the line at the three-star Hương Sen Hotel in central Ho Chi Minh City.')),
    ('2014', 'world',
     ('Sang Thái Lan tu nghiệp để học hỏi từ môi trường quốc tế, trở về nước khi Bangkok xảy ra biến cố.',
      'Trained in Thailand to learn from an international kitchen, returning home when unrest broke out in Bangkok.')),
    ('2015', 'kitchen',
     ('Bếp phó nhà hàng The Kafe, TP. Hồ Chí Minh — chuỗi Việt Nam vừa gọi vốn nước ngoài 3,8 triệu đô la, doanh thu 2 – 2,8 tỷ đồng mỗi tháng.',
      'Sous chef at The Kafe, Ho Chi Minh City — a Vietnamese chain that had just raised 3.8 million USD, turning over 2 – 2.8 billion VND a month.')),
    ('2015', 'award',
     ('Huy chương đồng cuộc thi Đầu bếp Việt Nam Tài năng, phần thi set menu món Việt. Cùng năm đạt huy chương bạc giải Đầu bếp trẻ Việt Nam Tài năng do hiệp hội đầu bếp thế giới tổ chức.',
      'Bronze medal at Vietnam Talented Chef for the Vietnamese set-menu round, plus silver at the Young Talented Chef award organised by the world chefs association.')),
    ('2016 – 2017', 'world',
     ('Bếp trưởng nhà hàng Indo tại Aarhus, thành phố lớn thứ hai Đan Mạch. Cùng đội ngũ đưa nhà hàng vào top 2 nhà hàng châu Á ngon nhất thành phố do giới phê bình bình chọn, lên báo và truyền hình Đan Mạch.',
      'Head chef at Indo in Aarhus, Denmark’s second city. With his team he took the restaurant into the city’s top two Asian restaurants as voted by critics, with coverage in Danish press and television.')),
    ('2018', 'world',
     ('Bếp phó nhà hàng Cavas tại Frankfurt, Đức, dưới sự dẫn dắt của bếp trưởng hai sao Michelin Michael Riemenschneider — nơi học thế nào là ẩm thực châu Âu đỉnh cao.',
      'Sous chef at Cavas in Frankfurt, Germany, under two-Michelin-star chef Michael Riemenschneider — where he learned what European fine dining really demands.')),
    ('2019', 'home',
     ('Quay về Việt Nam tìm nguồn cảm hứng để dựng một hướng đi riêng cho ẩm thực Việt.',
      'Returned to Vietnam to find the material for his own direction in Vietnamese cooking.')),
    ('2020 – 2023', 'home',
     ('Sống và làm việc tại Đồng Văn, Hà Giang. Chủ một homestay tại Làng cổ Thiên Hương.',
      'Lived and worked in Đồng Văn, Hà Giang, running a homestay in the old village of Thiên Hương.')),
    ('2022', 'award',
     ('Huy chương vàng cuộc thi Đầu bếp Việt Nam Tài năng, phần thi các món thịt bò Mỹ.',
      'Gold medal at Vietnam Talented Chef in the US beef category.')),
    ('2023', 'kitchen',
     ('Bếp trưởng điều hành Senna Wellness Retreat Bắc Ninh, tiêu chuẩn 4 sao. Phục vụ các buổi tiệc lớn cho giới doanh nhân và quan chức cấp cao, dẫn dắt đội bếp hơn 20 người.',
      'Executive chef at the four-star Senna Wellness Retreat in Bắc Ninh, cooking for large events for business leaders and senior officials, leading a brigade of more than twenty.')),
    ('2023', 'tv',
     ('Top 4 chung cuộc Top Chef phiên bản Việt Nam, phát sóng trên VTV3, tranh tài cùng hàng nghìn thí sinh cả nước.',
      'Finished in the top four of Top Chef Vietnam on VTV3, against thousands of entrants nationwide.')),
    ('2024 – 2025', 'world',
     ('Sống và làm việc tại Budapest, Hungary. Thành lập công ty Le-Ng, chuyên cung cấp giải pháp ẩm thực và set up nhà hàng, quán ăn tại châu Âu.',
      'Based in Budapest, Hungary. Founded Le-Ng, providing culinary solutions and restaurant set-up across Europe.')),
    ('2024', 'award',
     ('Giải thưởng Đầu bếp Bạc do hiệp hội đầu bếp quốc tế Best Gastronomie tại Pháp trao tặng.',
      'Silver Chef award from the international Best Gastronomie association in France.')),
    ('2024', 'award',
     ('Danh hiệu Master Chef, hạng mục World’s Master Chef của International Business Alliances tại Singapore.',
      'Named Master Chef in the World’s Master Chef category by International Business Alliances in Singapore.')),
    ('2025', 'tv',
     ('Tham gia Siêu Bếp trên HTV7 khung giờ vàng. Ba tập đối đầu ba đầu bếp chuyên nghiệp với ba sở trường khác nhau: thắng 2, hoà 1.',
      'Appeared on Siêu Bếp in HTV7’s prime slot, facing three professional chefs across three episodes: two wins, one draw.')),
]

ROLES = [
    (('Phó chủ tịch — đại diện Việt Nam', 'Vice President — Vietnam representative'),
     ('Chefs Sans Frontières (CSFint), hiệp hội đầu bếp không biên giới quốc tế do đầu bếp người Anh Alan Coxon sáng lập.',
      'Chefs Sans Frontières (CSFint), the international chefs-without-borders association founded by British chef Alan Coxon.')),
    (('Sáng lập và điều hành', 'Founder and director'),
     ('Viet Chefs Worldwide — tổ chức kết nối đầu bếp Việt Nam trên toàn thế giới.',
      'Viet Chefs Worldwide — connecting Vietnamese chefs across the globe.')),
]


def bio_timeline(depth=0, light=False):
    cls = 'tl tl--light' if light else 'tl'
    out = ['<ol class="%s">' % cls]
    for i, (year, kind, text) in enumerate(BIO, 1):
        t = R('bio.%d' % i, text[0], text[1])
        out.append(
            '  <li class="tl__i tl__i--%s"><span class="tl__y">%s</span>'
            '<span class="tl__t" data-i18n="bio.%d">%s</span></li>' % (kind, year, i, t))
    out.append('</ol>')
    return '\n'.join(out)


def bio_roles():
    out = ['<div class="roles">']
    for i, (title, desc) in enumerate(ROLES, 1):
        t = R('role.t%d' % i, title[0], title[1])
        d = R('role.d%d' % i, desc[0], desc[1])
        out.append('  <div class="role"><b data-i18n="role.t%d">%s</b>'
                   '<span data-i18n="role.d%d">%s</span></div>' % (i, t, i, d))
    out.append('</div>')
    return '\n'.join(out)


DISHES = [
    ('1', 'mon-01-trai-giac.jpg',  '01', 'Gỏi tôm sú',
     'Tôm sú biển tái húng quế · sốt nước mắm đậu phộng · bọt trái giác', 'dish--a'),
    ('2', 'mon-02-goi-tom-su.jpg', '02', 'Nọng heo đen vùng cao nướng muối ớt',
     'Sous-vide · rau củ ủ bơ · sốt mù tạc mật ong bạc hà', 'dish--b'),
    ('3', 'mon-03-ca-tuyet.jpg',   '03', 'Cá tuyết Na Uy dry-aged áp chảo',
     'Tỏi đen Lý Sơn · tiêu Phú Quốc · bánh phồng tôm', 'dish--h'),
    ('4', 'mon-04-nong-heo.jpg',   '04', 'Gà đen H’Mông cuộn bắp non nướng xông gỗ quế',
     'Sốt chẩm chéo hạt dổi · măng rừng nướng · nếp nương hấp lá dứa', 'dish--h'),
]


def dish_grid(depth=0):
    up = '../' * depth
    out = ['    <div class="dish-grid reveal">']
    for did, img, idx, name, sub, cls in DISHES:
        out.append(f'''      <button class="dish {cls}" type="button" data-dish="{did}">
        <div class="dish__img">
          <img src="{up}assets/{img}" alt="{name}" width="1800" height="1199" loading="lazy" decoding="async">
          <span class="dish__more" data-i18n="cui.more">Đọc câu chuyện</span>
        </div>
        <div class="dish__cap">
          <span class="idx">{idx}</span>
          <h3 class="h-3" data-i18n="cui.d{did}n">{name}</h3>
          <p data-i18n="cui.d{did}s">{sub}</p>
        </div>
      </button>
''')
    out.append('    </div>')
    return '\n'.join(out)


# ============================================================
# TRANG CHỦ
# ============================================================
def build_index():
    return head('Chef Minh Nguyễn — Tư vấn ẩm thực · Đào tạo · Private Chef',
                'Chef Minh Nguyễn — 15 năm nghề bếp. Tư vấn ẩm thực, đào tạo chuyên nghiệp, hợp tác thương hiệu và trải nghiệm private dining.') + header() + '''
<main id="top">

<!-- ================= HERO ================= -->
<section class="hero hero--video">
  <div class="hero__video" aria-hidden="true">
    <video id="hero-video" poster="assets/hero-poster.jpg"
           autoplay loop muted playsinline preload="auto"
           disablepictureinpicture disableremoteplayback>
      <source src="assets/hero.mp4" type="video/mp4">
    </video>
  </div>

  <div class="wrap hero__grid2">
    <div>
      <p class="hero__role rise rise--1" data-i18n="hero.role">Tư vấn ẩm thực · Đào tạo · Private Chef</p>
      <h1 class="h-display hero__name">
        <span class="word"><span>Chef</span></span>
        <span class="word"><span>Minh Nguyễn</span></span>
      </h1>
      <p class="hero__sub type" data-type-key="hero.sub"
         data-fallback="Hơn mười lăm năm trong bếp. Ẩm thực dần được chuyển mình bằng những kỹ thuật hiện đại, những câu chuyện về nguyên liệu, cùng các giá trị truyền thống — cho nhà hàng, cho người học nghề, và cho đến những bữa tiệc sang trọng."></p>
      <div class="hero__cta rise rise--4">
        <a href="the-chef.html" class="btn btn--solid btn--pulse" data-i18n="hero.cta1">Xem hành trình</a>
        <a href="#contact" class="btn btn--pulse" data-i18n="hero.cta2">Làm việc cùng Chef</a>
      </div>
    </div>

    <div class="hero__portrait rise rise--3">
      <img src="assets/chef-portrait.jpg" alt="Chef Minh Nguyễn trong bếp"
           width="900" height="1200" fetchpriority="high" decoding="async">
      <span class="hero__cap" data-i="toque"><span data-i18n="hero.cap">Top Chef Việt Nam 2023 · Top 4</span></span>
    </div>
  </div>

  <button class="sound-btn" id="sound-btn" type="button" aria-pressed="false">
    <i></i><span data-i18n="hero.sound">Đang tắt tiếng</span>
  </button>
</section>

<!-- ================= HÀNH TRÌNH ================= -->
<section class="band band--raised" id="craft">
  <div class="wrap">
    <div class="craft reveal">
      <div>
        <div class="craft__num" id="counter">15</div>
        <div class="craft__numlab" data-i18n="craft.label">Năm theo nghề</div>
      </div>
      <div>
        <p class="eyebrow" data-i18n="craft.eyebrow">Hành trình</p>
        <h2 class="h-2" data-i18n="craft.h">Nghề bếp học bằng thời gian,<br>không học bằng lối tắt.</h2>
        <p class="lead" data-i18n="craft.lead">Chef Minh Nguyễn hiện nổi bật với vai trò Nhà sáng lập kiêm CEO của cộng đồng Vietchefs Worldwide (VCW) và gia nhập hiệp hội International Chefs Sans Frontières (CSFint). Anh đã tranh tài tại <a href="https://www.facebook.com/Minhnguyensg0110/" target="_blank" rel="noopener">Top Chef Việt Nam 2023</a> và Siêu Bếp 2025, đẩy mạnh các giá trị cốt lõi của ẩm thực Việt Nam trước thềm APEC 2027, lan toả văn hoá ẩm thực thuần vị và kết nối thị trường.</p>
        <div class="stats">
          <div class="stat"><b>Top 4</b><span data-i18n="craft.s1s">Top Chef Việt Nam 2023 · VTV3</span></div>
          <div class="stat"><b>Master Chef</b><span data-i18n="craft.s2s">World’s Master Chef 2024 · Singapore</span></div>
          <div class="stat"><b>HCV · HCĐ</b><span data-i18n="craft.s3s">Đầu bếp Việt Nam Tài năng 2022 &amp; 2015</span></div>
        </div>
        <div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap">
          <button type="button" class="btn btn--solid" id="open-bio" data-i="book"><span data-i18n="craft.cta2">Đọc tiểu sử đầy đủ</span></button>
          <a href="the-chef.html" class="btn" data-i="arrow" data-i-pos="end"><span data-i18n="craft.cta">Xem trang hành trình</span> </a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ================= ẨM THỰC ================= -->
<section class="band band--shell" id="cuisine" data-nav="light">
  <div class="wrap">
    <div class="reveal" style="max-width:640px;margin-bottom:56px">
      <p class="eyebrow" data-i18n="cui.eyebrow">Ẩm thực</p>
      <h2 class="h-2" data-i18n="cui.h">Món ăn là bằng chứng,<br>không phải thực đơn.</h2>
      <p class="lead" data-i18n="cui.lead">Năm món, năm vùng đất. Chạm vào từng món để đọc câu chuyện Chef Minh viết cho nó.</p>
    </div>
''' + dish_grid() + '''
    <div style="margin-top:52px" class="reveal">
      <a href="cuisine.html" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="cui.cta2">Xem trang ẩm thực </a>
    </div>
  </div>
</section>

<!-- ================= TRIẾT LÝ ================= -->
<section class="band band--dark" id="philosophy" style="text-align:center">
  <div class="ph-bg" style="--ph-bg:url('assets/logo-banner.jpg')" aria-hidden="true"></div>
  <div class="wrap">
    <div class="stalk-rule reveal" style="margin-bottom:38px">
      <svg viewBox="60 0 80 44" aria-hidden="true"><use href="#stalk"/></svg>
    </div>

    <blockquote class="reveal" style="margin:0 auto;max-width:20ch">
      <p style="font-family:var(--display);font-weight:400;margin:0;color:var(--shell)" data-i18n="phil.quote">“Ẩm thực Việt không chỉ là món ăn, mà là câu chuyện về văn hóa, con người và vùng đất.”</p>
      <p class="phil-sub" data-i18n="phil.quote2">“Giữ hồn Việt trong từng nguyên liệu, dùng kỹ thuật hiện đại để đưa giá trị ấy đối thoại với thế giới.”</p>
      <footer style="margin-top:24px"><span class="label" data-i18n="phil.attr">Chef Minh Nguyễn</span></footer>
    </blockquote>

    <div class="medals reveal">
      <span class="medal medal--years" data-i="years"><b data-i18n="med.y">15+ năm</b></span>
      <span class="medal medal--gold" data-i="medal"><b>HCV</b> <span data-i18n="med.g">Đầu bếp Việt Nam Tài năng 2022 · U.S. Beef</span></span>
      <span class="medal medal--silver" data-i="medal"><b>HCB</b> <span data-i18n="med.s">Đầu bếp trẻ Việt Nam Tài năng 2015</span></span>
      <span class="medal medal--bronze" data-i="medal"><b>HCĐ</b> <span data-i18n="med.b">Đầu bếp Việt Nam Tài năng 2015</span></span>
      <span class="medal" data-i="toque"><b data-i18n="med.t">Top 4</b> <span data-i18n="med.t2">Top Chef Việt Nam 2023</span></span>
      <span class="medal" data-i="cutlery"><b data-i18n="med.m">Master Chef</b> <span data-i18n="med.m2">Singapore 2024</span></span>
    </div>

    <div class="reveal" style="margin-top:30px;display:flex;gap:30px;justify-content:center;flex-wrap:wrap">
      <span class="label" data-i="leaf" data-i18n="phil.t1">Văn hóa</span>
      <span class="label" data-i="users" data-i18n="phil.t2">Con người</span>
      <span class="label" data-i="pin" data-i18n="phil.t3">Vùng đất</span>
    </div>
  </div>
</section>

<!-- ================= DẢI CHỮ CHẠY ================= -->
<div class="ticker" id="ticker" aria-hidden="true"></div>

<!-- ================= BỐN TRỤ ================= -->
<section class="band band--raised" id="pillars">
  <div class="wrap">
    <div class="reveal" style="max-width:600px;margin-bottom:52px">
      <p class="eyebrow" data-i18n="pil.eyebrow">Dịch vụ</p>
      <h2 class="h-2" data-i18n="pil.h">Bốn cách để làm việc<br>cùng Chef Minh.</h2>
    </div>
    <div class="pillars reveal">
      <article class="pillar pillar--lg">
        <span class="pillar__rank" data-i18n="pil.focus">Đang mở rộng</span>
        <h3 class="h-3" data-i18n="pil.p1h">Đào tạo</h3>
        <p class="small" data-i18n="pil.p1s">Dạy nghề bếp cho người muốn đi đường dài, không dạy mẹo.</p>
        <ul>
          <li data-i18n="pil.p1a">Khai giảng liên tục các khoá 1 kèm 1 VIP</li>
          <li data-i18n="pil.p1b">Thiết kế menu cá nhân hoá</li>
          <li data-i18n="pil.p1c">Lớp chuyên đề món Việt – Âu trong ngày</li>
          <li data-i18n="pil.p1d">Đào tạo học viên online từ xa</li>
          <li data-i18n="pil.p1e">Chuyển giao công thức sốt các loại</li>
        </ul>
        <a href="academy.html" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="pil.p1cta">Xem các khóa học </a>
      </article>
      <article class="pillar pillar--lg">
        <span class="pillar__rank" data-i18n="pil.focus">Đang mở rộng</span>
        <h3 class="h-3" data-i18n="pil.p2h">Thương hiệu</h3>
        <p class="small" data-i18n="pil.p2s">Đồng hành cùng các nhãn hàng bằng chuyên môn lâu năm và cả hình ảnh thực tế.</p>
        <ul>
          <li data-i18n="pil.p2a">Hợp tác quảng bá cùng nhãn hàng</li>
          <li data-i18n="pil.p2b">KOL ngành ẩm thực</li>
          <li data-i18n="pil.p2c">Sản xuất video, hình ảnh quảng bá sản phẩm</li>
          <li data-i18n="pil.p2d">Biểu diễn ẩm thực quảng bá</li>
        </ul>
        <a href="services.html#brand" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="pil.p2cta">Xem hồ sơ hợp tác </a>
      </article>
      <article class="pillar pillar--sm">
        <h3 class="h-3" data-i18n="pil.p3h">Tư vấn</h3>
        <p class="small" data-i18n="pil.p3s">Dựng bếp, dựng thực đơn, dựng cách vận hành.</p>
        <ul>
          <li data-i18n="pil.p3a">Phát triển thực đơn</li>
          <li data-i18n="pil.p3b">Setup bếp và nhà hàng</li>
          <li data-i18n="pil.p3c">Vận hành và huấn luyện đội bếp</li>
          <li data-i18n="pil.p3d">Giải pháp khắc phục để tối ưu vận hành nhà bếp</li>
        </ul>
        <a href="services.html#consulting" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="pil.p3cta">Trao đổi về nhà hàng </a>
      </article>
      <article class="pillar pillar--sm">
        <h3 class="h-3" data-i18n="pil.p4h">Trải nghiệm</h3>
        <p class="small" data-i18n="pil.p4s">Cá nhân hoá bữa tiệc của bạn bằng cách cộng tác với Chef Minh Nguyễn trong những dịch vụ dưới đây.</p>
        <ul>
          <li data-i18n="pil.p4a">Private Chef</li>
          <li data-i18n="pil.p4b">Private Dining</li>
          <li data-i18n="pil.p4c">Sự kiện riêng</li>
        </ul>
        <a href="services.html#experiences" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="pil.p4cta">Đặt trải nghiệm </a>
      </article>
    </div>
  </div>
</section>

<!-- ================= ACADEMY ================= -->
<section class="band band--shell" id="academy" data-nav="light">
  <div class="wrap">
    <div class="reveal" style="max-width:600px;margin-bottom:48px">
      <p class="eyebrow" data-i18n="aca.eyebrow">Academy</p>
      <h2 class="h-2" data-i18n="aca.h">Học cùng Chef Minh.</h2>
      <p class="lead" data-i18n="aca.lead">Lớp giới hạn số người để mỗi học viên đều được đứng bếp thật.</p>
    </div>
''' + course_cards() + '''
    <div style="margin-top:20px" class="reveal">
      <a href="academy.html" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="aca.all">Xem trang Academy </a>
    </div>
  </div>
</section>

<!-- ================= TRUYỀN THÔNG ================= -->
<section class="band band--dark" id="trust">
  <div class="wrap">
    <div class="reveal" style="max-width:640px;margin-bottom:48px">
      <p class="eyebrow" data-i18n="tru.eyebrow">Truyền thông &amp; thành tích</p>
      <h2 class="h-2" data-i18n="tru.h">Nơi Chef Minh<br>đã xuất hiện.</h2>
    </div>
''' + video_grid(limit=3, feature=True) + '''
''' + article_grid(limit=3, feature=True) + '''

    <div style="margin-top:44px" class="reveal">
      <a href="press.html" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="tru.all">Xem tất cả </a>
    </div>

    <div class="kit reveal">
      <div>
        <h3 class="h-3" data-i18n="tru.kith">Dành cho nhãn hàng và đối tác</h3>
        <p class="small" data-i18n="tru.kits">Hồ sơ năng lực đầy đủ: kinh nghiệm, số liệu độ phủ, các chiến dịch đã thực hiện và hình thức hợp tác.</p>
      </div>
      <a href="#contact" data-need="brand" class="btn btn--solid" data-i18n="tru.kitcta">Nhận hồ sơ năng lực</a>
    </div>
  </div>
</section>

<!-- ================= BLOG ================= -->
<section class="band band--shell" id="blog" data-nav="light">
  <div class="wrap">
    <div class="reveal" style="max-width:620px;margin-bottom:48px">
      <p class="eyebrow" data-i18n="blg.eyebrow">Kiến thức bếp</p>
      <h2 class="h-2" data-i18n="blg.h">Kiến thức bếp,<br>viết cho người muốn hiểu.</h2>
      <p class="lead" data-i18n="blg.lead">Kỹ thuật, nguyên liệu Việt và cách nấu — giải thích bằng ngôn ngữ của người đứng bếp.</p>
    </div>
''' + post_grid() + '''
    <div style="margin-top:44px" class="reveal">
      <a href="blog.html" class="link-arrow" data-i="arrow" data-i-pos="end" data-i18n="blg.all">Xem tất cả bài viết </a>
    </div>
  </div>
</section>

''' + contact_section() + '''
</main>
''' + MODAL + biomodal() + footer()


# ============================================================
# KHỐI DÙNG LẠI
# ============================================================
COURSES = [
    ('academy-01.jpg',
     ('Học nấu ăn để làm chủ', 'Cook to own your kitchen'),
     ('Dành cho người sắp mở nhà hàng và muốn tự đứng bếp, tự giữ công thức.',
      'For people about to open a restaurant who want to run the stove and keep their own recipes.'),
     ('Khai giảng liên tục', 'Rolling intake'),
     [(('Thời lượng','Length'), ('Theo lịch của bạn','Your own schedule')),
      (('Quy mô lớp','Class size'), ('1 kèm 1 VIP','One-to-one VIP'))],
     [(('Khai giảng','Intake'), ('Liên tục quanh năm','All year round')),
      (('Địa điểm','Location'), ('TP. Hồ Chí Minh · hoặc online','Ho Chi Minh City · or online')),
      (('Đặc biệt','Special'), ('Thiết kế menu học theo yêu cầu học viên','Menu designed around each student')),
      (('Sau khoá','After'), ('Hỗ trợ kèm 24/7, ưu đãi tư vấn set up','24/7 follow-up, discounted set-up consulting'))],
     [('Muốn mở nhà hàng và tự giữ bí quyết công thức','You want to open a restaurant and keep your own recipes'),
      ('Chưa biết cách tính giá bán và kiểm soát chi phí','You are unsure how to price dishes and control cost'),
      ('Muốn vận hành bếp không lệ thuộc vào nhân sự','You want a kitchen that does not depend on one hire')]),

    ('academy-02.jpg',
     ('Lớp món Á – Âu cơ bản', 'Asian & European foundation'),
     ('Dành cho người mới bước vào nghề bếp, cần một lộ trình rõ ràng.',
      'For people entering the trade who need a clear path.'),
     ('Khai giảng liên tục', 'Rolling intake'),
     [(('Thời lượng','Length'), ('1 – 2 tháng','1 – 2 months')),
      (('Quy mô lớp','Class size'), ('Tối đa 2 – 3 người','Max 2 – 3 students'))],
     [(('Khai giảng','Intake'), ('Liên tục quanh năm','All year round')),
      (('Lịch học','Schedule'), ('Phù hợp người vừa đi làm vừa học','Fits people working full time')),
      (('Địa điểm','Location'), ('TP. Hồ Chí Minh','Ho Chi Minh City')),
      (('Cách dạy','Teaching'), ('Truyền đạt bằng toàn bộ kinh nghiệm thực chiến','Taught from real kitchen experience'))],
     [('Muốn làm nghề bếp nhưng chưa biết bắt đầu từ đâu','You want to cook professionally but do not know where to start'),
      ('Muốn học từ một người thầy đã thành công trong nghề','You want to learn from someone who has done it')]),

    ('press-digicook.jpg',
     ('Khoá Á – Âu nâng cao', 'Asian & European advanced'),
     ('Dành cho người đã có nền, muốn đi sâu vào sốt, kỹ thuật và tư duy thi đấu.',
      'For cooks with a base who want depth in sauces, technique and competition thinking.'),
     ('Khai giảng hằng tháng', 'Monthly intake'),
     [(('Thời lượng','Length'), ('Theo lịch của bạn','Your own schedule')),
      (('Quy mô lớp','Class size'), ('Tối đa 1 – 2 người','Max 1 – 2 students'))],
     [(('Khai giảng','Intake'), ('Hằng tháng','Monthly')),
      (('Chuyên sâu','Depth'), ('Sốt nền và sốt đặc biệt do Chef sáng tạo','Base and signature sauces created by the Chef')),
      (('Kỹ năng','Skills'), ('Trang trí và các trường phái nấu ăn','Plating and major culinary schools')),
      (('Tư duy','Thinking'), ('Thi đấu ẩm thực và sáng tạo món','Competition and dish creation'))],
     [('Học các loại sốt đã thành công tại nhiều cuộc thi','Learn the sauces that won at competition'),
      ('Sắp xếp và vận hành nhà bếp chuyên nghiệp','Professional kitchen layout and operations'),
      ('Thuật ngữ chuyên ngành và tư duy sáng tạo món ăn','Industry terminology and creative thinking')]),
]


CHECK = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M4 12.5 9 18 20 6"/></svg>')


def course_cards(depth=0, full=False):
    up = '../' * depth
    out = ['    <div class="courses reveal">']
    for i, (img, name, desc, badge, spec, rows, asks) in enumerate(COURSES, 1):
        show = asks if full else asks[:2]
        ask = '\n'.join(
            '            <li>%s<span data-i18n="aca.c%da%d">%s</span></li>'
            % (CHECK, i, n, R('aca.c%da%d' % (i, n), a[0], a[1]))
            for n, a in enumerate(show, 1))
        sp = '\n'.join(
            '            <div><b data-i18n="aca.c%dsk%d">%s</b><span data-i18n="aca.c%dsv%d">%s</span></div>'
            % (i, n, R('aca.c%dsk%d' % (i, n), k[0], k[1]),
               i, n, R('aca.c%dsv%d' % (i, n), v[0], v[1]))
            for n, (k, v) in enumerate(spec, 1))
        rw = '\n'.join(
            '            <li><b data-i18n="aca.c%drk%d">%s</b><span data-i18n="aca.c%drv%d">%s</span></li>'
            % (i, n, R('aca.c%drk%d' % (i, n), k[0], k[1]),
               i, n, R('aca.c%drv%d' % (i, n), v[0], v[1]))
            for n, (k, v) in enumerate(rows, 1))
        nm = R('aca.c%dh' % i, name[0], name[1])
        ds = R('aca.c%ds' % i, desc[0], desc[1])
        bd = R('aca.c%dbadge' % i, badge[0], badge[1])
        out.append(f'''      <article class="course">
        <div class="mo-frame" style="position:relative">
          <img src="{up}assets/{img}" alt="{nm}" width="1600" height="1000" loading="lazy" decoding="async">
          <span class="course__badge" data-i="clock"><span data-i18n="aca.c{i}badge">{bd}</span></span>
        </div>
        <div class="course__in">
          <h3 data-i18n="aca.c{i}h">{nm}</h3>
          <p class="course__desc" data-i18n="aca.c{i}s">{ds}</p>
          <div class="course__spec">
{sp}
          </div>
          <ul class="course__ask">
{ask}
          </ul>
          <ul class="course__rows">
{rw}
          </ul>
          <a class="course__more" href="{up}index.html?need=hoc#contact" data-i="arrow" data-i-pos="end"><span data-i18n="aca.more">Xem chi tiết &amp; đăng ký</span> </a>
        </div>
      </article>''')
    out.append('    </div>')
    R('aca.more', 'Xem chi tiết & đăng ký', 'See details & register')
    return '\n'.join(out)



# ============================================================
# BÀI BÁO — link thật, đã bỏ tham số theo dõi của Facebook
# ============================================================
ARTICLES = [
    ('https://htv.vn/sieu-bep-mua-2-tap-8-sieu-bep-minh-nguyen-va-nhung-mon-an-thuong-nho-mien-tay-222260102181331923.htm',
     'mon-01-trai-giac.jpg', 'HTV', '01 · 2026',
     ('Siêu Bếp mùa 2 · Tập 8 — Những món ăn thương nhớ miền Tây',
      'Siêu Bếp season 2 · Episode 8 — Dishes that miss the Mekong Delta'),
     ('Chef Minh Nguyễn mang trái giác và tôm sú, hai đặc sản quê hương Sóc Trăng, lên sóng HTV7.',
      'Chef Minh Nguyễn brought wild grape and tiger prawn, two specialities of his native Sóc Trăng, to HTV7.')),

    ('https://htv.vn/sieu-bep-mua-2-tap-5-sieu-bep-minh-nguyen-chinh-phuc-thuc-khach-voi-mon-an-chua-lanh-222251212082122084.htm',
     'press-sieubep-01.jpg', 'HTV', '12 · 2025',
     ('Siêu Bếp mùa 2 · Tập 5 — Chinh phục thực khách bằng món ăn chữa lành',
      'Siêu Bếp season 2 · Episode 5 — Winning the table with food that heals'),
     ('Món xôi gà thực dưỡng không dùng đạm động vật, kể lại quãng thời gian Chef sống ở vùng cao Tây Bắc.',
      'A macrobiotic sticky rice dish without animal protein, retelling the time the Chef spent in the northern highlands.')),

    ('https://vietnamtre.vn/chef-minh-nguyen-su-gia-cua-am-thuc-viet-tren-dat-chau-au-va-nhung-chia-se-day-thu-vi-c2401410/',
     'chef-portrait.jpg', 'Việt Nam Trẻ', '2024',
     ('Sứ giả của ẩm thực Việt trên đất châu Âu',
      'An ambassador for Vietnamese food in Europe'),
     ('Chef Minh Nguyễn nói về việc mang hương vị Việt tới thực khách châu Âu và những gì học được trên đường đi.',
      'Chef Minh Nguyễn on bringing Vietnamese flavour to European diners, and what the road taught him.')),

    ('https://www.yan.vn/chef-minh-nguyen-danh-bai-thach-thuc-xay-dung-su-nghiep-dau-bep-quoc-te-330841.html',
     'chef-wide.jpg', 'YAN', '12 · 2023',
     ('Đánh bại thách thức, xây dựng sự nghiệp đầu bếp quốc tế',
      'Beating the odds, building an international cooking career'),
     ('Chân dung hành trình từ những quán ăn nhỏ tới vị trí bếp trưởng tại châu Âu, và góc nhìn về đưa ẩm thực Việt ra thế giới.',
      'From small eateries to head chef in Europe, and a view on taking Vietnamese food to the world.')),

    ('https://doisongvathuonghieu.com/minh-nguyen-vuot-qua-nghich-canh-tro-thanh-dau-bep-vuon-tam-quoc-te/',
     'press-award.jpg', 'Đời Sống & Thương Hiệu', '09 · 2023',
     ('Vượt qua nghịch cảnh, trở thành đầu bếp vươn tầm quốc tế',
      'Through hardship to an international kitchen career'),
     ('Bếp phó tại Việt Nam năm 18 tuổi, bếp trưởng tại châu Âu năm 20 tuổi, và kế hoạch dẫn dắt thế hệ đầu bếp trẻ.',
      'Sous chef in Vietnam at eighteen, head chef in Europe at twenty, and a plan to bring young Vietnamese cooks with him.')),

    ('https://thanhnien.vn/hoa-hau-hhen-nie-bat-tay-ngoc-chau-lam-giam-khao-top-chef-viet-nam-2023-185230711122234072.htm',
     'press-topchef.jpg', 'Thanh Niên', '07 · 2023',
     ('Top Chef Việt Nam 2023 — mùa giải Chef Minh vào Top 4',
      'Top Chef Vietnam 2023 — the season Chef Minh reached the Top 4'),
     ('Bài giới thiệu mùa giải và ban giám khảo của Top Chef Việt Nam 2023, sân chơi Chef Minh Nguyễn tranh tài.',
      'A preview of the season and judging panel of Top Chef Vietnam 2023, the contest Chef Minh Nguyễn competed in.')),
]


def article_grid(limit=None, depth=0, feature=False):
    up = '../' * depth
    items = ARTICLES[:limit] if limit else ARTICLES
    cls = 'press-grid press-grid--feat' if feature else 'press-grid'
    out = ['    <div class="%s reveal">' % cls]
    for i, (url, img, src, date, title, sub) in enumerate(items, 1):
        t = R('art.t%d' % i, title[0], title[1])
        s = R('art.s%d' % i, sub[0], sub[1])
        out.append(f'''      <a class="pcard" href="{url}" target="_blank" rel="noopener">
        <span class="pcard__img">
          <img src="{up}assets/{img}" alt="{t}" width="820" height="470" loading="lazy" decoding="async">
          <span class="pcard__src">{src}</span>
        </span>
        <span class="pcard__body">
          <span class="pcard__meta">{date}</span>
          <h3 data-i18n="art.t{i}">{t}</h3>
          <p data-i18n="art.s{i}">{s}</p>
          <span class="pcard__go" data-i="arrow" data-i-pos="end"><span data-i18n="art.read">Đọc bài viết</span> </span>
        </span>
      </a>''')
    out.append('    </div>')
    R('art.read', 'Đọc bài viết', 'Read the article')
    return '\n'.join(out)


VIDEOS = [
    ('ApH3DkrNGws', 'Chef Minh Nguyễn — Video 01'),
    ('zcRWwyw8PH8', 'Chef Minh Nguyễn — Video 02'),
    ('yWJtd__ER98', 'Chef Minh Nguyễn — Video 03'),
    ('ClLg9_NEa4k', 'Chef Minh Nguyễn — Video 04'),
    ('0kXq-ExsEbA', 'Chef Minh Nguyễn — Video 05'),
]


def video_grid(limit=None, feature=False):
    """Nhúng YouTube kiểu nhẹ: chỉ tải ảnh bìa, bấm mới nạp trình phát.
    Nhúng thẳng 5 iframe sẽ kéo về hơn 3MB script và làm chậm trang rất nhiều."""
    items = VIDEOS[:limit] if limit else VIDEOS
    cls = 'videos videos--feat' if feature else 'videos'
    out = ['    <div class="%s reveal">' % cls]
    for vid, title in items:
        out.append(f'''      <button class="lyt" type="button" data-yt="{vid}" aria-label="Phát: {title}">
        <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{title}"
             width="480" height="360" loading="lazy" decoding="async">
        <span class="lyt__play" aria-hidden="true"></span>
        <span class="lyt__cap">{title}</span>
      </button>''')
    out.append('    </div>')
    return '\n'.join(out)


MEDIA = [
    ('press-topchef.jpg', ('Truyền hình','Television'), ('Top Chef Vietnam 2023','Top Chef Vietnam 2023'),
     ('Chef Minh Nguyễn vào tới Top 4 của mùa giải.','Chef Minh Nguyễn reached the Top 4 of the season.'), ''),
    ('press-award.jpg', ('Giải thưởng','Award'), ('Best Master Chef Awards 2024','Best Master Chef Awards 2024'),
     ('Chứng nhận trao cho Nguyen Thai Minh, tháng 9/2024.','Certificate awarded to Nguyen Thai Minh, September 2024.'), 'media-card--tall'),
    ('press-sieubep-01.jpg', ('Truyền hình','Television'), ('Siêu Bếp — HTV7','Siêu Bếp — HTV7'),
     ('Tham gia chương trình Siêu Bếp do TVHub sản xuất.','Appearing on Siêu Bếp, produced by TVHub.'), ''),
    ('press-sieubep-02.jpg', ('Truyền hình','Television'), ('Siêu Bếp — phần thi','Siêu Bếp — the challenge'),
     ('Một phần thi trong chương trình Siêu Bếp.','A challenge round on Siêu Bếp.'), ''),
    ('press-digicook.jpg', ('Sự kiện','Event'), ('DigiCook — Cặp đôi hoàn hảo Amway Queen','DigiCook — Amway Queen'),
     ('Đồng hành cùng người chơi trong suốt chương trình.','Working alongside contestants through the show.'), ''),
    ('press-oneriver.jpg', ('Hợp tác','Partnership'), ('One River','One River'),
     ('[CẦN XÁC NHẬN nội dung hợp tác]','[TO BE CONFIRMED]'), ''),
]


def media_grid(limit=None, depth=0):
    up = '../' * depth
    items = MEDIA[:limit] if limit else MEDIA
    out = ['    <div class="media-grid reveal">']
    for n, (img, cat, title, desc, extra) in enumerate(items, 1):
        cat = R('md.c%d' % n, cat[0], cat[1])
        title = R('md.t%d' % n, title[0], title[1])
        desc = R('md.d%d' % n, desc[0], desc[1])
        out.append(f'''      <article class="media-card {extra}">
        <img src="{up}assets/{img}" alt="{title}" width="1600" height="1066" loading="lazy" decoding="async">
        <div class="media-card__body">
          <span class="media-card__cat" data-i18n="md.c{n}">{cat}</span>
          <h3 data-i18n="md.t{n}">{title}</h3>
          <p data-i18n="md.d{n}">{desc}</p>
        </div>
      </article>''')
    out.append('    </div>')
    return '\n'.join(out)


POSTS = [
    ('blog/sous-vide.html', 'blog-sous-vide.jpg',
     ('Kỹ thuật bếp', 'Technique'),
     ('Sous vide: nấu bằng nhiệt độ, không nấu bằng thời gian',
      'Sous vide: cooking by temperature, not by time'),
     ('Vì sao 63°C giữ được thứ mà 100°C phá mất, và khi nào kỹ thuật này thực sự đáng dùng.',
      'Why 63°C keeps what 100°C destroys, and when the technique is actually worth it.')),
    ('blog/dry-aging.html', 'blog-dry-age.jpg',
     ('Nguyên liệu', 'Ingredients'),
     ('Dry-age: làm khô có kiểm soát để vị đậm hơn',
      'Dry-age: controlled drying for deeper flavour'),
     ('Nguyên lý đằng sau việc cố tình để nguyên liệu mất nước, và ranh giới giữa chín tới và hỏng.',
      'The principle behind deliberate moisture loss, and the line between aged and spoiled.')),
    ('blog/nuoc-dung.html', 'blog-nuoc-dung.jpg',
     ('Cách nấu', 'How to cook'),
     ('Nước dùng: phần không ai thấy nhưng quyết định cả món',
      'Stock: the part nobody sees that decides the dish'),
     ('Xương, nhiệt độ, thời gian và lý do nồi nước dùng không bao giờ được sôi bùng.',
      'Bones, temperature, time, and why a stock pot must never boil.')),
]


def post_grid(depth=0):
    up = '../' * depth
    out = ['    <div class="posts reveal">']
    for i, (link, img, cat, title, sub) in enumerate(POSTS, 1):
        c = R('blg.c%d' % i, cat[0], cat[1])
        t = R('blg.t%d' % i, title[0], title[1])
        s2 = R('blg.s%d' % i, sub[0], sub[1])
        out.append(f'''      <a class="post post-link" href="{up}{link}">
        <img src="{up}assets/{img}" alt="" width="1800" height="1199" loading="lazy" decoding="async">
        <span class="post__cat" data-i18n="blg.c{i}">{c}</span>
        <h3 data-i18n="blg.t{i}">{t}</h3>
        <p data-i18n="blg.s{i}">{s2}</p>
      </a>''')
    out.append('    </div>')
    return '\n'.join(out)


def contact_section(depth=0):
    up = '../' * depth
    return f'''<!-- ================= LIÊN HỆ ================= -->
<section class="band contact" id="contact">
  <div class="wrap">
    <div class="reveal">
      <h2 class="h-display" style="font-size:clamp(2.4rem,6vw,4.4rem)" data-i18n="con.h">Bắt đầu từ<br>việc của bạn.</h2>
      <p class="lead" style="margin:26px auto 0;text-align:center" data-i18n="con.lead">Chọn đúng nhu cầu để câu hỏi phía sau đi thẳng vào việc.</p>
    </div>

    <div class="contact-grid reveal">
      <div class="contact-grid__left">
        <p class="eyebrow" data-i18n="con.direct">Liên hệ trực tiếp</p>
        <div class="info-row">
          <span class="label" data-i18n="con.email">Email</span>
          <a href="mailto:thaiminhchef@gmail.com">thaiminhchef@gmail.com</a>
        </div>
        <div class="info-row">
          <span class="label" data-i18n="con.tel">Điện thoại</span>
          <span class="v"><a href="tel:+84352118837">0352 118 837</a> &nbsp;·&nbsp; <a href="tel:+84961838367">0961 838 367</a></span>
        </div>
        <div class="info-row">
          <span class="label">Zalo</span>
          <a href="https://zalo.me/0352118837" target="_blank" rel="noopener">0352 118 837</a>
        </div>
        <div class="info-row">
          <span class="label" data-i18n="con.web">Website</span>
          <a href="https://www.chefminhnguyen.com">chefminhnguyen.com</a>
        </div>
        <p class="small" style="margin-top:30px" data-i18n="con.hours">Chef và cộng sự phản hồi trong 24–48 giờ làm việc. Nếu gấp, gọi hoặc nhắn Zalo sẽ nhanh hơn.</p>
      </div>

      <div class="contact-grid__right">
        <form class="form is-open" id="form" novalidate>
          <div class="field">
            <label for="f-need" data-i18n="f.need">Bạn cần gì?</label>
            <select id="f-need" name="need">
              <option value="" data-i18n="f.need0">— Chọn nội dung —</option>
              <option value="hoc" data-i18n="con.r1">Tôi muốn học</option>
              <option value="brand" data-i18n="con.r2">Tôi đại diện một thương hiệu</option>
              <option value="nhahang" data-i18n="con.r3">Tôi có nhà hàng</option>
              <option value="trainghiem" data-i18n="con.r4">Tôi muốn đặt trải nghiệm</option>
            </select>
            <div class="chips" role="group" aria-label="Chọn nhanh">
              <button class="chip" type="button" data-route="hoc" aria-pressed="false" data-i18n="con.r1">Tôi muốn học</button>
              <button class="chip" type="button" data-route="brand" aria-pressed="false" data-i18n="con.r2">Tôi đại diện một thương hiệu</button>
              <button class="chip" type="button" data-route="nhahang" aria-pressed="false" data-i18n="con.r3">Tôi có nhà hàng</button>
              <button class="chip" type="button" data-route="trainghiem" aria-pressed="false" data-i18n="con.r4">Tôi muốn đặt trải nghiệm</button>
            </div>
          </div>

          <div class="form__row">
            <div class="field">
              <label for="f-name" data-i18n="f.name">Họ và tên</label>
              <input id="f-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-phone" data-i18n="f.phone">Số điện thoại</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>

          <div class="form__row">
            <div class="field">
              <label for="f-email" data-i18n="f.email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="f-zalo" data-i18n="f.zalo">Zalo (nếu có)</label>
              <input id="f-zalo" name="zalo" type="tel">
            </div>
          </div>

          <div class="form__row branch" data-branch="hoc" hidden>
            <div class="field">
              <label for="f-course" data-i18n="f.course">Khóa quan tâm</label>
              <input id="f-course" name="course" type="text">
            </div>
            <div class="field">
              <label for="f-level" data-i18n="f.level">Trình độ hiện tại</label>
              <select id="f-level" name="level">
                <option data-i18n="f.lv1">Chưa có kinh nghiệm</option>
                <option data-i18n="f.lv2">Đang làm bếp</option>
                <option data-i18n="f.lv3">Đã làm nhiều năm</option>
              </select>
            </div>
          </div>

          <div class="form__row branch" data-branch="brand" hidden>
            <div class="field">
              <label for="f-brand" data-i18n="f.brand">Tên thương hiệu</label>
              <input id="f-brand" name="brand" type="text">
            </div>
            <div class="field">
              <label for="f-camp" data-i18n="f.camp">Hình thức hợp tác</label>
              <select id="f-camp" name="campaign">
                <option data-i18n="f.cp1">Chiến dịch truyền thông</option>
                <option data-i18n="f.cp2">Nội dung ẩm thực</option>
                <option data-i18n="f.cp3">Sự kiện</option>
                <option data-i18n="f.cp4">Đại sứ dài hạn</option>
              </select>
            </div>
          </div>

          <div class="form__row branch" data-branch="nhahang" hidden>
            <div class="field">
              <label for="f-type" data-i18n="f.type">Loại hình</label>
              <input id="f-type" name="venue" type="text">
            </div>
            <div class="field">
              <label for="f-stage" data-i18n="f.stage">Giai đoạn</label>
              <select id="f-stage" name="stage">
                <option data-i18n="f.st1">Chuẩn bị mở mới</option>
                <option data-i18n="f.st2">Đang vận hành, cần cải tổ</option>
                <option data-i18n="f.st3">Mở rộng thêm chi nhánh</option>
              </select>
            </div>
          </div>

          <div class="form__row branch" data-branch="trainghiem" hidden>
            <div class="field">
              <label for="f-guests" data-i18n="f.guests">Số khách</label>
              <input id="f-guests" name="guests" type="number" min="1">
            </div>
            <div class="field">
              <label for="f-date" data-i18n="f.date">Ngày mong muốn</label>
              <input id="f-date" name="date" type="date">
            </div>
          </div>

          <div class="field">
            <label for="f-msg" data-i18n="f.msg">Nội dung</label>
            <textarea id="f-msg" name="message"></textarea>
          </div>

          <button type="submit" class="btn btn--solid" data-i18n="f.send">Gửi thông tin</button>
          <p class="form__note" id="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </div>
</section>
'''


# ============================================================
# CÁC TRANG CON
# ============================================================
def build_cuisine():
    return head('Ẩm thực — Chef Minh Nguyễn', 'Năm món signature của Chef Minh Nguyễn, mỗi món kèm câu chuyện do chính Chef viết.') \
        + header('cuisine.html') \
        + pagehead('<a href="index.html">Trang chủ</a> / <span data-i18n="nav.cuisine">Ẩm thực</span>',
                   ('Ẩm thực','Cuisine'),
                   ('Món ăn là bằng chứng,<br>không phải thực đơn.','The dishes are evidence,<br>not a menu.'),
                   ('Bốn món, bốn vùng đất. Chạm vào từng món để đọc câu chuyện Chef Minh viết cho nó.',
                    'Four dishes, four places. Tap any of them to read the story Chef Minh wrote for it.'), 'pgcui') + '''
<main>
<section class="band band--shell" data-nav="light">
  <div class="wrap">
''' + dish_grid() + '''
    <div style="margin-top:56px" class="reveal">
      <a href="index.html?need=nhahang#contact" class="link-arrow" data-i="arrow" data-i-pos="end">Trao đổi về thực đơn của bạn </a>
    </div>
  </div>
</section>
</main>
''' + MODAL + biomodal() + footer()


def build_the_chef():
    return head('Chef Minh Nguyễn — Hành trình nghề bếp', 'Tiểu sử, các mốc nghề nghiệp và thành tích của Chef Minh Nguyễn từ 2008 tới nay.') \
        + header('the-chef.html') \
        + pagehead('<a href="index.html">Trang chủ</a> / <span data-i18n="nav.chef">Chef</span>',
                   ('Hành trình','The path'),
                   ('Nghề bếp học bằng thời gian,<br>không học bằng lối tắt.',
                    'This trade is learned in years,<br>not in shortcuts.'), '', 'pgchef') + '''
<main>

<section class="band band--dark">
  <div class="wrap">
    <div class="craft reveal">
      <div>
        <div class="craft__num" id="counter">15</div>
        <div class="craft__numlab" data-i18n="craft.label">Năm theo nghề</div>
      </div>
      <div>
        <p class="lead" data-i18n="chef.intro">Bắt đầu từ căn bếp nhà hàng của gia đình ở Nhà Bè năm mười bốn tuổi, đi qua Thái Lan, Đan Mạch, Đức và Hungary, rồi quay về Đồng Văn để tìm lại nguyên liệu Việt. Dưới đây là các mốc có thật, theo đúng thứ tự chúng đã xảy ra.</p>
        <div class="stats">
          <div class="stat"><b>Top 4</b><span data-i18n="craft.s1s">Top Chef Việt Nam 2023 · VTV3</span></div>
          <div class="stat"><b>Master Chef</b><span data-i18n="craft.s2s">World’s Master Chef 2024 · Singapore</span></div>
          <div class="stat"><b>HCV · HCĐ</b><span data-i18n="craft.s3s">Đầu bếp Việt Nam Tài năng 2022 &amp; 2015</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band band--shell" data-nav="light" id="timeline">
  <div class="wrap">
    <p class="eyebrow" data-i18n="chef.tl">Các mốc</p>
    <h2 class="h-2" style="margin-bottom:44px" data-i18n="chef.tlh">Từng chặng một.</h2>
    <div class="reveal">
''' + bio_timeline(light=True) + '''
    </div>

    <p class="eyebrow" style="margin-top:64px" data-i18n="bio.roles">Vai trò hiện tại</p>
    <div class="reveal">
''' + bio_roles() + '''
    </div>
  </div>
</section>

<section class="band band--dark" id="philosophy" style="text-align:center">
  <div class="wrap">
    <div class="stalk-rule reveal" style="margin-bottom:52px">
      <svg viewBox="60 0 80 44" aria-hidden="true"><use href="#stalk"/></svg>
    </div>
    <blockquote class="reveal" style="margin:0 auto;max-width:19ch">
      <p style="font-family:var(--display);font-weight:400;font-size:clamp(1.9rem,4.4vw,3.5rem);line-height:1.24;margin:0;color:var(--shell)" data-i18n="phil.quote">“Ẩm thực Việt không chỉ là món ăn, mà là câu chuyện về văn hóa, con người và vùng đất.”</p>
      <p style="font-size:1rem;line-height:1.8;color:var(--cream-soft);max-width:52ch;margin:34px auto 0" data-i18n="phil.quote2">“Tôi muốn giữ được cái hồn Việt trong từng nguyên liệu, đồng thời dùng kỹ thuật và tư duy hiện đại để đưa những giá trị ấy đối thoại với thế giới.”</p>
      <footer style="margin-top:36px"><span class="label" data-i18n="phil.attr">Chef Minh Nguyễn</span></footer>
    </blockquote>
    <div class="stalk-rule reveal" style="margin-top:56px">
      <svg viewBox="60 0 80 44" aria-hidden="true"><use href="#stalk"/></svg>
    </div>
    <div style="margin-top:52px"><a href="cuisine.html" class="link-arrow" data-i="arrow" data-i-pos="end"><span data-i18n="cui.cta2">Xem trang ẩm thực</span> </a></div>
  </div>
</section>

</main>
''' + footer()


def build_services():
    blocks = [
        ('consulting', ('Tư vấn','Consulting'),
         ('Dựng bếp, dựng thực đơn, dựng cách vận hành.',
          'Building the kitchen, the menu and the way it runs.'),
         [('Phát triển thực đơn','Menu development'),
          ('Setup bếp và nhà hàng','Kitchen and restaurant setup'),
          ('Vận hành và huấn luyện đội bếp','Operations and team training'),
          ('Chuẩn hoá công thức và định lượng','Standardised recipes and portioning'),
          ('Kiểm soát chi phí nguyên liệu','Ingredient cost control'),
          ('Giải pháp khắc phục để tối ưu vận hành nhà bếp','Fixes to optimise kitchen operations')],
         'nhahang', ('Trao đổi về nhà hàng của bạn','Talk about your restaurant')),
        ('experiences', ('Trải nghiệm','Experiences'),
         ('Cá nhân hoá bữa tiệc của bạn bằng cách cộng tác với Chef Minh Nguyễn trong những dịch vụ dưới đây.',
          'Personalise your event by working with Chef Minh Nguyễn through the services below.'),
         [('Private Chef tại nhà','Private Chef at home'),
          ('Private Dining','Private Dining'),
          ('Sự kiện riêng và tiệc VIP','Private events and VIP dinners')],
         'trainghiem', ('Đặt trải nghiệm','Book an experience')),
        ('brand', ('Thương hiệu','Brand'),
         ('Đồng hành cùng các nhãn hàng bằng chuyên môn lâu năm và cả hình ảnh thực tế.',
          'Working with brands through long experience and real presence.'),
         [('Hợp tác quảng bá cùng nhãn hàng','Brand promotion partnerships'),
          ('KOL ngành ẩm thực','Food-industry KOL'),
          ('Sản xuất video, hình ảnh quảng bá sản phẩm','Product video and photo production'),
          ('Biểu diễn ẩm thực quảng bá','Live culinary demonstrations')],
         'brand', ('Nhận hồ sơ năng lực','Request the profile')),
    ]
    body = ''
    for i, (bid, title, desc, items, need, cta) in enumerate(blocks):
        shell = ' band--shell" data-nav="light' if i % 2 == 1 else ' band--dark'
        lis = '\n'.join(
            '          <li style="padding:12px 0 12px 22px;position:relative;border-bottom:1px solid rgba(198,166,100,.14)">'
            + CHECK + '<span data-i18n="sv.%s%d">%s</span></li>' % (bid, n, R('sv.%s%d' % (bid, n), x[0], x[1]))
            for n, x in enumerate(items, 1))
        ti = R('sv.%s.t' % bid, title[0], title[1])
        de = R('sv.%s.d' % bid, desc[0], desc[1])
        ct = R('sv.%s.c' % bid, cta[0], cta[1])
        body += f'''
<section class="band{shell}" id="{bid}">
  <div class="wrap">
    <div class="reveal" style="max-width:660px">
      <p class="eyebrow" data-i18n="sv.{bid}.t">{ti}</p>
      <h2 class="h-2" data-i18n="sv.{bid}.d">{de}</h2>
      <ul style="list-style:none;padding:0;margin:28px 0 34px;max-width:580px">
{lis}
      </ul>
      <a href="index.html?need={need}#contact" class="btn btn--solid" data-i="chat"><span data-i18n="sv.{bid}.c">{ct}</span></a>
    </div>
  </div>
</section>
'''
    R('sv.aca.t', 'Đào tạo', 'Education')
    R('sv.aca.h', 'Trụ thứ tư có trang riêng.', 'The fourth pillar has its own page.')
    R('sv.aca.l', 'Ba khoá học, lịch khai giảng và cách đăng ký nằm ở trang Academy.',
      'Three courses, intake dates and how to register are on the Academy page.')
    return head('Dịch vụ — Chef Minh Nguyễn', 'Tư vấn nhà hàng, private dining và hợp tác thương hiệu cùng Chef Minh Nguyễn.') \
        + header('services.html') \
        + pagehead('<a href="index.html">Trang chủ</a> / <span data-i18n="nav.services">Dịch vụ</span>',
                   ('Dịch vụ','Services'),
                   ('Bốn cách để làm việc<br>cùng Chef Minh.','Four ways to work<br>with Chef Minh.'), '', 'pgsv') \
        + '<main>' + body + '''
<section class="band band--raised">
  <div class="wrap" style="text-align:center">
    <p class="eyebrow" style="justify-content:center" data-i18n="sv.aca.t">Đào tạo</p>
    <h2 class="h-2" style="margin-left:auto;margin-right:auto" data-i18n="sv.aca.h">Trụ thứ tư có trang riêng.</h2>
    <p class="lead" style="margin:0 auto 30px" data-i18n="sv.aca.l">Ba khoá học, lịch khai giảng và cách đăng ký nằm ở trang Academy.</p>
    <a href="academy.html" class="btn" data-i="book"><span data-i18n="nav.academy">Academy</span></a>
  </div>
</section>
</main>
''' + footer()


def build_academy():
    return head('Academy — Học cùng Chef Minh Nguyễn', 'Các khóa học bếp Âu cơ bản và nâng cao cùng Chef Minh Nguyễn tại TP. Hồ Chí Minh.') \
        + header('academy.html') \
        + pagehead('<a href="index.html">Trang chủ</a> / <span data-i18n="nav.academy">Academy</span>',
                   ('Academy','Academy'),
                   ('Học cùng Chef Minh.','Learn with Chef Minh.'),
                   ('Lớp giới hạn số người để mỗi học viên đều được đứng bếp thật.',
                    'Class sizes are capped so everyone actually cooks.'), 'pgaca') + '''
<main>
<section class="band band--shell" data-nav="light">
  <div class="wrap">
''' + course_cards(full=True) + '''
    <div class="reveal" style="margin-top:56px;max-width:640px">
      <h3 class="h-3">Cách đăng ký</h3>
      <p class="small">Bấm <b>Chi tiết</b> ở khoá bạn quan tâm. Form sẽ mở sẵn ở mục “Tôi muốn học”, chỉ cần điền tên và cách liên hệ. Chef hoặc cộng sự sẽ gọi lại để trao đổi lộ trình và học phí phù hợp với trình độ của bạn. Học một lần dùng suốt đời, hỗ trợ kèm 24/7 sau khi hoàn thành khoá học.</p>
    </div>
  </div>
</section>
</main>
''' + footer()


def build_press():
    R('tru.press', 'Báo chí', 'Press')
    R('tru.pressh', 'Bài viết về Chef Minh.', 'Articles about Chef Minh.')
    R('tru.vid', 'Video', 'Video')
    R('tru.vidh', 'Xem Chef Minh làm nghề.', 'Watch Chef Minh at work.')
    R('tru.img', 'Hình ảnh & sự kiện', 'Photos & events')
    R('tru.imgh', 'Những nơi đã đi qua.', 'Places along the way.')
    R('tru.aw', 'Thành tích', 'Achievements')
    return head('Truyền thông & thành tích — Chef Minh Nguyễn',
                'Bài báo, video và các giải thưởng của Chef Minh Nguyễn trên báo chí và truyền hình.') \
        + header('press.html') \
        + pagehead('<a href="index.html">Trang chủ</a> / <span data-i18n="nav.press">Truyền thông</span>',
                   ('Truyền thông &amp; thành tích','Press &amp; credentials'),
                   ('Nơi Chef Minh<br>đã xuất hiện.','Where Chef Minh<br>has appeared.'), '', 'pgpress') + '''
<main>

<!-- ---------- 1. BÁO CHÍ ---------- -->
<section class="band band--dark">
  <div class="wrap">
    <p class="eyebrow" data-i18n="tru.press">Báo chí</p>
    <h2 class="h-2" style="margin-bottom:38px" data-i18n="tru.pressh">Bài viết về Chef Minh.</h2>
''' + article_grid(feature=True) + '''
  </div>
</section>

<!-- ---------- 2. VIDEO ---------- -->
<section class="band band--raised">
  <div class="wrap">
    <p class="eyebrow" data-i18n="tru.vid">Video</p>
    <h2 class="h-2" style="margin-bottom:38px" data-i18n="tru.vidh">Xem Chef Minh làm nghề.</h2>
''' + video_grid(feature=True) + '''
  </div>
</section>

<!-- ---------- 3. HÌNH ẢNH & SỰ KIỆN ---------- -->
<section class="band band--shell" data-nav="light">
  <div class="wrap">
    <p class="eyebrow" data-i18n="tru.img">Hình ảnh &amp; sự kiện</p>
    <h2 class="h-2" style="margin-bottom:38px" data-i18n="tru.imgh">Những nơi đã đi qua.</h2>
''' + media_grid() + '''
  </div>
</section>

<!-- ---------- 4. THÀNH TÍCH + HỒ SƠ ---------- -->
<section class="band band--dark">
  <div class="wrap">
    <p class="eyebrow" data-i18n="tru.aw">Thành tích</p>
    <div class="awards reveal" style="border-top:0">
      <div class="award-row"><b>2023</b><span data-i18n="aw.1">Top 4 — Top Chef Việt Nam, VTV3</span><em data-i18n="aw.k1">Truyền hình</em></div>
      <div class="award-row"><b>2024</b><span data-i18n="aw.2">Master Chef — World’s Master Chef, International Business Alliances, Singapore</span><em data-i18n="aw.k2">Giải thưởng</em></div>
      <div class="award-row"><b>2024</b><span data-i18n="aw.3">Đầu bếp Bạc — Best Gastronomie, Pháp</span><em data-i18n="aw.k2">Giải thưởng</em></div>
      <div class="award-row"><b>2022</b><span data-i18n="aw.4">Huy chương vàng — Đầu bếp Việt Nam Tài năng, hạng mục U.S. Beef</span><em data-i18n="aw.k3">Huy chương</em></div>
      <div class="award-row"><b>2015</b><span data-i18n="aw.5">Huy chương bạc — Đầu bếp trẻ Việt Nam Tài năng</span><em data-i18n="aw.k3">Huy chương</em></div>
      <div class="award-row"><b>2015</b><span data-i18n="aw.6">Huy chương đồng — Đầu bếp Việt Nam Tài năng</span><em data-i18n="aw.k3">Huy chương</em></div>
    </div>

    <div class="kit reveal">
      <div>
        <h3 class="h-3" data-i18n="tru.kith">Dành cho nhãn hàng và đối tác</h3>
        <p class="small" data-i18n="tru.kits">Hồ sơ năng lực đầy đủ: kinh nghiệm, số liệu độ phủ, các chiến dịch đã thực hiện và hình thức hợp tác.</p>
      </div>
      <a href="index.html?need=brand#contact" class="btn btn--solid" data-i="mail"><span data-i18n="tru.kitcta">Nhận hồ sơ năng lực</span></a>
    </div>
  </div>
</section>

</main>
''' + footer()


def build_blog():
    return head('Kiến thức bếp — Chef Minh Nguyễn', 'Kỹ thuật bếp, nguyên liệu và cách nấu, giải thích bằng ngôn ngữ của người đứng bếp.') \
        + header('blog.html') \
        + pagehead('<a href="index.html">Trang chủ</a> / <span data-i18n="nav.blog">Blog</span>',
                   ('Kiến thức bếp','Kitchen knowledge'),
                   ('Kiến thức bếp,<br>viết cho người muốn hiểu.',
                    'Kitchen knowledge,<br>written for people who want to understand.'),
                   ('Kỹ thuật, nguyên liệu Việt và cách nấu — giải thích bằng ngôn ngữ của người đứng bếp.',
                    'Technique, Vietnamese ingredients and how to cook them — explained by someone at the stove.'), 'pgblg') + '''
<main>
<section class="band band--shell" data-nav="light">
  <div class="wrap">
''' + post_grid() + '''
  </div>
</section>
</main>
''' + footer()


# ============================================================
# BÀI VIẾT BLOG
# ============================================================
def article_page(slug, cat, title, sub, img, body_html, prev_next):
    return head(f'{title} — Chef Minh Nguyễn', sub, depth=1) \
        + header('blog.html', depth=1) \
        + f'''<section class="pagehead">
  <div class="wrap">
    <p class="crumb"><a href="../index.html">Trang chủ</a> / <a href="../blog.html">Kiến thức bếp</a></p>
    <p class="eyebrow">{cat}</p>
    <h1 class="h-display" style="font-size:clamp(2rem,4.4vw,3.2rem);max-width:20ch">{title}</h1>
    <p class="lead">{sub}</p>
    <p class="article__meta"><span>Chef Minh Nguyễn</span><span>Kiến thức bếp</span></p>
  </div>
</section>

<main>
<section class="band band--shell" data-nav="light">
  <div class="wrap">
    <img src="../assets/{img}" alt="" style="width:100%;aspect-ratio:21/9;object-fit:cover;margin-bottom:48px" loading="lazy">
    <div class="article">
      <p class="draft-note">[CẦN CHEF DUYỆT] Bài này do bên thiết kế soạn từ kiến thức bếp chuyên nghiệp phổ thông, dùng làm bản nháp. Chef cần đọc, sửa theo kinh nghiệm thực tế và duyệt trước khi đăng dưới tên mình. Xoá đoạn này sau khi duyệt.</p>
{body_html}
    </div>

    <div style="margin-top:64px;padding-top:34px;border-top:1px solid var(--shell-line);display:flex;gap:28px;flex-wrap:wrap;justify-content:space-between">
      <a href="../blog.html" class="link-arrow" data-i="arrow" data-i-pos="end">Tất cả bài viết </a>
      <a href="{prev_next[0]}" class="link-arrow" data-i="arrow" data-i-pos="end">{prev_next[1]} </a>
    </div>
  </div>
</section>
</main>
''' + footer(depth=1)


SOUS_VIDE = '''      <p>Trong bếp truyền thống, chúng ta điều khiển món ăn bằng thời gian: chiên năm phút, hầm hai tiếng. Nhiệt độ thì gần như không kiểm soát được — chảo có thể 180°C hoặc 240°C tuỳ hôm. Sous vide đảo ngược chuyện đó. Nó cố định nhiệt độ, và biến thời gian thành thứ ít quan trọng hơn.</p>

      <h2>Nguyên lý: mỗi loại protein hỏng ở một mốc nhiệt khác nhau</h2>
      <p>Thịt không "chín" ở một điểm duy nhất. Các nhóm protein biến tính lần lượt ở những mốc khác nhau, và chính thứ tự đó quyết định miếng thịt mềm hay khô.</p>
      <ul>
        <li><b>Khoảng 50°C</b> — myosin bắt đầu đông lại. Thịt chuyển từ trong sang đục, giữ nguyên độ mọng.</li>
        <li><b>Khoảng 60–65°C</b> — collagen bắt đầu tan thành gelatin. Đây là lý do phần thịt nhiều gân trở nên mềm khi nấu lâu ở mốc này.</li>
        <li><b>Trên 68°C</b> — actin biến tính và co mạnh, ép nước ra khỏi sợi cơ. Đây là điểm miếng thịt bắt đầu khô, và không có cách nào cứu lại.</li>
      </ul>
      <p>Nấu bằng chảo hay lò nghĩa là bề mặt vượt xa 68°C từ lâu trước khi lõi đạt tới nhiệt độ mong muốn. Kết quả là một lát cắt có gradient: viền ngoài xám và khô, lõi giữa mới đúng độ. Sous vide đặt toàn bộ miếng thịt vào một môi trường đúng bằng nhiệt độ đích, nên không phần nào vượt quá.</p>

      <h2>Vì sao phải hút chân không</h2>
      <p>Túi hút chân không không phải để "giữ hương vị" như nhiều người nói. Nó có hai việc kỹ thuật rõ ràng: đẩy hết không khí ra để nguyên liệu tiếp xúc trực tiếp với nước — không khí dẫn nhiệt kém hơn nước rất nhiều — và giữ cho túi chìm thay vì nổi lên.</p>

      <h2>Thời gian: quyết định bởi độ dày, không phải khối lượng</h2>
      <p>Một sai lầm phổ biến là tính thời gian theo cân nặng. Nhiệt truyền theo chiều dày, nên một miếng thịt 2kg dẹt sẽ chín nhanh hơn một khối 1kg dày. Quy tắc thực tế: thời gian để lõi đạt nhiệt tăng theo bình phương độ dày. Gấp đôi độ dày thì mất khoảng bốn lần thời gian.</p>
      <p>Sau khi lõi đã đạt nhiệt, thời gian thêm không làm thịt chín hơn — nó làm collagen tan thêm. Đó là lý do một số phần thịt dai được nấu 24 đến 48 giờ ở nhiệt độ thấp.</p>

      <h2>Bước không được bỏ: áp chảo sau</h2>
      <p>Sous vide không tạo được lớp vỏ. Phản ứng Maillard — thứ tạo màu nâu và hàng trăm hợp chất thơm — cần nhiệt độ trên 140°C và bề mặt khô. Vì vậy quy trình đầy đủ luôn là: nấu chậm để kiểm soát lõi, lau thật khô bề mặt, rồi áp chảo cực nhanh ở lửa lớn.</p>
      <p>Lau khô là bước hay bị bỏ qua và cũng là bước quyết định. Bề mặt còn ẩm thì toàn bộ năng lượng của chảo sẽ dùng để bốc hơi nước thay vì tạo vỏ, và trong lúc chờ, lõi thịt tiếp tục chín quá mức.</p>

      <h2>Rủi ro an toàn thực phẩm</h2>
      <p>Đây là phần nghiêm túc nhất và cũng hay bị xem nhẹ nhất. Khoảng 5°C đến 55°C là vùng vi khuẩn sinh sôi nhanh. Sous vide thường vận hành ngay sát mép trên của vùng đó.</p>
      <div class="callout">Diệt khuẩn là kết hợp giữa nhiệt độ <b>và</b> thời gian giữ. Ở 55°C cần rất lâu; ở 60°C nhanh hơn nhiều. Nấu ở nhiệt độ thấp mà rút ngắn thời gian là rủi ro thật, không phải lý thuyết.</div>
      <p>Ba nguyên tắc bắt buộc trong bếp chuyên nghiệp: dùng nguyên liệu tươi và bảo quản lạnh đúng cách; đạt đủ thời gian giữ nhiệt tương ứng với nhiệt độ đã chọn; và nếu không phục vụ ngay thì làm lạnh nhanh trong nước đá rồi trữ lạnh, không để nguội tự nhiên ở nhiệt độ phòng.</p>

      <h2>Khi nào không nên dùng sous vide</h2>
      <p>Kỹ thuật này không phải lúc nào cũng tốt hơn. Nó vô nghĩa với những món mà giá trị nằm ở lớp vỏ và độ tương phản kết cấu — đồ chiên giòn, đồ nướng than. Nó cũng không cứu được nguyên liệu kém: sous vide giữ nguyên bản chất nguyên liệu, nên nguyên liệu nhạt sẽ cho ra món nhạt, chỉ mềm hơn.</p>
      <p>Nơi nó thật sự đáng dùng là khi cần độ chính xác lặp lại: một nhà hàng phải cho ra hai trăm phần giống hệt nhau, hoặc một phần thịt đắt tiền mà không được phép nấu hỏng.</p>
'''

DRY_AGING = '''      <p>Nghe qua thì vô lý: cố tình để một nguyên liệu đắt tiền mất nước và mất khối lượng, chấp nhận phải cắt bỏ phần ngoài, để đổi lấy cái gì? Câu trả lời nằm ở ba quá trình xảy ra song song trong lúc đó.</p>

      <h2>Ba việc xảy ra cùng lúc</h2>
      <h3>1. Mất nước làm vị cô đặc lại</h3>
      <p>Đây là phần dễ hiểu nhất. Nước bay hơi khỏi bề mặt và dần rút ra từ bên trong. Cùng một lượng hợp chất tạo vị nhưng nằm trong ít nước hơn, nên mỗi miếng cắn đậm hơn. Với thịt bò, mức hao hụt có thể lên tới một phần ba khối lượng.</p>

      <h3>2. Enzyme tự phân giải cấu trúc</h3>
      <p>Đây mới là phần quan trọng. Các enzyme vốn có sẵn trong mô — nhóm calpain và cathepsin — tiếp tục hoạt động sau khi con vật chết. Chúng cắt các protein dài thành mảnh ngắn hơn, làm sợi cơ lỏng ra. Kết quả là thịt mềm hơn theo cách mà không kỹ thuật nấu nào tạo được.</p>
      <p>Cùng lúc đó, protein bị cắt thành các axit amin tự do, trong đó có glutamate — nguồn gốc trực tiếp của vị umami. Mỡ cũng bị phân giải một phần thành axit béo, tạo ra hương thơm sâu, hơi hạt, hơi phô mai.</p>

      <h3>3. Vi sinh vật bề mặt</h3>
      <p>Trong phòng ủ có kiểm soát, một lớp nấm mốc lành tính hình thành trên bề mặt. Lớp này vừa bảo vệ phần thịt bên trong khỏi vi sinh vật gây hỏng, vừa đóng góp vào hương. Phần vỏ ngoài này sẽ bị gọt bỏ trước khi chế biến.</p>

      <h2>Điều kiện: bốn thông số không được sai</h2>
      <ul>
        <li><b>Nhiệt độ</b> — khoảng 1–3°C. Cao hơn thì vi khuẩn gây hỏng thắng; thấp hơn thì enzyme gần như ngừng hoạt động.</li>
        <li><b>Độ ẩm</b> — khoảng 80–85%. Quá khô thì lớp vỏ cứng lại quá nhanh và chặn quá trình bên trong; quá ẩm thì mốc xấu phát triển.</li>
        <li><b>Luồng khí</b> — phải liên tục và nhẹ. Không khí tù đọng là điều kiện lý tưởng cho vi khuẩn kỵ khí.</li>
        <li><b>Thời gian</b> — 21 đến 28 ngày là khoảng phổ biến với thịt bò. Sau 45 ngày, hương phô mai và hạt trở nên rất mạnh, không phải khẩu vị của mọi người.</li>
      </ul>

      <h2>Với cá thì khác</h2>
      <p>Cá dry-age theo thang thời gian hoàn toàn khác — thường tính bằng ngày chứ không phải tuần, và ở độ ẩm thấp hơn. Mục tiêu cũng khác: chủ yếu là loại bớt nước để thịt săn chắc và da giòn được khi áp chảo, chứ không nhắm tới hương lên men mạnh.</p>
      <p>Cá cũng phải được xử lý sạch triệt để trước khi ủ — bỏ mang, bỏ nội tạng, lau khô hoàn toàn. Một sai sót nhỏ ở bước này sẽ hỏng cả mẻ.</p>

      <div class="callout">Ranh giới giữa dry-age và thịt hỏng nằm ở chỗ có kiểm soát hay không. Không có tủ chuyên dụng, không có nhiệt kế và ẩm kế, thì đó không phải kỹ thuật — đó là để thịt hỏng có chủ đích.</div>

      <h2>Cái giá phải trả</h2>
      <p>Hao hụt 20–35% khối lượng, cộng với phần vỏ phải gọt bỏ. Cần thiết bị riêng và không gian riêng. Cần thời gian, nghĩa là cần vốn nằm chờ. Với một nhà hàng, đây là quyết định tài chính trước khi là quyết định ẩm thực — phải tính được giá bán có gánh nổi phần hao hụt đó không.</p>
'''

NUOC_DUNG = '''      <p>Khách không bao giờ gọi một bát nước dùng. Nhưng nếu nước dùng nhạt, mọi món sốt trong bếp đều nhạt theo, và không có gia vị nào chữa được. Đây là phần hạ tầng của bếp — không ai thấy, nhưng mọi thứ đứng trên nó.</p>

      <h2>Nước dùng làm được gì mà nước lã không làm được</h2>
      <p>Ba thứ: gelatin, hợp chất thơm và vị umami nền.</p>
      <p>Gelatin đến từ collagen trong xương và mô liên kết. Đây là thứ tạo cảm giác đầy đặn, hơi dính môi, và là lý do một món sốt tốt bám được vào thìa. Không có gelatin, sốt chỉ là nước có màu, dù có cô đặc bao nhiêu đi nữa.</p>

      <h2>Xương: chọn loại nào</h2>
      <ul>
        <li><b>Xương khớp, chân, đuôi</b> — nhiều collagen nhất. Đây là nguồn gelatin chính.</li>
        <li><b>Xương ống</b> — cho tuỷ và vị béo, nhưng ít collagen hơn nhiều người tưởng.</li>
        <li><b>Xương có dính thịt</b> — cho vị, nhưng cũng cho nhiều bọt đục hơn.</li>
      </ul>
      <p>Tỷ lệ thực tế trong bếp: khoảng một phần xương với hai phần nước tính theo khối lượng. Ít nước hơn thì cô đặc nhưng dễ cháy đáy; nhiều nước hơn thì phải nấu lâu để cô lại, và càng lâu càng dễ đục.</p>

      <h2>Trắng hay nâu: một bước duy nhất tạo khác biệt</h2>
      <p>Nước dùng trắng thì xương vào nồi ngay. Nước dùng nâu thì xương được nướng trước ở nhiệt cao cho tới khi ngả nâu sâu. Phản ứng Maillard trên bề mặt xương tạo ra hàng trăm hợp chất thơm không tồn tại trong nước dùng trắng, và cũng cho màu.</p>
      <p>Rau củ nền — hành tây, cà rốt, cần tây — cũng nên được xử lý tương ứng: để sống cho nước dùng trắng, xào hoặc nướng ngả nâu cho nước dùng nâu.</p>

      <h2>Nguyên tắc quan trọng nhất: không được sôi bùng</h2>
      <p>Nồi nước dùng phải giữ ở trạng thái lăn tăn — bề mặt chỉ khẽ động, thỉnh thoảng nổi một bong bóng. Khoảng 85–95°C.</p>
      <p>Lý do rất cụ thể. Khi nước sôi mạnh, chuyển động cơ học đánh nhỏ các hạt mỡ và protein đông tụ, phân tán chúng thành nhũ tương lơ lửng. Nước dùng đục vĩnh viễn, và không lọc được nữa. Nước dùng đã đục thì chỉ còn cách làm trong bằng lòng trắng trứng — một quy trình tốn công và làm mất bớt hương.</p>
      <div class="callout">Vớt bọt liên tục trong nửa giờ đầu. Đó là lúc phần lớn protein đông tụ và tạp chất nổi lên. Bỏ qua bước này thì chúng sẽ tan trở lại vào nồi.</div>

      <h2>Thời gian: nhiều hơn không phải lúc nào cũng tốt hơn</h2>
      <ul>
        <li><b>Cá</b> — 20 đến 45 phút. Nấu lâu hơn sẽ ra vị đắng và tanh từ xương.</li>
        <li><b>Gà</b> — 3 đến 4 giờ.</li>
        <li><b>Bò, bê</b> — 6 đến 8 giờ, có nơi làm tới 12.</li>
      </ul>
      <p>Sau mốc tối ưu, collagen đã tan hết còn các hợp chất thơm bắt đầu phân huỷ. Nồi nước dùng nấu 24 giờ không đậm gấp đôi nồi 12 giờ — nó chỉ ngả sang vị xương và vị kim loại.</p>

      <h2>Sai lầm hay gặp</h2>
      <ul>
        <li><b>Cho muối từ đầu.</b> Nước dùng sẽ được cô đặc ở các bước sau. Muối không bay hơi, nên món sốt cuối cùng sẽ mặn không thể sửa. Nêm ở bước cuối, không bao giờ ở bước đầu.</li>
        <li><b>Đậy kín vung.</b> Hơi nước ngưng tụ rơi ngược xuống mang theo mùi hăng. Để hé vung.</li>
        <li><b>Khuấy.</b> Không có lý do gì để khuấy nồi nước dùng. Khuấy chỉ làm đục.</li>
        <li><b>Để nguội tự nhiên qua đêm.</b> Một nồi lớn mất rất nhiều giờ để đi qua vùng nhiệt độ nguy hiểm. Làm lạnh nhanh bằng nước đá rồi mới cho vào tủ.</li>
      </ul>

      <h2>Cách kiểm tra</h2>
      <p>Cho một ít nước dùng vào chén, để lạnh. Nước dùng tốt sẽ đông lại thành thạch mềm — đó là bằng chứng có đủ gelatin. Nếu vẫn lỏng như nước, mẻ đó thiếu collagen: lần sau tăng tỷ lệ xương khớp, hoặc giảm lượng nước.</p>
'''


def build_articles():
    os.makedirs('blog', exist_ok=True)
    arts = [
        ('sous-vide.html', 'Kỹ thuật bếp',
         'Sous vide: nấu bằng nhiệt độ, không nấu bằng thời gian',
         'Vì sao 63°C giữ được thứ mà 100°C phá mất, và khi nào kỹ thuật này thực sự đáng dùng.',
         'blog-sous-vide.jpg', SOUS_VIDE, ('dry-aging.html', 'Bài tiếp: Dry-age')),
        ('dry-aging.html', 'Nguyên liệu',
         'Dry-age: làm khô có kiểm soát để vị đậm hơn',
         'Nguyên lý đằng sau việc cố tình để nguyên liệu mất nước, và ranh giới giữa chín tới và hỏng.',
         'blog-dry-age.jpg', DRY_AGING, ('nuoc-dung.html', 'Bài tiếp: Nước dùng')),
        ('nuoc-dung.html', 'Cách nấu',
         'Nước dùng: phần không ai thấy nhưng quyết định cả món',
         'Xương, nhiệt độ, thời gian và lý do nồi nước dùng không bao giờ được sôi bùng.',
         'blog-nuoc-dung.jpg', NUOC_DUNG, ('sous-vide.html', 'Bài tiếp: Sous vide')),
    ]
    for slug, cat, title, sub, img, body, pn in arts:
        open('blog/' + slug, 'w', encoding='utf-8').write(
            article_page(slug, cat, title, sub, img, body, pn))
    return [a[0] for a in arts]


# ============================================================
# CHẠY
# ============================================================
if __name__ == '__main__':
    pages = {
        'index.html': build_index(),
        'the-chef.html': build_the_chef(),
        'cuisine.html': build_cuisine(),
        'services.html': build_services(),
        'academy.html': build_academy(),
        'press.html': build_press(),
        'blog.html': build_blog(),
    }
    for name, html in pages.items():
        open(name, 'w', encoding='utf-8').write(html)
        print('✓', name, len(html) // 1024, 'KB')
    for a in build_articles():
        print('✓ blog/' + a)

    import json
    with open('js/i18n-auto.js', 'w', encoding='utf-8') as fh:
        fh.write('/* Từ điển sinh tự động bởi build.py — đừng sửa tay */\n')
        fh.write('window.CMN_I18N = ' + json.dumps(I18N, ensure_ascii=False, indent=1) + ';\n')
    print('✓ js/i18n-auto.js —', len(I18N), 'mục')

    # ---- Gộp CSS: 3 lượt tải còn 1 ----
    css = ''
    for f in ['css/style.css', 'css/motion.css', 'css/sponsor.css']:
        css += '\n/* ===== %s ===== */\n' % f + open(f, encoding='utf-8').read()
    css = re.sub(r'/\*(?!\s*=====)[\s\S]*?\*/', '', css)      # bỏ chú thích, giữ nhãn phần
    css = re.sub(r'\n\s*\n+', '\n', css)
    css = re.sub(r'[ \t]+', ' ', css)
    open('css/site.css', 'w', encoding='utf-8').write(css)
    print('✓ css/site.css —', len(css) // 1024, 'KB')

    # ---- Gộp JS: 5 lượt tải còn 1 ----
    js = ''
    for f in ['js/icons.js', 'js/i18n-auto.js', 'js/main.js', 'js/motion.js', 'js/sponsor.js']:
        js += '\n/* ===== %s ===== */\n' % f + open(f, encoding='utf-8').read() + '\n'
    open('js/site.js', 'w', encoding='utf-8').write(js)
    print('✓ js/site.js —', len(js) // 1024, 'KB')


def build_404():
    return head('Không tìm thấy trang — Chef Minh Nguyễn', 'Trang bạn tìm không tồn tại.') \
        + header() + '''
<main>
<section class="band band--dark" style="min-height:64vh;display:flex;align-items:center;text-align:center">
  <div class="wrap">
    <p class="eyebrow" style="justify-content:center">404</p>
    <h1 class="h-display" style="font-size:clamp(2.4rem,6vw,4.4rem)">Món này<br>không có trong thực đơn.</h1>
    <p class="lead" style="margin:26px auto 38px">Đường dẫn bạn vừa mở không tồn tại hoặc đã đổi tên.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a href="index.html" class="btn btn--solid">Về trang chủ</a>
      <a href="cuisine.html" class="btn">Xem ẩm thực</a>
    </div>
  </div>
</section>
</main>
''' + footer()


open('404.html', 'w', encoding='utf-8').write(build_404())
print('✓ 404.html')

SITE = 'https://www.chefminhnguyen.com/'
urls = ['', 'the-chef.html', 'cuisine.html', 'services.html', 'academy.html',
        'press.html', 'blog.html', 'blog/sous-vide.html', 'blog/dry-aging.html', 'blog/nuoc-dung.html']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    pr = '1.0' if u == '' else ('0.8' if '/' not in u else '0.6')
    sm += '  <url><loc>%s%s</loc><priority>%s</priority></url>\n' % (SITE, u, pr)
sm += '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
open('robots.txt', 'w', encoding='utf-8').write(
    'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
open('CNAME', 'w', encoding='utf-8').write('chefminhnguyen.com\n')
open('.nojekyll', 'w', encoding='utf-8').write('')
print('✓ sitemap.xml, robots.txt, CNAME, .nojekyll')
