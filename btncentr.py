import os
import re

html_path = "maroc.html"

# Чтение HTML
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()


# Функция для центровки кнопки "Оплатить"
def center_pay_buttons(match):
    section_html = match.group(0)

    # Находим цену
    price_match = re.search(
        r'(<h3[^>]*class="[^"]*u-text-3"[^>]*>.*?<\/h3>)', section_html, re.DOTALL
    )
    # Находим наличие
    availability_match = re.search(
        r'(<p[^>]*class="[^"]*u-text-availability"[^>]*>.*?<\/p>)',
        section_html,
        re.DOTALL,
    )
    # Находим кнопку "Оплатить"
    button_match = re.search(r"(<a[^>]*>Оплатить<\/a>)", section_html, re.DOTALL)

    if not (price_match and availability_match and button_match):
        return section_html  # если чего-то нет, не трогаем

    price_html = price_match.group(1)
    availability_html = availability_match.group(1)
    button_html = button_match.group(1)

    # Создаем новый блок с кнопкой между ценой и наличием
    new_block = f"{price_html}\n<div style='text-align:center'>\n{button_html}\n</div>\n{availability_html}"

    # Заменяем старый порядок на новый
    section_html = (
        section_html.replace(price_html, "")
        .replace(availability_html, "")
        .replace(button_html, "")
    )
    section_html = section_html.replace(
        "</div>\n</div>\n</div>", f"{new_block}\n</div>\n</div>\n</div>", 1
    )

    return section_html


# Применяем ко всем секциям
html_content = re.sub(
    r'(<section class="u-clearfix u-section-16"[^>]*>.*?</section>)',
    center_pay_buttons,
    html_content,
    flags=re.DOTALL,
)

# Сохраняем результат
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Кнопки 'Оплатить' перемещены по центру относительно цены и наличия")
