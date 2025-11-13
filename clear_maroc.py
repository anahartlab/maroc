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

## Удаляем старую навигацию, если есть
for old_nav in soup.find_all("nav", class_="u-nav"):
    old_nav.decompose()

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
    # Создаем контейнер для кнопки меню и навигации
    menu_container = soup.new_tag("div", **{"id": "menu-container"})
    # Кнопка для сворачивания/разворачивания
    toggle_btn = soup.new_tag("button", **{"id": "menu-toggle"})
    toggle_btn.string = "Развернуть навигационное меню"
    toggle_btn["style"] = (
        "padding:12px 25px; margin:20px auto; cursor:pointer; border-radius:8px; "
        "background:#007BFF; color:#fff; font-weight:bold; border:none; "
        "box-shadow:0 4px 6px rgba(0,0,0,0.3); display:block; transition:0.3s;"
    )
    menu_container.append(toggle_btn)
    menu_container.append(nav)
    header.insert_after(menu_container)

    # Добавляем кнопку "В начало"
    back_btn = soup.new_tag("button", **{"id": "back-to-menu"})
    back_btn.string = "В начало"
    back_btn["style"] = (
        "position:fixed; bottom:20px; right:20px; padding:10px 15px; background:#333; color:#fff; border:none; border-radius:5px; cursor:pointer; z-index:999;"
    )
    soup.body.append(back_btn)

    # Добавляем скрипт для сворачивания и кнопки "В начало"
    script = soup.new_tag("script")
    script.string = """
    const toggleBtn = document.getElementById("menu-toggle");
    const nav = document.querySelector("#menu-container nav");
    toggleBtn.addEventListener("click", function() {
        if (nav.style.display === "none") {
            nav.style.display = "block";
            toggleBtn.textContent = "Свернуть навигационное меню";
            toggleBtn.style.boxShadow = "0 6px 8px rgba(0,0,0,0.4)";
        } else {
            nav.style.display = "none";
            toggleBtn.textContent = "Развернуть навигационное меню";
            toggleBtn.style.boxShadow = "0 4px 6px rgba(0,0,0,0.3)";
        }
    });
    toggleBtn.addEventListener("mouseover", function() {
        toggleBtn.style.boxShadow = "0 8px 12px rgba(0,0,0,0.5)";
    });
    toggleBtn.addEventListener("mouseout", function() {
        if (nav.style.display === "block") {
            toggleBtn.style.boxShadow = "0 6px 8px rgba(0,0,0,0.4)";
        } else {
            toggleBtn.style.boxShadow = "0 4px 6px rgba(0,0,0,0.3)";
        }
    });
    document.getElementById("back-to-menu").addEventListener("click", function() {
        document.getElementById("menu-container").scrollIntoView({behavior:"smooth"});
    });
    """
    soup.body.append(script)

# Сохраняем HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ Проданные товары удалены, навигация создана.")
