from bs4 import BeautifulSoup
import os

# Путь к файлу HTML
html_file = "/Users/anahart/GitHub/maroc-1/maroc.html"
# Путь к папке с изображениями товаров
images_root = "/Users/anahart/GitHub/maroc-1/images/"

# Читаем HTML
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Удаляем старые nav
for old_nav in soup.find_all("nav", class_="u-nav"):
    old_nav.decompose()

# Создаем nav с иконками
nav = soup.new_tag("nav", **{"class": "u-nav u-unstyled u-center"})
nav["style"] = "text-align:center; margin:20px 0;"
ul = soup.new_tag("ul", **{"class": "u-unstyled"})
ul["style"] = "list-style:none; padding:0; display:flex; flex-wrap:wrap; justify-content:center; gap:15px;"

for section in soup.find_all("section", class_="u-clearfix u-section-16"):
    sec_id = section.get("id")
    h3 = section.find(["h3", "h2", "h1"])
    if not h3:
        continue
    title = h3.get_text(strip=True)

    # Попытка найти главное изображение
    folder_name = sec_id  # предполагаем, что id секции = названию папки
    folder_path = os.path.join(images_root, folder_name)
    icon_src = None
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.lower().startswith("main") and file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                icon_src = f"images/{folder_name}/{file_name}"
                break

    li = soup.new_tag("li")
    a = soup.new_tag("a", href=f"#{sec_id}")
    a["style"] = "display:flex; flex-direction:column; align-items:center; text-decoration:none; color:#333;"
    if icon_src:
        img = soup.new_tag("img", src=icon_src)
        img["style"] = "width:50px; height:50px; object-fit:cover; margin-bottom:5px; border-radius:5px;"
        a.append(img)
    a.append(title)
    li.append(a)
    ul.append(li)
nav.append(ul)

header = soup.find("header")
if header:
    header.insert_after(nav)

# Сохраняем HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ Навигация с иконками создана.")