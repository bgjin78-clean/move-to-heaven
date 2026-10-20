# -*- coding: utf-8 -*-
"""남양주·의정부·구리 동 단위 상담 페이지 생성기.

전화번호나 도메인을 바꾼 뒤 이 파일을 다시 실행하면 html과 배너가 다시 만들어집니다.
  python build.py
"""

from __future__ import annotations

import html
import json
import os
import shutil
import zlib
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSET_DIR = Path(r"C:\Users\j\.cursor\projects\c-Users-j-Desktop-4-Move-to-Heaven\assets")
SRC = ROOT / "img" / "src"

BRAND = "무브투헤븐"
PHONE_DISPLAY = "010-4026-0892"
PHONE_TEL = "01040260892"
PHONE_INTL = "+82-10-4026-0892"
# 배포 주소. 비어 있으면 canonical과 절대경로 sitemap은 만들지 않습니다.
SITE_URL = "https://heaven.allbarunclean.com"

RAW = {
    "hero": "raw-hero.jpg",
    "promo": "raw-promo.jpg",
    "yupum": "raw-yupum.jpg",
    "godok": "raw-godok.jpg",
    "special": "raw-special.jpg",
    "trash": "raw-trash.jpg",
    "waste": "raw-waste.jpg",
}

SERVICES = [
    {
        "key": "yupum",
        "name": "유품정리",
        "pair": ("고독사청소", "특수청소"),
        "file": "svc-yupum.jpg",
        "caption": "유품 분류와 포장",
        "cat": "생활서비스 > 유품정리",
        "point": "보관할 물건과 처리할 물건을 먼저 나눕니다.",
        "detail": "유품은 임의로 버리지 않습니다. 서류, 사진, 귀금속처럼 남겨야 할 물건과 반출할 가재를 구분한 뒤 포장합니다. 기증과 폐기 범위는 작업 전에 정합니다.",
        "faq_q": "유품을 함부로 버리나요?",
        "faq_a": "버리지 않습니다. 보관, 기증, 폐기 범위를 먼저 정하고 그 기준으로만 포장하고 반출합니다.",
    },
    {
        "key": "godok",
        "name": "고독사청소",
        "pair": ("유품정리", "특수청소"),
        "file": "svc-godok.jpg",
        "caption": "공간 살균과 탈취",
        "cat": "생활서비스 > 특수청소",
        "point": "악취와 오염 범위를 확인한 뒤 살균과 탈취를 진행합니다.",
        "detail": "발견이 늦어진 공간은 오염이 바닥과 벽으로 번져 있는 경우가 많습니다. 관계 기관 절차가 필요한 현장은 출입 가능 여부를 먼저 확인합니다. 현장 사진은 상담 외에 공개하지 않습니다.",
        "faq_q": "발견 직후에도 바로 들어가나요?",
        "faq_a": "출입 가능 여부를 먼저 확인합니다. 현장 보존이 필요한 동안에는 일정을 미루고, 정리가 가능한 시점부터 살균과 탈취를 진행합니다.",
    },
    {
        "key": "special",
        "name": "특수청소",
        "pair": ("고독사청소", "쓰레기집청소"),
        "file": "svc-special.jpg",
        "caption": "보호구 착용 작업",
        "cat": "생활서비스 > 특수청소",
        "point": "일반 청소로 어려운 오염과 악취를 보호구와 장비로 처리합니다.",
        "detail": "욕실, 주방, 원룸처럼 오염이 한곳에 모인 현장과 집 전체로 퍼진 현장을 구분해 인원과 시간을 잡습니다.",
        "faq_q": "일반 입주청소와 무엇이 다른가요?",
        "faq_a": "입주청소는 생활 때 묻은 먼지가 대상입니다. 특수청소는 악취나 오염이 그 범위를 넘을 때 보호구를 쓰고 진행합니다.",
    },
    {
        "key": "trash",
        "name": "쓰레기집청소",
        "pair": ("폐기물처리", "특수청소"),
        "file": "svc-trash.jpg",
        "caption": "생활폐기물 반출",
        "cat": "생활서비스 > 쓰레기집청소",
        "point": "쌓인 가재와 생활폐기물을 나눠 비웁니다.",
        "detail": "보관할 물건은 따로 모으고, 버릴 물건은 봉투와 박스로 나눠 반출합니다. 주방, 화장실, 베란다까지 비운 뒤 바닥 상태를 확인합니다.",
        "faq_q": "사람이 사는 집도 가능한가요?",
        "faq_a": "가능합니다. 거주 중이면 방과 거실을 나눠 진행하고, 당일 사용할 공간부터 비웁니다.",
    },
    {
        "key": "waste",
        "name": "폐기물처리",
        "pair": ("쓰레기집청소", "특수청소"),
        "file": "svc-waste.jpg",
        "caption": "폐기물 분리 상차",
        "cat": "생활서비스 > 폐기물처리",
        "point": "가전, 가구, 생활폐기물을 성상별로 나눠 반출합니다.",
        "detail": "처리 방법은 품목에 따라 달라집니다. 냉장고, 세탁기, 소파, 매트리스처럼 부피가 큰 물건은 엘리베이터와 주차 위치를 미리 알려 주시면 인원을 맞춥니다. 무단 투기는 하지 않습니다.",
        "faq_q": "가전과 가구만 맡겨도 되나요?",
        "faq_a": "가능합니다. 품목과 수량을 알려 주시면 반출 가능 여부와 차량 크기를 안내합니다. 종류마다 처리 경로가 다릅니다.",
    },
]

LOCAL_LINES = [
    "엘리베이터 유무와 주차 위치를 알려 주시면 반출 인원을 맞춥니다.",
    "베란다와 다용도실에 쌓인 물품은 따로 범위를 나눕니다.",
    "원룸, 아파트, 다가구, 상가주택을 구분해서 작업 시간을 잡습니다.",
    "주말이나 저녁 작업이 필요하면 이동 동선을 먼저 확인합니다.",
]

CITIES = [
    {
        "name": "남양주",
        "label": "남양주시",
        "intro": "다산·별내 신도시부터 진접, 화도, 와부, 수동, 조안까지 남양주 읍면동을 상담합니다.",
        "areas": [
            {"name": "와부읍", "spot": "덕소역·팔당·월문리", "housing": "한강변 아파트와 주택", "alias": ["덕소"]},
            {"name": "진접읍", "spot": "진접역·광릉·내각리", "housing": "진접선 주변 아파트와 주택", "alias": ["진접"]},
            {"name": "화도읍", "spot": "마석역·천마산·녹촌리", "housing": "아파트와 전원주택", "alias": ["마석"]},
            {"name": "진건읍", "spot": "사릉역·용정리", "housing": "주택가와 창고가 섞인 생활권", "alias": ["사릉"]},
            {"name": "오남읍", "spot": "오남역·오남리", "housing": "대단지 아파트", "alias": ["오남"]},
            {"name": "퇴계원읍", "spot": "퇴계원역·퇴계원리", "housing": "읍내 아파트와 상가주택", "alias": ["퇴계원"]},
            {"name": "별내면", "spot": "청학리·광전로", "housing": "주택과 광릉 생활권", "alias": []},
            {"name": "수동면", "spot": "축령산·송천리", "housing": "전원주택과 펜션", "alias": []},
            {"name": "조안면", "spot": "운길산역·북한강", "housing": "한강변 주택", "alias": ["운길산"]},
            {"name": "호평동", "spot": "호평역 생활권", "housing": "평내호평 아파트 단지", "alias": []},
            {"name": "평내동", "spot": "평내호평역", "housing": "역세권 아파트와 상가", "alias": ["평내호평"]},
            {"name": "금곡동", "spot": "금곡역", "housing": "경춘선 아파트와 주택", "alias": []},
            {"name": "양정동", "spot": "양정역 인근", "housing": "저밀도 주택", "alias": []},
            {"name": "다산1동", "spot": "다산역·다산신도시", "housing": "신축 고층 아파트", "alias": ["다산동"]},
            {"name": "다산2동", "spot": "지금동·도농동 생활권", "housing": "다산신도시 남측 아파트", "alias": ["지금동", "도농동"]},
            {"name": "별내동", "spot": "별내역·별내신도시", "housing": "8호선 신축 아파트", "alias": ["별내"]},
        ],
    },
    {
        "name": "의정부",
        "label": "의정부시",
        "intro": "의정부역 구시가지부터 가능, 녹양, 호원, 장암, 신곡, 민락, 고산, 금오까지 의정부 행정동을 상담합니다.",
        "areas": [
            {"name": "의정부1동", "spot": "의정부역·시청·행복로", "housing": "역세권 상가와 아파트", "alias": ["의정부동"]},
            {"name": "의정부2동", "spot": "의정부역 북쪽 구시가지", "housing": "다가구와 근린상가", "alias": []},
            {"name": "호원1동", "spot": "회룡역 생활권", "housing": "호원동 아파트", "alias": ["호원동", "회룡"]},
            {"name": "호원2동", "spot": "망월사역 생활권", "housing": "호원동 주택과 아파트", "alias": ["망월사"]},
            {"name": "장암동", "spot": "장암역·수락산 자락", "housing": "장암 아파트", "alias": []},
            {"name": "신곡1동", "spot": "발곡·신곡 서측", "housing": "신곡 아파트 단지", "alias": ["신곡동", "발곡"]},
            {"name": "신곡2동", "spot": "신곡동 동측", "housing": "아파트와 상가", "alias": ["신곡동"]},
            {"name": "송산1동", "spot": "용현동 일대", "housing": "동부 아파트", "alias": ["용현동"]},
            {"name": "송산2동", "spot": "민락지구", "housing": "민락동 아파트", "alias": ["민락동"]},
            {"name": "송산3동", "spot": "민락2지구·낙양동", "housing": "신축 아파트", "alias": ["민락동", "낙양동"]},
            {"name": "고산동", "spot": "고산지구", "housing": "의정부 동남 아파트", "alias": []},
            {"name": "자금동", "spot": "금오동·자일동·탑석역", "housing": "금오 생활권 아파트", "alias": ["금오동", "자일동", "탑석"]},
            {"name": "가능동", "spot": "가능역·법원 인근", "housing": "다세대와 연립", "alias": []},
            {"name": "흥선동", "spot": "흥선로 구시가지", "housing": "주택과 근린생활시설", "alias": []},
            {"name": "녹양동", "spot": "녹양역·종합운동장", "housing": "북부 아파트와 주택", "alias": []},
        ],
    },
    {
        "name": "구리",
        "label": "구리시",
        "intro": "갈매, 동구, 인창, 교문, 수택까지 구리 8개 행정동을 상담합니다.",
        "areas": [
            {"name": "갈매동", "spot": "갈매역·갈매지구", "housing": "신축 아파트", "alias": []},
            {"name": "동구동", "spot": "구리전통시장·동구릉 생활권", "housing": "구시가지 주택과 상가", "alias": ["구리전통시장"]},
            {"name": "인창동", "spot": "구리시청·돌다리", "housing": "인창 구시가지", "alias": ["돌다리"]},
            {"name": "교문1동", "spot": "교문사거리·아천동", "housing": "외곽 주택과 아파트", "alias": ["아천동"]},
            {"name": "교문2동", "spot": "교문동 중심", "housing": "상가와 아파트", "alias": ["교문동"]},
            {"name": "수택1동", "spot": "구리역 인근", "housing": "역세권 주택가", "alias": ["수택동"]},
            {"name": "수택2동", "spot": "수택동 중심", "housing": "밀집 주택가", "alias": ["수택동"]},
            {"name": "수택3동", "spot": "토평동·한강 쪽", "housing": "아파트와 주택", "alias": ["토평동"]},
        ],
    },
]


def E(value: str) -> str:
    return html.escape(value, quote=True)


def stable_index(seed: str, count: int) -> int:
    return zlib.crc32(seed.encode("utf-8")) % count


def rel(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, from_file.parent).replace("\\", "/")


def page_path(city: dict, area: dict, service: dict) -> Path:
    a, b = service["pair"]
    fname = f"{area['name']}-{service['name']}-{a}-{b}-업체.html"
    return ROOT / "청소" / "경기" / city["name"] / area["name"] / fname


def city_path(city: dict) -> Path:
    return ROOT / "청소" / "경기" / city["name"] / "index.html"


def home_path() -> Path:
    return ROOT / "index.html"


def public_path(path: Path) -> str:
    return "/" + path.relative_to(ROOT).as_posix()


def abs_url(path: str) -> str:
    parts = [quote(part) for part in path.split("/")]
    return SITE_URL.rstrip("/") + "/".join(parts)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "malgunbd.ttf" if bold else "malgun.ttf"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - w) // 2)
    top = max(0, (nh - h) // 2)
    return im.crop((left, top, left + w, top + h))


def fade_left(im: Image.Image, strength: int = 214, reach: float = 0.72) -> Image.Image:
    base = im.convert("RGBA")
    w, h = base.size
    reach_px = max(1, int(w * reach))
    row = []
    for x in range(w):
        if x >= reach_px:
            row.append(0)
        else:
            t = 1 - (x / reach_px)
            row.append(int(strength * (t ** 1.2)))
    mask = Image.new("L", (w, 1))
    mask.putdata(row)
    mask = mask.resize((w, h))
    shade = Image.new("RGBA", (w, h), (12, 20, 34, 255))
    shade.putalpha(mask)
    return Image.alpha_composite(base, shade)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, face, fill) -> None:
    x, y = xy
    draw.text((x + 2, y + 3), text, font=face, fill=(0, 0, 0, 130))
    draw.text((x, y), text, font=face, fill=fill)


def prepare_sources() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for name in RAW.values():
        target = SRC / name
        origin = ASSET_DIR / name
        if origin.exists():
            shutil.copyfile(origin, target)
        elif not target.exists():
            raise SystemExit(f"원본 이미지가 없습니다: {origin}")


def compose_images() -> None:
    prepare_sources()
    out = ROOT / "img"
    out.mkdir(parents=True, exist_ok=True)

    hero = fade_left(cover(Image.open(SRC / RAW["hero"]), 1600, 900))
    draw = ImageDraw.Draw(hero)
    draw.rounded_rectangle((56, 78, 470, 138), radius=28, fill=(255, 255, 255, 230))
    draw.text((78, 90), "남양주 · 의정부 · 구리", font=font(30, True), fill=(20, 32, 51, 255))
    draw_text(draw, (60, 176), "유품정리", font(86, True), (255, 255, 255, 255))
    draw_text(draw, (60, 278), "고독사청소", font(86, True), (255, 255, 255, 255))
    draw_text(draw, (60, 392), "특수청소 · 쓰레기집청소", font(36, True), (255, 226, 150, 255))
    draw_text(draw, (60, 448), "폐기물처리까지 방문 상담", font(34, True), (255, 255, 255, 255))
    draw.rounded_rectangle((56, 560, 760, 820), radius=32, fill=(225, 6, 0, 245))
    draw.text((88, 586), "24시간 전화 상담", font=font(32, True), fill=(255, 255, 255, 255))
    draw.text((88, 640), PHONE_DISPLAY, font=font(68, True), fill=(255, 255, 255, 255))
    draw.text((88, 736), BRAND + "  ·  현장 사진은 공개하지 않습니다", font=font(26), fill=(255, 255, 255, 230))
    hero.convert("RGB").save(out / "hero.jpg", "JPEG", quality=86, optimize=True, progressive=True)

    promo = fade_left(cover(Image.open(SRC / RAW["promo"]), 1600, 900), strength=196, reach=0.66)
    draw = ImageDraw.Draw(promo)
    draw_text(draw, (64, 150), "쓰레기집청소", font(78, True), (255, 255, 255, 255))
    draw_text(draw, (64, 250), "폐기물 반출", font(78, True), (255, 255, 255, 255))
    draw_text(draw, (64, 370), "남양주 · 의정부 · 구리 출동", font(36, True), (255, 226, 150, 255))
    draw.rounded_rectangle((64, 470, 780, 760), radius=32, fill=(20, 32, 51, 230))
    draw.text((96, 506), "상담 후 방문 견적", font=font(32, True), fill=(255, 226, 150, 255))
    draw.text((96, 566), PHONE_DISPLAY, font=font(68, True), fill=(255, 255, 255, 255))
    draw.text((96, 670), "터치하면 전화가 연결됩니다", font=font(28), fill=(255, 255, 255, 230))
    promo.convert("RGB").save(out / "promo.jpg", "JPEG", quality=86, optimize=True, progressive=True)

    for service in SERVICES:
        image = cover(Image.open(SRC / RAW[service["key"]]), 960, 960)
        image.save(out / service["file"], "JPEG", quality=84, optimize=True, progressive=True)


def head(title: str, desc: str, css: str, icon: str, script: str, jsonld: dict, path: str) -> str:
    canon = ""
    og_url = ""
    if SITE_URL:
        full = abs_url(public_path(Path(path)) if False else path)
        canon = f'<link rel="canonical" href="{E(full)}">'
        og_url = f'<meta property="og:url" content="{E(full)}">'
    data = json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
{canon}
<meta property="og:locale" content="ko_KR">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{E(rel(ROOT / path.lstrip('/'), ROOT / 'img' / 'hero.jpg') if not path.startswith('CLEAN') else '')}">
{og_url}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{E(icon)}" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<link rel="stylesheet" href="{E(css)}">
<script type="application/ld+json">{data}</script>
</head>
<body>
"""


def fix_og(html_text: str, from_file: Path) -> str:
    og = rel(from_file, ROOT / "img" / "hero.jpg")
    return html_text.replace('content="OGIMG"', f'content="{og}"')


def doc_head(title: str, desc: str, from_file: Path, jsonld: dict, keywords: str) -> str:
    css = rel(from_file, ROOT / "css" / "site.css")
    icon = rel(from_file, ROOT / "favicon.svg")
    canon = ""
    og_url = ""
    if SITE_URL:
        full = abs_url(public_path(from_file))
        canon = f'<link rel="canonical" href="{E(full)}">'
        og_url = f'<meta property="og:url" content="{E(full)}">'
    data = json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c")
    og = rel(from_file, ROOT / "img" / "hero.jpg")
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="keywords" content="{E(keywords)}">
<meta name="robots" content="index, follow, max-image-preview:large">
{canon}
<meta property="og:locale" content="ko_KR">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{E(og)}">
{og_url}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{E(icon)}" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<link rel="stylesheet" href="{E(css)}">
<script type="application/ld+json">{data}</script>
</head>
<body>
<main class="post-shell">
"""


def call_block() -> str:
    return f"""
<a class="post-call" href="tel:{PHONE_TEL}" aria-label="전화 상담 {PHONE_DISPLAY}">
  <span>유품정리 / 고독사청소 / 특수청소 / 쓰레기집 / 폐기물</span>
  <strong>📞 {PHONE_DISPLAY}</strong>
  <small>터치하시면 바로 전화가 연결됩니다</small>
</a>
<div class="post-action-row">
  <a class="post-action blue" href="#estimate"><strong>📦</strong><span>유품정리/고독사 상담</span></a>
  <a class="post-action green" href="#estimate"><strong>🚛</strong><span>쓰레기집/폐기물 상담</span></a>
</div>
<section class="post-notice">
  <p><strong>긴급 정리와 견적</strong>은 전화로 연결해 주세요.</p>
  <p>사진을 보내 주실 수 있으면 범위를 더 정확히 안내합니다. 상담 외에는 사진을 공개하지 않습니다.</p>
</section>
"""


def form_block(from_file: Path, area_label: str, service_name: str) -> str:
    options = []
    for service in SERVICES:
        selected = " selected" if service["name"] == service_name else ""
        options.append(f'<option value="{E(service["name"])}"{selected}>{E(service["name"])}</option>')
    return f"""
<section id="estimate" class="form-card">
  <h2>방문 상담 메모</h2>
  <p class="hint">연락처와 현장 내용을 남기시면 상담으로 이어집니다.</p>
  <form id="estimate-form" data-tel="tel:{PHONE_TEL}" data-phone="{PHONE_DISPLAY}">
    <div class="fields">
      <label>지역<input name="area" required value="{E(area_label)}"></label>
      <label>연락처<input name="phone" required inputmode="tel" placeholder="010-0000-0000"></label>
      <label>서비스<select name="service">{''.join(options)}</select></label>
      <label>상황<textarea name="memo" placeholder="평수, 층수, 엘리베이터, 보관할 물건이 있는지"></textarea></label>
      <div class="agree-box">
        <p><strong>개인정보 수집 및 이용 동의</strong> (필수)</p>
        <ul>
          <li>수집 항목: 지역, 연락처, 요청 서비스, 상담 내용</li>
          <li>이용 목적: 상담 접수와 견적 안내</li>
          <li>보유 기간: 상담 목적 달성 후 지체 없이 파기</li>
        </ul>
        <p>동의를 거부하실 수 있습니다. 거부하시면 상담 신청을 진행할 수 없습니다.</p>
        <label class="agree"><input type="checkbox" name="agree" required><span>개인정보 수집 및 이용에 동의합니다.</span></label>
      </div>
      <button class="submit" type="submit">빠른 상담 신청하기</button>
    </div>
  </form>
  <div id="estimate-result" class="estimate-result" hidden></div>
</section>
"""


def footer(from_file: Path) -> str:
    script = rel(from_file, ROOT / "js" / "site.js")
    return f"""
<p class="site-footer">{E(BRAND)} · 남양주 · 의정부 · 구리 · 상담 {PHONE_DISPLAY}<br>견적은 현장 범위에 따라 달라집니다. 폐기물은 품목별로 나눠 반출하며 무단으로 버리지 않습니다.</p>
</main>
<div class="callbar"><a href="tel:{PHONE_TEL}">전화 상담 {PHONE_DISPLAY}</a></div>
<script src="{E(script)}"></script>
</body>
</html>
"""


def service_by_name(name: str) -> dict:
    for service in SERVICES:
        if service["name"] == name:
            return service
    raise KeyError(name)


def render_area(city: dict, area: dict, service: dict) -> str:
    path = page_path(city, area, service)
    a, b = service["pair"]
    title = f"{city['label']} {area['name']} {service['name']} {a} {b} 업체"
    desc = f"{city['label']} {area['name']} {service['name']} 상담. {a}, {b}까지 방문 전에 범위를 확인합니다. 현장 사진은 공개하지 않습니다. {PHONE_DISPLAY}"
    aliases = " ".join(area["alias"])
    keywords = ", ".join(
        [f"{city['label']} {area['name']} {service['name']}", a, b, "특수청소", "유품정리", PHONE_DISPLAY]
        + [f"{name} {service['name']}" for name in area["alias"]]
    )
    place = f"{city['label']} {area['name']}"
    local = LOCAL_LINES[stable_index(place + service["name"], len(LOCAL_LINES))]
    hero = rel(path, ROOT / "img" / "hero.jpg")
    promo = rel(path, ROOT / "img" / "promo.jpg")
    crumbs = [
        (home_path(), "홈"),
        (city_path(city), city["label"]),
        (path, area["name"]),
    ]
    crumb_html = "".join(f'<a href="{E(rel(path, target))}">{E(label)}</a>' for target, label in crumbs[:2])
    crumb_html += f'<span>{E(area["name"])}</span>'

    faqs = [
        (f"{place}도 {service['name']} 출장이 되나요?",
         f"{place}을 포함해 남양주, 의정부, 구리 전역을 상담합니다. 주소를 알려 주시면 방문 시간과 차량 진입을 안내합니다."),
        ("주말이나 공휴일에도 가능한가요?",
         "가능합니다. 아파트는 엘리베이터 사용 시간과 차량이 설 자리를 미리 맞춥니다."),
        ("견적은 어떻게 안내하나요?",
         "평수, 층수, 엘리베이터, 오염 범위, 반출량을 들은 뒤 안내합니다. 현장과 이야기가 다르면 작업을 시작하기 전에 다시 말씀드립니다."),
        (service["faq_q"], service["faq_a"]),
    ]
    faq_html = []
    for question, answer in faqs:
        faq_html.append(
            f'<button type="button" class="faq-button" data-faq aria-expanded="false">{E(question)}</button>'
            f'<div class="faq-panel" hidden><p>{E(answer)}</p></div>'
        )

    strip = []
    for item in SERVICES:
        target = page_path(city, area, item)
        img = rel(path, ROOT / "img" / item["file"])
        strip.append(
            f'<a class="pcitem" href="{E(rel(path, target))}">'
            f'<img class="pcimg" src="{E(img)}" alt="{E(place + " " + item["caption"])}" width="960" height="960" loading="lazy">'
            f'<div class="pcname">{E(item["caption"])}</div></a>'
        )

    others = [item for item in city["areas"] if item["name"] != area["name"]]
    start = stable_index(area["name"], len(others))
    neighbors = [others[(start + i) % len(others)] for i in range(6)]
    cards = []
    for index, near in enumerate(neighbors, start=1):
        target = page_path(city, near, service)
        query = quote(f"경기 {city['label']} {near['name']} {service['name']}")
        naver = f"https://map.naver.com/p/search/{query}"
        google = f"https://www.google.com/maps/search/?api=1&query={query}"
        cards.append(f"""
<article class="place-card">
  <div class="place-rank">{index}</div>
  <div class="place-main">
    <h3><a href="{E(rel(path, target))}">{E(near['name'])} {E(service['name'])} {E(a)} {E(b)}</a></h3>
    <p class="place-cat">{E(service['cat'])}</p>
    <p class="place-addr">경기 {E(city['label'])} {E(near['name'])}</p>
    <p class="place-kw">#{E(service['name'])} #{E(a)} #방문상담</p>
    <p class="place-desc">{E(near['name'])} 일대 {E(a)} 문의와 {E(service['name'])} 현장 범위를 이어서 확인할 수 있습니다. {E(near['spot'])}.</p>
  </div>
  <div class="place-links">
    <a href="{E(rel(path, target))}">{E(near['name'])} 페이지</a>
    <a href="{naver}" target="_blank" rel="noopener">네이버지도</a>
    <a href="{google}" target="_blank" rel="noopener">구글지도</a>
  </div>
</article>""")

    pager = []
    for item in SERVICES:
        if item["name"] == service["name"]:
            continue
        pager.append(f'<a class="pager-link" href="{E(rel(path, page_path(city, area, item)))}">{E(item["name"])}</a>')
    pager.append(f'<a class="pager-link pager-next" href="{E(rel(path, home_path()))}">상담 안내 홈</a>')

    thumbs = []
    resources = []
    for item in SERVICES:
        img = rel(path, ROOT / "img" / item["file"])
        alt = f"{place} {service['name']} {item['caption']}"
        thumbs.append(f'<img src="{E(img)}" alt="{E(alt)}" width="960" height="960" loading="lazy">')
    for item in SERVICES:
        if item["name"] == service["name"]:
            continue
        img = rel(path, ROOT / "img" / item["file"])
        resources.append(
            f'<a class="post-resource-link" href="{E(rel(path, page_path(city, area, item)))}">'
            f'<span class="post-resource-thumb"><img src="{E(img)}" alt="{E(place + " " + item["name"])}" width="960" height="960" loading="lazy"></span>'
            f'<strong class="post-resource-title">{E(place)} {E(item["name"])} 상담 안내</strong>'
            f'<em class="post-resource-arrow">›</em></a>'
        )
        if len(resources) == 4:
            break

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "홈"},
                    {"@type": "ListItem", "position": 2, "name": city["label"]},
                    {"@type": "ListItem", "position": 3, "name": f"{area['name']} {service['name']}"},
                ],
            },
            {
                "@type": "Service",
                "name": title,
                "serviceType": service["name"],
                "areaServed": {"@type": "AdministrativeArea", "name": place},
                "provider": {
                    "@type": "LocalBusiness",
                    "name": BRAND,
                    "telephone": PHONE_INTL,
                    "areaServed": ["남양주시", "의정부시", "구리시"],
                },
                "description": desc,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a_}}
                    for q, a_ in faqs
                ],
            },
        ],
    }
    alias_line = f" 검색에 함께 쓰이는 이름: {aliases}." if aliases else ""
    return doc_head(title, desc, path, graph, keywords) + f"""
<div class="post-badges">
  <a href="{E(rel(path, city_path(city)))}">📍 {E(place)}</a>
  <span>{E(service['name'])} 외</span>
</div>
<nav class="crumb" aria-label="경로">{crumb_html}</nav>
<header class="post-header">
  <h1>{E(title)}</h1>
  <p>{E(place)} 인근 {E(service['name'])} 상담과 방문 범위를 한 화면에서 확인할 수 있습니다.</p>
</header>
{call_block()}
<figure class="post-hero-media">
  <img src="{E(hero)}" alt="{E(place + ' ' + service['name'] + ' 24시간 상담')}" width="1600" height="900">
</figure>
{form_block(path, place, service['name'])}
<section class="post-summary">
  <div class="summary-card">
    <h2>{E(place)} {E(service['name'])} 안내</h2>
    <p>{E(place)}은 {E(area['spot'])} 일대입니다. {E(area['housing'])}에서 {E(service['name'])}가 필요하면 방문 전에 평수와 엘리베이터, 주차 위치를 확인합니다.</p>
    <p>{E(service['detail'])}</p>
    <p>{E(local)}{E(alias_line)}</p>
    <dl>
      <div><dt>대표 지역</dt><dd>{E(place)}</dd></div>
      <div><dt>대표 서비스</dt><dd>{E(service['name'])}</dd></div>
      <div><dt>분류</dt><dd>{E(service['cat'])}</dd></div>
    </dl>
  </div>
</section>
<section class="post-strip">
  <h2>{E(area['name'])} 작업 범위</h2>
  <div class="rowx">{''.join(strip)}</div>
</section>
<section class="post-places" aria-label="인근 지역">
  <div class="section-heading"><span>NEAR</span><h2>{E(area['name'])} 인근 {E(service['name'])} 지역</h2></div>
  <p class="lead">같은 {E(city['label'])} 안에서 이어서 볼 수 있는 읍면동 상담 페이지입니다. 지도 버튼은 해당 동 검색으로 연결됩니다.</p>
  {''.join(cards)}
  <div class="mini">
    <a href="#estimate">방문 상담 메모 작성</a>
    <a class="solid" href="tel:{PHONE_TEL}">24시간 전화 연결</a>
  </div>
</section>
<figure class="post-map-promo">
  <a href="tel:{PHONE_TEL}" aria-label="{E(area['name'])} 전화 상담">
    <img src="{E(promo)}" alt="{E(area['name'] + ' 쓰레기집청소 폐기물처리 상담')}" width="1600" height="900" loading="lazy">
  </a>
</figure>
<section class="faq-section">
  <div class="section-heading"><span>FAQ</span><h2>자주 확인하는 질문</h2></div>
  {''.join(faq_html)}
</section>
<nav class="pager" aria-label="다른 서비스">{''.join(pager)}</nav>
<section class="post-thumbs" aria-label="작업 이미지">{''.join(thumbs)}</section>
<section class="post-resource-links" aria-label="다른 상담">{''.join(resources)}</section>
""" + footer(path)


def render_city(city: dict) -> str:
    path = city_path(city)
    title = f"{city['label']} 유품정리 고독사청소 특수청소 쓰레기집청소 폐기물처리"
    desc = f"{city['label']} 읍면동별 유품정리, 고독사청소, 특수청소, 쓰레기집청소, 폐기물처리 상담. {PHONE_DISPLAY}"
    keywords = f"{city['label']}, 유품정리, 고독사청소, 특수청소, 쓰레기집청소, 폐기물처리"
    hero = rel(path, ROOT / "img" / "hero.jpg")
    blocks = []
    for area in city["areas"]:
        links = []
        for service in SERVICES:
            links.append(f'<a href="{E(rel(path, page_path(city, area, service)))}">{E(service["name"])}</a>')
        alias = f" · {', '.join(area['alias'])}" if area["alias"] else ""
        blocks.append(
            f'<section class="area-block"><h2>{E(area["name"])}</h2>'
            f'<p>{E(area["spot"])} · {E(area["housing"])}{E(alias)}</p>'
            f'<div class="kw-row">{"".join(links)}</div></section>'
        )
    graph = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": title,
        "areaServed": city["label"],
        "provider": {"@type": "LocalBusiness", "name": BRAND, "telephone": PHONE_INTL},
        "description": desc,
    }
    return doc_head(title, desc, path, graph, keywords) + f"""
<div class="post-badges"><a href="{E(rel(path, home_path()))}">홈</a><span>📍 {E(city['label'])}</span></div>
<header class="post-header">
  <h1>{E(title)}</h1>
  <p>{E(city['intro'])} 행정구역은 시청 공개 읍면동 기준입니다.</p>
</header>
{call_block()}
<figure class="post-hero-media"><img src="{E(hero)}" alt="{E(city['label'] + ' 유품정리 특수청소')}" width="1600" height="900"></figure>
{form_block(path, city['label'], '유품정리')}
<section class="summary-card" style="margin-top:16px">
  <h2>{E(city['label'])} 읍면동</h2>
  <p>동 이름을 고른 뒤 필요한 작업을 선택하면 해당 상담 페이지로 이동합니다.</p>
  {''.join(blocks)}
</section>
""" + footer(path)


def render_home() -> str:
    path = home_path()
    title = "남양주 의정부 구리 유품정리 고독사청소 특수청소 쓰레기집청소 폐기물처리"
    desc = f"남양주시, 의정부시, 구리시 읍면동 유품정리와 특수청소 상담. 현장 사진은 공개하지 않습니다. {PHONE_DISPLAY}"
    keywords = "남양주 유품정리, 의정부 고독사청소, 구리 특수청소, 쓰레기집청소, 폐기물처리"
    hero = rel(path, ROOT / "img" / "hero.jpg")
    cards = []
    for city in CITIES:
        cards.append(
            f'<a class="city-card" href="{E(rel(path, city_path(city)))}">'
            f'<strong>{E(city["label"])}</strong>'
            f'<span>{len(city["areas"])}개 읍면동 · {E(city["intro"])}</span></a>'
        )
    services = []
    for service in SERVICES:
        img = rel(path, ROOT / "img" / service["file"])
        services.append(
            f'<article class="info-band"><img src="{E(img)}" alt="{E(service["caption"])}" width="960" height="960" loading="lazy">'
            f'<strong>{E(service["name"])}</strong><span>{E(service["point"])} {E(service["detail"])}</span></article>'
        )
    graph = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": BRAND,
        "telephone": PHONE_INTL,
        "areaServed": ["남양주시", "의정부시", "구리시"],
        "description": desc,
    }
    return doc_head(title, desc, path, graph, keywords) + f"""
<div class="post-badges"><span>📍 남양주 · 의정부 · 구리</span><span>{E(BRAND)}</span></div>
<header class="post-header">
  <h1>남양주 · 의정부 · 구리<br>유품정리 · 고독사청소 · 특수청소</h1>
  <p>쓰레기집청소와 폐기물처리까지, 읍면동 페이지에서 방문 범위를 확인할 수 있습니다.</p>
</header>
{call_block()}
<figure class="post-hero-media"><img src="{E(hero)}" alt="유품정리와 특수청소 상담" width="1600" height="900"></figure>
{form_block(path, '남양주·의정부·구리', '유품정리')}
<section>
  <div class="section-heading"><span>AREA</span><h2>지역 선택</h2></div>
  <div class="city-grid">{''.join(cards)}</div>
</section>
<section>
  <div class="section-heading"><span>WORK</span><h2>작업 구분</h2></div>
  <div class="service-grid">{''.join(services)}</div>
</section>
<section class="summary-card" style="margin-top:16px">
  <h2>진행 순서</h2>
  <p>1. 전화로 주소와 상황을 확인합니다.</p>
  <p>2. 방문 시간, 인원, 차량 진입을 정합니다.</p>
  <p>3. 보관할 물건과 반출할 물건을 나눕니다.</p>
  <p>4. 정리 후 반출하고, 현장 사진은 공개하지 않습니다.</p>
</section>
""" + footer(path)


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    compose_images()
    count = 0
    urls = []
    write_page(home_path(), render_home())
    urls.append(public_path(home_path()))
    count += 1
    for city in CITIES:
        write_page(city_path(city), render_city(city))
        urls.append(public_path(city_path(city)))
        count += 1
        for area in city["areas"]:
            for service in SERVICES:
                path = page_path(city, area, service)
                write_page(path, render_area(city, area, service))
                urls.append(public_path(path))
                count += 1
    robots = "User-agent: *\nAllow: /\n"
    if SITE_URL:
        lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for url in urls:
            lines.append(f"  <url><loc>{abs_url(url)}</loc></url>")
        lines.append("</urlset>")
        (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
        robots += f"Sitemap: {SITE_URL.rstrip('/')}/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    areas = sum(len(city["areas"]) for city in CITIES)
    print(f"pages={count} areas={areas} services={len(SERVICES)}")
    print(page_path(CITIES[0], CITIES[0]["areas"][13], SERVICES[0]).relative_to(ROOT))


if __name__ == "__main__":
    main()
