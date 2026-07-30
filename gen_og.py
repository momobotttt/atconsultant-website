#!/usr/bin/env python3
"""生成 og.png (1200x630) — 分享去 WhatsApp / IG / FB 時嘅預覽卡片。
跟網站 palette：炭黑 #1a1a1a × 金 #c9a227。CJK 一律用 STHeiti（PingFang 會出口字）。
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
INK, GOLD, WHITE, MUTED = "#1a1a1a", "#c9a227", "#ffffff", "#9aa4ae"

HEI_M = "/System/Library/Fonts/STHeiti Medium.ttc"
HEI_L = "/System/Library/Fonts/STHeiti Light.ttc"
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"


def f(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# 右上角金色光暈（同 hero ::after 呼應）— 畫完 blur 一次，避免出現色帶
glow = Image.new("RGB", (W, H), INK)
gd = ImageDraw.Draw(glow)
for r in range(340, 0, -2):
    a = 34 * (1 - r / 340) ** 1.6
    gd.ellipse([W - 150 - r, -170 - r, W - 150 + r, -170 + r],
               fill=(26 + int(a), 26 + int(a * 0.78), 26 + int(a * 0.16)))
glow = glow.filter(ImageFilter.GaussianBlur(28))
img = Image.blend(img, glow, 0.95)
d = ImageDraw.Draw(img)

# 左邊金色直條
d.rectangle([0, 0, 10, H], fill=GOLD)

x = 88

# Eyebrow
d.text((x, 96), "HONG KONG  ·  ACCOUNTING & CORPORATE SERVICES",
       font=f(DIDOT, 22), fill=GOLD)

# Wordmark
d.text((x, 146), "A", font=f(DIDOT, 76), fill=WHITE)
aw = d.textlength("A", font=f(DIDOT, 76))
d.text((x + aw + 6, 146), "&", font=f(DIDOT, 76), fill=GOLD)
amp = d.textlength("&", font=f(DIDOT, 76))
d.text((x + aw + amp + 12, 146), "T Consultant", font=f(DIDOT, 76), fill=WHITE)

# 主 headline（U+30FB「・」STHeiti 冇字render成方格，改用 U+00B7「·」）
d.text((x, 268), "開公司 · 會計 · 報稅", font=f(HEI_M, 62), fill=WHITE)
d.text((x, 348), "一個 WhatsApp 全程辦妥", font=f(HEI_M, 62), fill=GOLD)

# 分隔線
d.line([x, 446, x + 340, 446], fill="#3a3a3a", width=2)

# 賣點
d.text((x, 474), "明碼實價 HK$6,500 全包政府費用   ·   最快一星期完成",
       font=f(HEI_L, 30), fill=MUTED)

# 底部
d.text((x, 546), "atconsultant.com.hk", font=f(DIDOT, 30), fill=WHITE)
ig = "@atconsultanthk"
igw = d.textlength(ig, font=f(DIDOT, 30))
d.text((W - 88 - igw, 546), ig, font=f(DIDOT, 30), fill=GOLD)

img.save("/Users/chifoonfung/at_consultant/website/og.png", "PNG", optimize=True)
print("saved og.png", img.size)
