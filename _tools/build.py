# -*- coding: utf-8 -*-
"""
Build bài viết dự án Nhật Khang.
  python3 _tools/build.py
Đọc _src/du-an/*.json -> sinh du-an/<slug>.html, chèn thẻ dự án vào index.html
(giữa <!-- CARDS:START --> và <!-- CARDS:END -->), sinh sitemap.xml, robots.txt.
Chỉ dùng thư viện chuẩn Python.
"""
import json, glob, os, html, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = 'https://lenhatkhangvn-bit.github.io/nhatkhang-website'   # đổi khi gắn tên miền riêng
ASSET_V = '4'                                                          # tăng khi đổi CSS/JS
BRAND = 'Nhật Khang'
STATUS_RUN = {'Đang thi công'}
E = html.escape

ORG = {
  "@type": "HomeAndConstructionBusiness",
  "@id": SITE_URL + "/#org",
  "name": "Công ty TNHH Kiến trúc Xây dựng Nhật Khang",
  "alternateName": "Nhật Khang",
  "slogan": "Xây niềm tin – Dựng an khang",
  "url": SITE_URL + "/",
  "logo": SITE_URL + "/assets/img/logo-light.png",
  "image": SITE_URL + "/assets/img/real-b4.jpg",
  "telephone": ["+84903590352", "+84905135833"],
  "taxID": "0402354390",
  "address": {"@type": "PostalAddress", "streetAddress": "202 Lương Nhữ Hộc", "addressLocality": "Phường Cẩm Lệ",
              "addressRegion": "Đà Nẵng", "addressCountry": "VN"},
  "areaServed": {"@type": "City", "name": "Đà Nẵng"},
  "sameAs": ["https://www.facebook.com/noithatnhatkhang", "https://www.youtube.com/@nhatkhang.danang"]
}

TECH = ['Tô trát: kiểm tra độ phẳng ≤ 3 mm trên thước 2 m, góc vuông.',
        'Cán nền khu ướt: dốc 1–2% về phễu thu, đổ nước thử.',
        'Chống thấm WC: ngâm nước 24 giờ trước khi lát gạch.',
        'Cấp nước: thử áp 10 bar trong 30 phút; đo cách điện trước khi đóng trần.',
        'Ốp lát: bôi keo kín 100% mặt sau viên gạch, gõ kiểm tra bộp.',
        'Sơn: tường đủ khô (độ ẩm < 16%) mới sơn; bả 2 lớp, 1 lót, 2 phủ.']

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'


def load():
    arts = []
    for f in sorted(glob.glob(os.path.join(ROOT, '_src', 'du-an', '*.json'))):
        a = json.load(open(f, encoding='utf-8'))
        if a.get('draft'):
            continue
        t = sum(v for _, v in a['bars']) or 1
        a['bars'] = [(k, round(v / t * 100, 1)) for k, v in a['bars']]
        arts.append(a)
    arts.sort(key=lambda a: (a.get('order', 99), a.get('date', '')), reverse=False)
    return arts


def head(a, url, img):
    title = f"{a['seo_title']} | {BRAND}"
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": a['seo_title'], "description": a['desc'],
         "image": [img], "datePublished": a.get('date'), "dateModified": a.get('updated', a.get('date')),
         "inLanguage": "vi-VN", "author": {"@id": SITE_URL + "/#org"}, "publisher": ORG, "mainEntityOfPage": url,
         "keywords": a.get('keyword', '')},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Dự án", "item": SITE_URL + "/#du-an"},
            {"@type": "ListItem", "position": 3, "name": a['short'], "item": url}]},
    ]
    if a.get('faq'):
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a['faq']]})
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(a['desc'])}">
<meta name="keywords" content="{E(a.get('keyword', ''))}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(a['seo_title'])}"><meta property="og:description" content="{E(a['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css?v={ASSET_V}">
{lds}'''


NAV = '''<header id="hdr" class="solid fixed-solid">
  <div class="wrap nav">
    <a href="../index.html" class="logo" aria-label="Nhật Khang – trang chủ"><img src="../assets/img/logo-dark.png" alt="Logo Nhật Khang – Xây niềm tin, Dựng an khang" width="180" height="44"></a>
    <nav class="menu" id="menu">
      <a href="../index.html#dich-vu">Dịch vụ</a><a href="../index.html#du-an">Dự án</a><a href="../index.html#bang-gia">Bảng giá</a><a href="../index.html#quy-trinh">Quy trình</a><a href="../index.html#bao-gia">Báo giá</a>
      <a href="tel:0903590352" class="hot">0903 590 352</a>
    </nav>
    <button class="burger" id="burger" aria-label="Mở menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  </div>
</header>'''

FOOT = f'''<footer>
  <div class="wrap">
    <div class="fgrid">
      <div><img src="../assets/img/logo-dark.png" alt="Nhật Khang" loading="lazy"><p><b style="color:#ddd">CÔNG TY TNHH KIẾN TRÚC XÂY DỰNG NHẬT KHANG</b><br>MST: 0402354390<br>202 Lương Nhữ Hộc, Phường Cẩm Lệ, TP. Đà Nẵng</p></div>
      <div><h4>Liên hệ</h4><ul><li><a href="tel:0903590352">0903 590 352</a></li><li><a href="tel:0905135833">0905 135 833</a></li></ul></div>
      <div><h4>Kênh Nhật Khang</h4><ul><li><a href="https://www.facebook.com/noithatnhatkhang" target="_blank" rel="noopener">Fanpage: noithatnhatkhang</a></li><li><a href="https://www.youtube.com/@nhatkhang.danang" target="_blank" rel="noopener">YouTube: @nhatkhang.danang</a></li><li><a href="https://zalo.me/0903590352" target="_blank" rel="noopener">Zalo: 0903 590 352</a></li></ul></div>
    </div>
    <div class="legal"><span>© <span id="yr">2026</span> Nhật Khang. Xây niềm tin – Dựng an khang.</span><span>Hoàn thiện & Nội thất căn hộ · Đà Nẵng</span></div>
  </div>
</footer>
<div class="float"><a class="zalo" href="https://zalo.me/0903590352" target="_blank" rel="noopener" aria-label="Chat Zalo">Zalo</a><a class="call" href="tel:0903590352" aria-label="Gọi hotline">{PHONE_SVG}</a></div>
<div class="lb" id="lb"><button class="x" aria-label="Đóng">×</button><button class="pv" aria-label="Ảnh trước">‹</button><img alt=""><button class="nx" aria-label="Ảnh sau">›</button><div class="lbc"></div></div>
<script src="../assets/js/main.js?v={ASSET_V}"></script>'''


def page(a, arts):
    url = f"{SITE_URL}/du-an/{a['slug']}.html"
    img = f"{SITE_URL}/assets/img/{a.get('cover') or 'og.jpg'}"
    others = [x for x in arts if x['slug'] != a['slug']]
    lbl = a.get('img_label', 'Phối cảnh thiết kế')
    g = ''
    if a.get('imgs'):
        g = f'<h2>Hình ảnh {"thực tế" if lbl == "Ảnh thực tế" else "phương án"}</h2><div class="gallery">' + ''.join(
            f'<figure class="gi{" big" if i == 0 else ""}"><span class="lbl">{E(lbl)}</span><img src="../assets/img/{f}" alt="{E(c)} – {E(a["short"])}" loading="lazy"><figcaption class="cap"><b>{E(c)}</b></figcaption></figure>'
            for i, (f, c) in enumerate(a['imgs'])) + '</div>'
    cover = f'<div class="cover"><img src="../assets/img/{a["cover"]}" alt="{E(a["seo_title"])}" fetchpriority="high"></div>' if a.get('cover') else ''
    bars = ''.join(f'<div class="bar"><span>{E(k)}</span><span class="t"><i style="width:{v}%"></i></span><span class="p">{str(v).replace(".", ",")}%</span></div>' for k, v in a['bars'])
    items = ''.join(f'<li><b>{E(k)}:</b> {E(v)}</li>' for k, v in a['items'])
    facts = ''.join(f'<div><small>{E(k)}</small><b{" class=g" if "Suất" in k else ""}>{E(v)}</b></div>' for k, v in a['facts'])
    faq = ''
    if a.get('faq'):
        faq = '<h2>Câu hỏi thường gặp</h2><div class="faq">' + ''.join(
            f'<details{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(ans)}</p></details>' for i, (q, ans) in enumerate(a['faq'])) + '</div>'
    rel = ''.join(f'<li><a href="{o["slug"]}.html">{E(o["short"])} – {E(o["seo_title"])}</a></li>' for o in others[:4])
    d = a.get('date', '')
    dshow = datetime.date.fromisoformat(d).strftime('%d/%m/%Y') if d else ''
    return f'''<!DOCTYPE html>
<html lang="vi"><head>
{head(a, url, img)}</head><body>
{NAV}
<main>
<section class="art-hero"><div class="wrap">
  <nav class="crumb" aria-label="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="../index.html#du-an">Dự án</a> / {E(a["short"])}</nav>
  <span class="eyebrow">{E(a["status"])}{" · " + dshow if dshow else ""}</span>
  <h1 style="margin-top:12px">{E(a["title"])}</h1>
  <p class="hook">{E(a["hook"])}</p>
  <p class="lead">{E(a["lead"])}</p>
  <div class="facts">{facts}</div>
</div></section>
<section class="art"><div class="wrap art-grid">
  <article>
    {cover}
    <h2>Tổng quan</h2>{''.join(f"<p>{E(p)}</p>" for p in a["intro"])}
    <h2>Các hạng mục thi công chính</h2><ul class="hl-list">{items}</ul>
    <h2>Cơ cấu chi phí theo báo giá</h2>
    <p>Tỷ trọng từng nhóm hạng mục trên tổng giá trị báo giá (chưa VAT):</p>
    <div class="bars">{bars}</div>
    <div class="disc">{E(a["note"])}</div>
    {g}
    {faq}
    <div class="cta-in"><div><b>Căn hộ của anh/chị có diện tích tương tự?</b><span>Gửi diện tích và bản vẽ, Nhật Khang lập báo giá chi tiết từng hạng mục.</span></div><a class="btn btn-gold" href="../index.html#bao-gia">Nhận báo giá</a></div>
    <div class="disc">Số liệu trong bài được tổng hợp từ báo giá thực tế của Nhật Khang năm 2026, đã ẩn thông tin chủ nhà. Suất đầu tư mang tính tham khảo, chưa gồm VAT, và thay đổi theo vật liệu, hiện trạng và phạm vi từng căn. Xem thêm <a href="../index.html#bang-gia" style="color:#b88200;font-weight:600">bảng giá tham khảo</a>.</div>
  </article>
  <aside class="side">
    <div class="box dark"><h3>Muốn biết căn nhà mình hết bao nhiêu?</h3><p style="color:#bbb">Gửi diện tích và bản vẽ (nếu có), Nhật Khang lập báo giá chi tiết từng hạng mục.</p><a class="btn btn-gold" href="../index.html#bao-gia">Nhận báo giá</a></div>
    <div class="box"><h3>Tiêu chuẩn nghiệm thu áp dụng</h3><ul>{''.join(f"<li>{E(t)}</li>" for t in TECH)}</ul></div>
    <div class="box"><h3>Dự án khác</h3><ul>{rel}</ul></div>
  </aside>
</div></section>
</main>
{FOOT}
</body></html>'''


def card(a):
    th = (f'<div class="th" style="background-image:url(assets/img/{a["cover"]})" role="img" aria-label="{E(a["seo_title"])}">'
          if a.get('cover') else f'<div class="th noimg"><span>{E(a["short"])}</span>')
    st = 'run' if a['status'] in STATUS_RUN else ''
    fx = dict(a['facts'])
    meta = ''.join(f'<span>{E(fx[k])}</span>' for k in ('Diện tích', 'Phạm vi', 'Suất đầu tư tham khảo') if k in fx)
    return (f'<a class="pc reveal" href="du-an/{a["slug"]}.html">{th}<span class="st {st}">{E(a["status"])}</span></div>'
            f'<div class="bd"><div class="meta">{meta}</div><h3>{E(a["title"].split(" – ")[0])}</h3><p>{E(a["card"])}</p>'
            f'<span class="more">Xem hạng mục thi công →</span></div></a>\n')


def main():
    arts = load()
    os.makedirs(os.path.join(ROOT, 'du-an'), exist_ok=True)
    for a in arts:
        open(os.path.join(ROOT, 'du-an', a['slug'] + '.html'), 'w', encoding='utf-8').write(page(a, arts))
    idx = os.path.join(ROOT, 'index.html')
    s = open(idx, encoding='utf-8').read()
    cards = ''.join(card(a) for a in arts)
    s = re.sub(r'(<!-- CARDS:START -->).*?(<!-- CARDS:END -->)', lambda m: m.group(1) + '\n' + cards + m.group(2), s, flags=re.S)
    s = re.sub(r'(assets/(?:css/style\.css|js/main\.js))\?v=\w+', r'\1?v=' + ASSET_V, s)
    open(idx, 'w', encoding='utf-8').write(s)
    today = datetime.date.today().isoformat()
    urls = [(SITE_URL + '/', today, '1.0')] + [(f"{SITE_URL}/du-an/{a['slug']}.html", a.get('updated', a.get('date', today)), '0.8') for a in arts]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n' for u, d, p in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /_tools/\nSitemap: {SITE_URL}/sitemap.xml\n')
    print(f'Built {len(arts)} bài:', ', '.join(a['slug'] for a in arts))


if __name__ == '__main__':
    main()
