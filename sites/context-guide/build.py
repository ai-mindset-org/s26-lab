#!/usr/bin/env python3
"""Сборка одностраничного гайда из guide/*.md в shaper-грамматике.

Вход:  guide/01-start.md … guide/10-failures.md + guide/README.md (интро и карта)
Выход: sites/context-guide/index.html + sites/context-guide/assets/*.png

Запуск: python3 sites/context-guide/build.py
"""
import pathlib, re, shutil
import markdown

ROOT = pathlib.Path(__file__).resolve().parents[2]
GUIDE = ROOT / "guide"
OUT = ROOT / "sites" / "context-guide"
OUT_ASSETS = OUT / "assets"

SECTIONS = [
    ("01", "start", "минимальный старт", "сразу, первые 15 минут"),
    ("02", "sources", "карта источников", "когда первый источник собран"),
    ("03", "layers", "хранение слоями", "когда файлов стало больше десятка"),
    ("04", "vault", "волт: типы, имена, поиск", "когда перестал находить своё"),
    ("05", "rakes", "грабли", "прочитать заранее, вернуться при боли"),
    ("06", "security", "безопасность контекста", "до первой отправки во внешний сервис"),
    ("07", "examples", "примеры", "когда непонятно, как это выглядит у людей"),
    ("08", "generations", "поколения метода", "когда нашёл материалы прошлых потоков"),
    ("09", "gates", "механика срабатывания", "когда правила записаны и продолжают нарушаться"),
    ("10", "failures", "что не сработало", "до того, как начнёшь наводить порядок"),
]

FILES = {
    "01": "01-start.md", "02": "02-sources.md", "03": "03-layers.md", "04": "04-vault.md",
    "05": "05-rakes.md", "06": "06-security.md", "07": "07-examples.md",
    "08": "08-generations.md", "09": "09-gates.md", "10": "10-failures.md",
}

CSS = """
:root{
  --bg:#ffffff; --ink:#000000;
  --soft:#d9d9d9; --hair:#ececec; --muted:#8a8a8a; --flow:#e9b400;
  --mono:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --frame:1px; --gutter:22px; --wrap:1120px;
}
*{ box-sizing:border-box; }
html{ scroll-behavior:smooth; }
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--mono); font-size:15.5px; line-height:1.62;
  -webkit-font-smoothing:antialiased;
}
/* строчные — только в служебных подписях: в теле текста lowercase съел бы имена авторов */
.wrap{ max-width:var(--wrap); margin:0 auto; padding:34px 26px 60px; }

/* ── шапка ─────────────────────────────────────────── */
.shaper-header{
  display:grid; grid-template-columns:auto 1fr auto; gap:28px; align-items:baseline;
  border-bottom:var(--frame) solid var(--ink); padding-bottom:15px; letter-spacing:.04em;
}
.shaper-header .brand{ font-weight:600; letter-spacing:.18em; font-size:21px; }
.shaper-header .crumb{ color:var(--muted); font-size:14px; }
.shaper-header .meta{ color:var(--muted); font-size:12px; justify-self:end; text-align:right; }
.shaper-header .meta b{ color:var(--ink); font-weight:500; letter-spacing:.08em; }

/* ── навигация чипами, липкая ───────────────────────── */
.nav{
  position:sticky; top:0; z-index:20; background:var(--bg);
  border-bottom:var(--frame) solid var(--soft);
  padding:10px 0 9px; margin-bottom:26px;
  display:flex; flex-wrap:wrap; gap:6px; align-items:center;
}
.nav .lbl{ font-size:10.5px; text-transform:uppercase; letter-spacing:.18em; color:var(--muted); margin-right:6px; }
.nav a{
  border:var(--frame) solid var(--soft); padding:2px 8px; font-size:11.5px;
  color:var(--ink); text-decoration:none; white-space:nowrap;
}
.nav a:hover{ background:var(--hair); }
.nav a.on{ background:var(--ink); color:var(--bg); border-color:var(--ink); }

/* ── интро ─────────────────────────────────────────── */
.lede{ font-size:17px; line-height:1.6; margin:0 0 18px; }
.lede b{ font-weight:500; }
.caps{ font-size:10.5px; text-transform:uppercase; letter-spacing:.18em; color:var(--muted);
  font-weight:500; margin:0 0 9px; }

/* ── карта разделов ────────────────────────────────── */
.map{ border:var(--frame) solid var(--ink); display:grid;
  grid-template-columns:44px 1fr 1fr; margin:0 0 26px; }
.map > div{ padding:8px 12px; border-right:var(--frame) solid var(--soft);
  border-top:var(--frame) solid var(--soft); font-size:13px; }
.map > div:nth-child(3n){ border-right:none; }
.map > div:nth-child(-n+3){ border-top:none; background:var(--hair);
  font-size:10px; text-transform:uppercase; letter-spacing:.15em; color:var(--muted); }
.map .n{ color:var(--muted); font-size:12px; }
.map .when{ color:var(--muted); font-size:12.5px; }
.map a{ color:var(--ink); text-decoration:none; border-bottom:var(--frame) solid var(--soft); }
.map a:hover{ border-bottom-color:var(--ink); }

/* ── секции гайда ──────────────────────────────────── */
.sec{ border-top:var(--frame) solid var(--ink); padding-top:26px; margin-top:38px; }
.sec-head{ display:flex; align-items:baseline; gap:14px; margin-bottom:4px; }
.sec-num{ font-size:11px; letter-spacing:.18em; color:var(--muted); }
.sec h1{ font-size:25px; font-weight:600; margin:0 0 16px; letter-spacing:-.01em; }
.sec h2{ font-size:17.5px; font-weight:600; margin:30px 0 9px; }
.sec h3{ font-size:14.5px; font-weight:600; margin:22px 0 7px; color:var(--muted); }
.sec p{ margin:0 0 13px; }
.sec ul,.sec ol{ margin:0 0 13px; padding-left:22px; }
.sec li{ margin-bottom:5px; }
.sec li::marker{ color:var(--muted); }
.sec strong{ font-weight:600; }
.sec hr{ border:none; border-top:var(--frame) solid var(--soft); margin:26px 0; }
.sec a{ color:var(--ink); text-decoration:none; border-bottom:var(--frame) solid var(--soft); }
.sec a:hover{ border-bottom-color:var(--ink); }

.sec img{ display:block; width:100%; height:auto; border:var(--frame) solid var(--soft);
  margin:0 0 22px; }

.sec blockquote{ margin:0 0 14px; padding:2px 0 2px 16px;
  border-left:2px solid var(--ink); color:var(--muted); font-size:14.5px; }
.sec blockquote p{ margin:0 0 6px; }
.sec blockquote p:last-child{ margin-bottom:0; }

.sec table{ border-collapse:collapse; width:100%; margin:0 0 18px; font-size:13.5px;
  border:var(--frame) solid var(--ink); }
.sec th,.sec td{ padding:8px 12px; border-right:var(--frame) solid var(--soft);
  border-top:var(--frame) solid var(--soft); text-align:left; vertical-align:top; }
.sec th{ background:var(--hair); font-size:10px; text-transform:uppercase;
  letter-spacing:.15em; color:var(--muted); font-weight:500; border-top:none; }
.sec th:last-child,.sec td:last-child{ border-right:none; }
.sec thead + tbody tr:first-child td{ border-top:var(--frame) solid var(--soft); }

.sec pre{ border:var(--frame) solid var(--soft); background:var(--bg);
  padding:13px 15px; overflow-x:auto; font-size:12.5px; line-height:1.55; margin:0 0 16px; }
.sec code{ font-family:var(--mono); font-size:12.8px; background:var(--hair); padding:1px 5px; }
.sec pre code{ background:none; padding:0; font-size:12.5px; }

.up{ font-size:11px; letter-spacing:.06em; color:var(--muted); text-decoration:none;
  border-bottom:var(--frame) solid var(--soft); }
.up:hover{ border-bottom-color:var(--ink); }
.sec-foot{ margin-top:20px; }

/* ── подвал ────────────────────────────────────────── */
.shaper-footer{ border-top:var(--frame) solid var(--ink); padding-top:14px; margin-top:44px;
  color:var(--muted); font-size:12.5px; letter-spacing:.04em;
  display:grid; grid-template-columns:1fr auto; gap:20px; align-items:baseline; }
.shaper-footer b{ color:var(--ink); font-weight:500; }
.shaper-footer a{ color:var(--muted); }

.dot{ display:inline-block; width:5px; height:5px; background:var(--flow);
  border-radius:50%; vertical-align:middle; margin-left:5px; }

@media (max-width:760px){
  .wrap{ padding:22px 16px 44px; }
  .shaper-header{ grid-template-columns:1fr; gap:6px; }
  .shaper-header .meta{ justify-self:start; text-align:left; }
  .map{ grid-template-columns:34px 1fr; }
  .map > div:nth-child(3n){ display:none; }
  .map > div:nth-child(3n-1){ border-right:none; }
  .sec h1{ font-size:21px; }
  .shaper-footer{ grid-template-columns:1fr; }
}
"""

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])


def convert(num, slug, text):
    """markdown раздела → html, без первого H1 (он рисуется шапкой секции)."""
    text = re.sub(r"^#\s+.*?\n", "", text, count=1)
    # ссылки между разделами → якоря на этой же странице
    text = re.sub(r"\]\((\d\d)-[a-z]+\.md(#[\w-]+)?\)", lambda m: f"](#s{m.group(1)})", text)
    text = text.replace("](CONTRIBUTING.md)",
                        "](https://github.com/ai-mindset-org/s26-lab/blob/main/guide/CONTRIBUTING.md)")
    text = text.replace("](../README.md)", "](https://github.com/ai-mindset-org/s26-lab)")
    # картинки лежат рядом со страницей
    text = text.replace("../assets/", "assets/")
    md.reset()
    return md.convert(text)


def main():
    OUT_ASSETS.mkdir(parents=True, exist_ok=True)

    # картинки: карта + фигуры десяти разделов. context-fig-growth не берём —
    # она иллюстрирует CONTRIBUTING, которого на этой странице нет.
    needed = ["context-guide-map.png"] + [f"context-fig-{s}.png" for _, s, _, _ in SECTIONS]
    copied = []
    for name in needed:
        src = ROOT / "assets" / name
        if not src.exists():
            raise SystemExit(f"нет картинки: {src}")
        shutil.copy2(src, OUT_ASSETS / name)
        copied.append(name)
    for stale in OUT_ASSETS.iterdir():
        if stale.name not in needed:
            stale.unlink()
            print(f"убрана лишняя: {stale.name}")

    nav = '<div class="nav"><span class="lbl">разделы</span>' + "".join(
        f'<a href="#s{n}">{n} · {title}</a>' for n, _, title, _ in SECTIONS
    ) + "</div>"

    rows = ['<div class="map"><div>#</div><div>раздел</div><div>когда браться</div>']
    for n, _, title, when in SECTIONS:
        rows.append(f'<div class="n">{n}</div><div><a href="#s{n}">{title}</a></div>'
                    f'<div class="when">{when}</div>')
    rows.append("</div>")
    mapping = "".join(rows)

    secs = []
    for n, slug, title, _ in SECTIONS:
        body = convert(n, slug, (GUIDE / FILES[n]).read_text(encoding="utf-8"))
        secs.append(
            f'<section class="sec" id="s{n}">'
            f'<div class="sec-head"><span class="sec-num">{n}</span></div>'
            f'<h1>{title}</h1>{body}'
            f'<p class="sec-foot"><a class="up" href="#top">↑ к карте гайда</a></p>'
            f'</section>'
        )

    html = f"""<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>гайд · сборка личного контекста · s26</title>
<meta name="description" content="рабочий гайд к элементу «контекст» программы S26: как собрать личный контекст, чтобы агент получил профиль человека, а не догадки.">
<meta name="robots" content="index, follow">
<style>{CSS}</style>
</head><body>
<div class="wrap" id="top">

<header class="shaper-header">
  <span class="brand">shaper</span>
  <span class="crumb">гайд · сборка личного контекста · s26 · элемент 2 дуги</span>
  <span class="meta">s26-lab · <b>ai mindset</b> · 2026</span>
</header>

{nav}

<p class="lede">рабочий гайд к <b>элементу 2 «контекст»</b> программы S26: аудит жизни, инвентаризация поверхностей, чистка сохранёнок — чтобы агент получил профиль человека, а не догадки.</p>
<p class="lede">нужен на <b>pre-lab и W1</b>: там участник собирает входной документ и context layer, на который дальше встают состояние, агенты и форма.</p>

<p class="caps">карта гайда · порядок неслучаен</p>
<p>каждый следующий раздел нужен только тогда, когда предыдущий начал жать. <strong>строить всё сразу — самый дорогой способ бросить на середине.</strong><span class="dot"></span></p>

<img src="assets/context-guide-map.png" alt="как собирается личный контекст" style="width:100%;height:auto;border:1px solid var(--soft);margin:14px 0 24px">

{mapping}

<p class="caps">одно правило до всего остального</p>
<p>контекст, который лежит текстом, читается один раз на старте и дальше проигрывает вниманию. контекст, встроенный в момент действия, срабатывает независимо от того, помнишь ты о нём или нет. собирая контекст, спрашивай не «где это лежит», а <strong>«что произойдёт, когда это понадобится»</strong>.</p>

{"".join(secs)}

<footer class="shaper-footer">
  <span>пополняемый гайд · пишут проводники, участники и агенты · вход через форк и pull request<br>
  авторы: Александр Поваляев (AI Mindset) · Александр Васильев (Бесперебойник) · агенты контура</span>
  <span><b><a href="https://github.com/ai-mindset-org/s26-lab">github.com/ai-mindset-org/s26-lab</a></b></span>
</footer>

</div>
</body></html>"""

    (OUT / "index.html").write_text(html, encoding="utf-8")
    size = (OUT / "index.html").stat().st_size
    print(f"index.html: {size} байт ({size/1024:.0f} КБ)")
    print(f"картинок скопировано: {len(copied)}")


if __name__ == "__main__":
    main()
