#!/usr/bin/env python3
"""Генератор shaper-схем для guide/. Один шаблон — одна грамматика во всех фигурах.

Каждая фигура = полосы (band). Полоса = подпись + ряд блоков либо таблица.
Инверсия (active) = активное состояние, никогда цвет.
"""
import pathlib

CSS = """
  :root{ --bg:#fff; --ink:#000; --soft:#d9d9d9; --hair:#ececec; --muted:#8a8a8a; --flow:#e9b400;
    --mono:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; --frame:1px; }
  *{box-sizing:border-box;}
  html,body{ margin:0; padding:0; width:1600px; background:var(--bg); color:var(--ink);
    font-family:var(--mono); font-size:15px; line-height:1.5; -webkit-font-smoothing:antialiased; }
  body{ padding:38px 52px 30px; text-transform:lowercase; }
  header{ display:grid; grid-template-columns:auto 1fr auto; gap:28px; align-items:baseline;
    border-bottom:var(--frame) solid var(--ink); padding-bottom:14px; letter-spacing:.04em; margin-bottom:22px; }
  header .brand{ font-weight:600; letter-spacing:.18em; font-size:20px; }
  header .crumb{ color:var(--muted); font-size:14px; }
  header .meta{ color:var(--muted); font-size:12px; justify-self:end; }
  header .meta b{ color:var(--ink); font-weight:500; letter-spacing:.08em; }
  .band{ margin-bottom:22px; }
  .band-label{ font-size:10.5px; text-transform:uppercase; letter-spacing:.18em; color:var(--muted);
    margin:0 0 9px 2px; font-weight:500; }
  .row{ display:grid; gap:14px; }
  .block{ border:var(--frame) solid var(--ink); padding:14px 15px 12px; position:relative; background:var(--bg); }
  .block .num{ position:absolute; top:-11px; left:12px; width:22px; height:22px; background:var(--ink); color:var(--bg);
    border-radius:50%; display:grid; place-items:center; font-size:11px; font-weight:600; }
  .block h3{ margin:0; font-size:10px; text-transform:uppercase; letter-spacing:.16em; color:var(--muted); font-weight:500; }
  .block .lead{ font-size:15.5px; margin-top:5px; }
  .block .note{ font-size:12px; color:var(--muted); margin-top:6px; line-height:1.45; }
  .block.active{ background:var(--ink); color:var(--bg); }
  .block.active h3,.block.active .note{ color:var(--soft); }
  .block.active .num{ background:var(--bg); color:var(--ink); }
  .block.dash{ border-style:dashed; border-color:var(--muted); }
  .flow{ text-align:center; font-size:12px; color:var(--muted); letter-spacing:.1em; margin:9px 0 0; }
  .tbl{ border:var(--frame) solid var(--ink); display:grid; }
  .tbl div{ padding:8px 12px; border-right:var(--frame) solid var(--soft); font-size:13px; }
  .tbl div:last-child{ border-right:none; }
  .tbl .hd{ background:var(--hair); font-size:10px; text-transform:uppercase; letter-spacing:.15em; color:var(--muted); }
  .tbl .rh{ color:var(--muted); font-size:12px; letter-spacing:.05em; }
  .tbl .inv{ background:var(--ink); color:var(--bg); }
  .tbl .br{ border-top:var(--frame) solid var(--soft); }
  footer{ display:grid; grid-template-columns:1fr auto; align-items:baseline; gap:22px;
    border-top:var(--frame) solid var(--ink); padding-top:12px; margin-top:6px;
    color:var(--muted); font-size:12px; letter-spacing:.05em; }
  footer b{ color:var(--ink); font-weight:500; }
  .chips{ display:inline-flex; gap:6px; margin-left:10px; }
  .chips span{ border:var(--frame) solid var(--soft); padding:1px 7px; font-size:11px; }
  .chips span.on{ background:var(--ink); color:var(--bg); border-color:var(--ink); }
"""

def block(n, h3, lead, note, cls=""):
    num = f'<span class="num">{n}</span>' if n else ""
    return (f'<div class="block {cls}">{num}<h3>{h3}</h3>'
            f'<div class="lead">{lead}</div><div class="note">{note}</div></div>')

def band(label, inner):
    return f'<div class="band"><p class="band-label">{label}</p>{inner}</div>'

def row(cols, blocks):
    return f'<div class="row" style="grid-template-columns:{cols}">' + "".join(blocks) + "</div>"

def page(fid, crumb, body, chips_on, chips_all, foot_right):
    chips = "".join(f'<span class="{"on" if c==chips_on else ""}">{c}</span>' for c in chips_all)
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<title>shaper · {fid} · {crumb}</title><style>{CSS}</style></head><body>
<header><span class="brand">shaper</span>
<span class="crumb">{fid} · {crumb}</span>
<span class="meta">guide/ · <b>ai mindset</b> · 2026-07-30</span></header>
{body}
<footer><span>разделы гайда<span class="chips">{chips}</span></span>
<span><b>{foot_right}</b></span></footer>
</body></html>"""

CHIPS = ["старт", "источники", "слои", "волт", "грабли", "безопасность", "примеры"]

FIGS = {}

# ── fig.src · карта источников ────────────────────────────────────────────
FIGS["context-fig-sources"] = page(
    "fig.src", "карта источников · что брать и в каком порядке",
    band("два режима · главное различие, экономящее месяцы",
         row("1fr 1fr", [
             block("a", "живой запрос", "ходи за свежим",
                   "календарь, задачи, почта, переписка. копия расходится с оригиналом за сутки и врёт увереннее, чем пустота"),
             block("b", "локальное ядро", "храни у себя",
                   "кто ты, правила, решения, разборы. должно пережить отключение любого сервиса"),
         ]))
    + band("стоимость входа · брать снизу вверх, не наоборот",
           row("1fr 1fr 1fr", [
               block("1", "5–10 минут", "быстрые входы",
                     "календарь за 3 месяца · экспорт одного чата · надиктовка 5 минут · фото-лента", "active"),
               block("2", "30–60 минут", "средние",
                     "заметки · данные о здоровье · выписки. истинные приоритеты видны по тратам и времени"),
               block("3", "1–2 часа", "глубокие",
                     "почта · транскрипты созвонов · история кода. плотно, но требует готовности разбирать"),
           ]))
    + band("шесть поведений · проверка полноты не числом файлов, а закрытыми ролями",
           row("repeat(6,1fr)", [
               block("", "что сейчас", "живой запрос", "календарь, задачи, почта"),
               block("", "кто я", "локальное ядро", "о себе, принципы, решения"),
               block("", "как работаю", "след работы", "сессии, история, разборы"),
               block("", "как звучу", "сырой разговор", "транскрипт, голос, чат"),
               block("", "как видят", "публичная поверхность", "канал, сайт, выступления"),
               block("", "куда иду", "будущий слой", "цели, развилки, планы", "dash"),
           ]))
    + '<p class="flow">пустая роль — дыра, даже когда файлов много · будущий слой выпадает чаще прочих</p>',
    "источники", CHIPS, "guide/02-sources.md")

# ── fig.lay · слои хранения ──────────────────────────────────────────────
FIGS["context-fig-layers"] = page(
    "fig.lay", "хранение слоями · слой добавляется только когда предыдущий начал жать",
    band("порядок · строить всё сразу — самый дорогой способ бросить на середине",
         row("repeat(6,1fr)", [
             block("1", "сразу", "один документ", "пятнадцать минут, один источник, один вывод", "active"),
             block("2", "файлов больше десятка", "хранилище + имена", "версионирование и договор об именах"),
             block("3", "решения повторяются", "правила отдельно", "правило живёт не в заметке"),
             block("4", "не помнишь оснований", "журнал решений", "почему, а не только что"),
             block("5", "около сотни документов", "поиск по смыслу", "поиск по словам перестал попадать"),
             block("6", "работа длиннее захода", "чекпоинты сессий", "состояние переживает перерыв"),
         ]))
    + '<p class="flow">→ каждый слой имеет цену обслуживания · слой, который не мешает жить, не нужен</p>'
    + band("симптом перехода · по чему понятно, что пора",
           row("1fr 1fr 1fr", [
               block("", "слой 1 → 2", "«где я это записал»", "материал есть, найти нельзя"),
               block("", "слой 3 → 4", "«почему я так решил»", "выбор помнишь, основания нет"),
               block("", "слой 4 → 5", "«точно писал, но не ищется»", "формулировка была другая"),
           ]))
    + band("развернёт раздел",
           row("1fr", [
               block("", "ветка jarvis/guide-layers", "александр васильев · бесперебойник",
                     "восьмимесячный след эволюции контура · механика каждого перехода · раздел «что не сработало» с ценой", "dash"),
           ])),
    "слои", CHIPS, "guide/03-layers.md")

# ── fig.vlt · волт ───────────────────────────────────────────────────────
FIGS["context-fig-vault"] = page(
    "fig.vlt", "волт · адрес важнее папки",
    band("решение · тип живёт в имени файла, а не в дереве",
         row("1.3fr 1fr", [
             block("a", "формула имени", "{проект} {тип} описание – ГГГГ-ММ-ДД.md",
                   "дата в конце — сортировка по времени сама. имя латиницей: кириллица ломает ссылки и синхронизацию", "active"),
             block("b", "почему не папки", "выбор ветки всегда спорный",
                   "разбор звонка — это «партнёры» или «встречи»? через месяц будешь искать во второй"),
         ]))
    + band("четыре способа найти · каждый закрывает свою слепую зону",
           row("repeat(4,1fr)", [
               block("1", "помнишь название", "по типу и дате", "find по имени файла"),
               block("2", "помнишь суть", "по содержанию", "grep по всему хранилищу"),
               block("3", "не находится вообще", "по истории", "ловит переименованное — способ, который спасает чаще прочих", "active"),
               block("4", "не знал, что связано", "по графу", "соседи через wiki-ссылки"),
           ]))
    + band("границы · разные хранилища, а не разные папки",
           '<div class="tbl" style="grid-template-columns:150px 1fr 1fr 1fr">'
           '<div class="hd">контур</div><div class="hd">кто пишет</div><div class="hd">режим</div><div class="hd">сигнал маршрутизации</div>'
           '<div class="rh br">общий</div><div class="br">несколько человек и роботы</div><div class="br">общее версионируемое</div><div class="br">команда, партнёр, задача</div>'
           '<div class="rh br">личный</div><div class="br">один человек</div><div class="br">приватное</div><div class="br">всё остальное</div>'
           '<div class="rh br">закрытый</div><div class="br">один человек</div><div class="inv br">локально, обезличивание до отправки</div><div class="br">практика, здоровье, отношения</div>'
           '</div>')
    + '<p class="flow">общее у контуров — договор об именах и типы · поэтому материал переносится без переписывания</p>',
    "волт", CHIPS, "guide/04-vault.md")

# ── fig.sec · безопасность ───────────────────────────────────────────────
FIGS["context-fig-security"] = page(
    "fig.sec", "безопасность контекста · границы позволяют быть честным там, где это безопасно",
    band("четыре режима обращения с чувствительным",
         row("repeat(4,1fr)", [
             block("1", "не нужен ни одной задаче", "не собирать", "не выгружаешь вообще"),
             block("2", "нужен тебе, не системе", "собрать локально", "лежит на диске, в облако не идёт"),
             block("3", "паттерн полезен, детали нет", "обезличить", "большинство материала попадает сюда и хуже всего описано", "active"),
             block("4", "ничего чувствительного", "отдать как есть", "обычный источник"),
         ]))
    + band("обезличивание · подъём от фактуры к механике, а не замена имён на буквы",
           row("1fr 1fr 1fr", [
               block("", "сырое", "«разговор с N 14 июля про переезд, она давит, я тяну»", "фактура целиком"),
               block("", "плохо", "«разговор с N. 14 июля про переезд в Л.»", "узнаётся по датам и контексту, ничего не защищено"),
               block("", "хорошо", "«повторяющийся конфликт: близкий торопит с решением, тяну из-за темпа, не из-за решения»", "паттерн сохранён, фактура снята", "active"),
           ]))
    + '<p class="flow">проверка: дай текст тому, кто знает тебя, но не знает истории · назвал участников — обезличено плохо</p>'
    + band("границы, которые ломаются молча",
           row("1fr 1fr 1fr", [
               block("", "приватность через незнание адреса", "не защищён, а не найден пока",
                     "живой случай: гейт в конфиге был написан, но не срабатывал из-за порядка правил. изнутри 200, снаружи файл открыт"),
               block("", "папка, которая публикуется сама", "внимательность отказывает",
                     "механическая проверка перед сохранением, ложное срабатывание снимается флагом и остаётся в истории"),
               block("", "доступ, выданный один раз", "живёт годами",
                     "ревизия «кто ещё имеет доступ» скучна ровно до первого инцидента"),
           ])),
    "безопасность", CHIPS, "guide/06-security.md")

# ── fig.grw · как гайд растёт ────────────────────────────────────────────
FIGS["context-fig-growth"] = page(
    "fig.grw", "как гайд пополняется · вещь не двух авторов",
    band("кто пишет · материал участника ценнее материала автора",
         row("repeat(4,1fr)", [
             block("1", "проводники", "метод и механика", "разборы застреваний, прямой push или PR"),
             block("2", "участники", "свой способ и свои грабли", "форк → PR, без ожидания доступа. помнят, где было трудно", "active"),
             block("3", "гостевые практики", "законченный кейс", "через PR или проводника"),
             block("4", "агенты", "цифры с работающих систем", "PR с указанием, чем проверено"),
         ]))
    + band("какой контекст собирается · проверяемая механика, не рассказ о системе",
           row("repeat(4,1fr)", [
               block("", "механика", "как устроено и чем платишь", "обязательно с ценой решения"),
               block("", "цифра", "измеренное, с указанием чем", "цифра без источника — мнение"),
               block("", "грабля", "симптом → причина → цена", "симптом первым: по нему узнают себя"),
               block("", "формулировка", "дословная фраза о затыке", "единственный честный портрет читателя"),
           ]))
    + band("ветки в работе · параллельная сборка",
           row("1fr 1fr 1fr", [
               block("", "jarvis/guide-layers", "слои хранения", "механика каждого перехода", "dash"),
               block("", "jarvis/guide-gates", "механика срабатывания", "контекст в момент действия против текста", "dash"),
               block("", "jarvis/guide-failures", "что не сработало", "шесть пунктов с ценой каждого", "dash"),
           ]))
    + band("формат pull request · три строки",
           row("1fr",
               [block("", "обязательны все три", "что добавил · чем проверено · подтверждение что личных данных нет",
                      "третья строка не формальность: на ней ловится большая часть утечек")])),
    "примеры", CHIPS, "guide/CONTRIBUTING.md")

out = pathlib.Path(__file__).parent
for name, html in FIGS.items():
    (out / f"{name}.html").write_text(html, encoding="utf-8")
    print("написано", name)
