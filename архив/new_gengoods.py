import os
import csv
import re

# === Параметры ===
csv_path = "marocgoods.csv"
html_path = "maroc.html"

# Проверка файлов
if not os.path.exists(html_path):
    print(f"❌ HTML-файл '{html_path}' не найден.")
    exit()

if not os.path.exists(csv_path):
    print(f"❌ CSV-файл '{csv_path}' не найден.")
    exit()

# Читаем HTML
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Читаем CSV
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")  # указали правильный разделитель
    reader.fieldnames = [
        h.strip() for h in reader.fieldnames
    ]  # убираем пробелы из заголовков
    for row in reader:
        row = {k.strip(): v for k, v in row.items()}  # убираем пробелы из ключей
        name = row["Name"].strip()
        description = row["Description"].strip()
        price = row["Price"].strip()

        # Находим блок по id
        section_pattern = re.compile(
            rf'(<section[^>]*id="{re.escape(name)}"[^>]*>.*?</section>)', re.DOTALL
        )
        match = section_pattern.search(html_content)
        if not match:
            print(f"⚠️ Блок с id='{name}' не найден, пропущен.")
            continue

        section_html = match.group(1)

        # Обновляем описание
        section_html = re.sub(
            r'(<p class="u-align-left u-text u-text-2">).*?(</p>)',
            lambda m: m.group(1) + description + m.group(2),
            section_html,
            flags=re.DOTALL,
        )

        # Обновляем цену
        section_html = re.sub(
            r"(<h3[^>]*u-text-3[^>]*>).*?(</h3>)",
            lambda m: m.group(1) + price + " ₽" + m.group(2),
            section_html,
            flags=re.DOTALL,
        )

        # Заменяем старый блок на новый
        html_content = html_content.replace(match.group(1), section_html)

# Сохраняем результат
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Описания и цены обновлены по CSV")
