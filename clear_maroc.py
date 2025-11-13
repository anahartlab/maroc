from bs4 import BeautifulSoup

# Путь к файлу HTML
html_file = "/Users/anahart/GitHub/maroc-1/maroc.html"

# Читаем HTML
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1️⃣ Удаляем проданные товары
sections = soup.find_all("section", class_="u-clearfix u-section-16")
for section in sections:
    availability = section.find("p", class_="u-text-availability")
    if availability:
        text = availability.get_text(strip=True)
        if "0" in text or "нет" in text.lower():
            section.decompose()

## Удаляем старые меню, кнопки и контейнеры, если есть
for old_nav in soup.find_all("nav", class_="u-nav"):
    old_nav.decompose()
old_toggle = soup.find(id="menu-toggle")
if old_toggle:
    old_toggle.decompose()
old_back = soup.find(id="back-to-menu")
if old_back:
    old_back.decompose()
old_container = soup.find(id="menu-container")
if old_container:
    old_container.decompose()

# 2️⃣ Создаем новую красивую навигацию по оставшимся товарам
nav = soup.new_tag("nav", **{"class": "u-nav u-unstyled u-center"})
nav["style"] = "text-align:center; margin:20px 0;"
ul = soup.new_tag("ul", **{"class": "u-unstyled"})
ul["style"] = (
    "list-style:none; padding:0; display:flex; flex-wrap:wrap; justify-content:center; gap:15px;"
)
for section in soup.find_all("section", class_="u-clearfix u-section-16"):
    sec_id = section.get("id")
    # ищем заголовок внутри секции
    h3 = section.find(["h3", "h2", "h1"])
    if not h3:
        continue
    title = h3.get_text(strip=True)
    li = soup.new_tag("li")
    a = soup.new_tag("a", href=f"#{sec_id}")
    a["style"] = (
        "padding:5px 10px; color:#333; text-decoration:none; border-radius:5px; background-color:#f0f0f0; transition:0.3s;"
    )
    a["onmouseover"] = "this.style.backgroundColor='#dcdcdc'; this.style.color='#000';"
    a["onmouseout"] = "this.style.backgroundColor='#f0f0f0'; this.style.color='#333';"
    a.string = title
    li.append(a)
    ul.append(li)
nav.append(ul)

# Вставляем навигацию после header
header = soup.find("header")
if header:
    header.insert_after(nav)

# Сохраняем HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ Проданные товары удалены, навигация создана.")
