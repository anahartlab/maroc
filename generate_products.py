import os
import csv
import re

# === Параметры ===
csv_path = "marocgoods.csv"
html_path = "maroc.html"
images_dir = "images"
valid_exts = {".jpg", ".jpeg", ".png"}

# === Проверка HTML-файла ===
if not os.path.exists(html_path):
    print(f"❌ HTML-файл '{html_path}' не найден.")
    exit()

# === Читаем текущий HTML ===
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Полностью удаляем всё содержимое между </header> и <footer>
html_content = re.sub(r'(?s)(?<=</header>).*?(?=<footer)', '', html_content)

insert_index = html_content.lower().find("<footer")
if insert_index == -1:
    print("❌ Не найден <footer> в maroc.html")
    exit()

# === Читаем CSV ===
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Name"].strip()
        title = row["Title"].strip()
        description = row["Description"].strip()
        price = row["Price"].strip()
        stock = row["Stock"].strip()
        folder_path = os.path.join(images_dir, name)

        if not os.path.isdir(folder_path):
            print(f"⚠️  Пропущен '{name}' — папка '{folder_path}' не найдена.")
            continue

        images = [f for f in sorted(os.listdir(folder_path)) if os.path.splitext(f)[1].lower() in valid_exts]
        if not images:
            print(f"⚠️  Пропущен '{name}' — нет изображений.")
            continue

# Удаление существующего блока навигации
    nav_start = html_content.find('<section style="max-width: 900px; margin: 20px auto;" id="tapestries-nav">')
    if nav_start != -1:
        nav_end = html_content.find('</section>', nav_start)
        if nav_end != -1:
            html_content = html_content[:nav_start] + html_content[nav_end + len('</section>'):]

    # === Генерация навигационного блока ===
    nav_links = []
    for row in reader:
        name = row["Name"].strip()
        id_attr = name.strip()
        nav_links.append((id_attr, name))
    nav_items = ' | \n      '.join([f'<a href="#{name}">{name}</a>' for _, name in nav_links])
    nav_section = f"""
  <section style="max-width: 900px; margin: 20px auto;" id="tapestries-nav">
    <details open>
      <summary style="font-size: 1.3rem; font-weight: bold; cursor: pointer; padding: 10px 0;">
        🧵 Навигация по флуоресцентным полотнам
      </summary>
      <nav id="tapestries-nav" style="text-align: center; margin-top: 10px;">
        <!-- tapestries-nav-insert-point -->
        {nav_items}
      </nav>
    </details>
  </section>
  """

    header_end = html_content.lower().find("</header>")
    if header_end != -1:
        html_content = html_content[:header_end + len("</header>")] + nav_section + "\n" + html_content[header_end + len("</header>"):]
    else:
        print("⚠️  Не найден </header> для вставки навигации.")

    for row in reader:
        name = row["Name"].strip()
        title = row["Title"].strip()
        description = row["Description"].strip()
        seo_title = row.get("SEO Title", "").strip()
        seo_description = row.get("SEO Description", "").strip()
        seo_keywords = row.get("SEO Keywords", "").strip()
        price = row["Price"].strip()
        stock = row["Stock"].strip()
        stock = stock.replace("MOSCOW", "в Москве").replace("SAINT-PITER", "в Санкт-Петербурге").replace("CHUVASHIA", "в Чувашии")
        stock = stock.replace("в в", "в ").replace("шт.", "").strip()
        folder_path = os.path.join(images_dir, name.strip())

        if not os.path.isdir(folder_path):
            print(f"⚠️  Пропущен '{name}' — папка '{folder_path}' не найдена.")
            continue

        images = [f for f in sorted(os.listdir(folder_path))
                  if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in valid_exts]
        if not images:
            print(f"⚠️  Пропущен '{name}' — нет изображений.")
            continue
        
        # === Вставка перед <footer> ===
        html_content = html_content[:insert_index] + block + "\n" + html_content[insert_index:]
        insert_index += len(block)

# === Сохраняем результат ===
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Все товары из CSV добавлены в maroc.html")
import sys

# === Установка рабочей директории (если скрипт запущен не из корня репозитория) ===
repo_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(repo_root)