"""Build SCRIPT-phan-1.md from the speaker notes (<aside class="notes">) in sections/*.html.

Run from anywhere: python3 tools/build_script.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Same order as SECTIONS in index.html.
ORDER = ['00-cover', '00-outline', '01-what-is-nosql', '02-why-nosql', '03-four-types', '04-distributed-basics', '05-takeaways']


def inline_md(fragment):
    fragment = re.sub(r'</?b>', '**', fragment)
    fragment = re.sub(r'</?i>', '_', fragment)
    fragment = re.sub(r'</?code>', '`', fragment)
    return html.unescape(re.sub('<.*?>', '', fragment)).strip()


def main():
    lines = []
    n = 0
    minutes = 0.0
    for sec in ORDER:
        src = (ROOT / 'sections' / f'{sec}.html').read_text()
        for m in re.finditer(r'(<section class="slide[^"]*"[^>]*>)(.*?)</section>', src, re.S):
            n += 1
            head, body = m.group(1), m.group(2)
            eyebrow = re.search(r'class="eyebrow">.*?</svg>(.*?)</div>', body, re.S)
            h2 = re.search(r'<h2>(.*?)</h2>', body, re.S)
            if 'divider' in head:
                num = re.search(r'divider-num">(\d+)', body).group(1)
                title = f'Phần {num} — {inline_md(h2.group(1))}'
            else:
                title = inline_md((eyebrow or h2).group(1))
            lines += [f'## Slide {n} · {title}', '']
            notes = re.search(r'<aside class="notes">(.*?)</aside>', body, re.S)
            if not notes:
                continue
            text = notes.group(1)
            minutes += sum(float(x.replace(',', '.')) for x in re.findall(r'~([\d,]+) phút', text))
            minutes += sum(int(x) / 60 for x in re.findall(r'~(\d+) giây', text))
            for p in re.findall(r'<p>(.*?)</p>', text, re.S):
                lines += [inline_md(p), '']

    header = [
        '# Script thuyết trình — NoSQL Phần 1', '',
        '> Sinh tự động từ speaker notes trong `sections/*.html` (`<aside class="notes">`). '
        'Sửa script ở file section rồi chạy lại `python3 tools/build_script.py`.',
        '> Khi trình chiếu: nhấn **N** để hiện script ngay trên slide, **→ / Space** để qua bước tiếp theo, '
        '**O** xem tổng quan, **T** đổi theme, **F** toàn màn hình.',
        '> `[→]` trong script = nhấn phím mũi tên để hiện ý tiếp theo trên cùng slide.', '',
        f'**Tổng thời lượng ước tính:** khoảng {round(minutes)} phút (chưa tính hỏi đáp), {n} slide.', '',
    ]
    (ROOT / 'SCRIPT-phan-1.md').write_text('\n'.join(header + lines))
    print(f'{n} slides, ~{round(minutes)} min')


if __name__ == '__main__':
    main()
