import csv
import re

# Загружаем HTML
with open("maroc.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Полностью удаляем всё содержимое между </header> и <footer>
html_content = re.sub(r'(?s)(?<=</header>).*?(?=<footer)', '', html_content)

# Читаем CSV с товарами (marocgoods.csv)
with open("marocgoods.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    products_html = ""
    for row in reader:
        name = row["Name"].strip()
        title = row["Title"].strip()
        description = row["Description"].strip()
        price = row["Price"].strip()
        availability = row["Stock"].strip()
        images_field = row.get("Images") or row.get("images") or ""
        images = [img.strip() for img in images_field.split(";") if img.strip()]

        # SEO данные
        seo_title = row.get("seo_title", title).strip()
        seo_description = row.get("seo_description", description[:160]).strip()
        seo_keywords = row.get("seo_keywords", title).strip()

        # Уникальный id для карусели
        carousel_id = f"carousel-{name}"

        # Генерация индикаторов
        indicators = "\n".join(
            f'<li data-u-target="#{carousel_id}" data-u-slide-to="{i}" class="{"u-active " if i == 0 else ""}u-grey-70 u-shape-circle" style="width: 10px; height: 10px;"></li>'
            for i in range(len(images))
        )

        # Генерация слайдов
        slides = "\n".join(
            f'''
            <div class="{"u-active " if i == 0 else ""}u-carousel-item u-gallery-item u-carousel-item-{i+1}">
              <div class="u-back-slide">
                <img class="u-back-image u-expanded" src="images/{name}/{img}" alt="{title}" loading="lazy">
              </div>
              <div class="u-align-center u-over-slide u-shading u-valign-bottom u-over-slide-{i+1}"></div>
            </div>
            '''
            for i, img in enumerate(images)
        )

        product_block = f"""
<section class="u-clearfix u-section-16" id="{name}">
  <!--
    SEO Title: {seo_title}
    SEO Description: {seo_description}
    SEO Keywords: {seo_keywords}
  -->
  <div class="u-clearfix u-sheet u-valign-middle-md u-sheet-1">
    <div class="u-layout">
      <div class="u-layout-row">
        <div class="u-size-30">
          <div class="u-container-style u-layout-cell u-size-60">
            <div class="u-container-layout">
              <div class="custom-expanded u-carousel u-gallery u-gallery-slider u-layout-carousel u-lightbox u-show-text-none"
                   data-interval="5000" data-u-ride="carousel" id="{carousel_id}">

                <ol class="u-absolute-hcenter u-carousel-indicators">
                  {indicators}
                </ol>

                <div class="u-carousel-inner u-gallery-inner" role="listbox">
                  {slides}
                </div>

                <a class="u-carousel-control u-carousel-control-prev u-grey-70 u-icon-circle u-opacity u-opacity-70"
                   href="#{carousel_id}" role="button" data-u-slide="prev">‹</a>
                <a class="u-carousel-control u-carousel-control-next u-grey-70 u-icon-circle u-opacity u-opacity-70"
                   href="#{carousel_id}" role="button" data-u-slide="next">›</a>
              </div>
            </div>
          </div>
        </div>
        <div class="u-size-30">
          <div class="u-container-style u-layout-cell u-size-60">
            <div class="u-container-layout">
              <h3 class="u-align-center">{title}</h3>
              <p>{description}</p>
              <h3 class="u-align-center">{price} ₽</h3>
              <p class="u-align-center u-text-availability">{availability}</p>
              <div class="u-align-center">
                <a href="https://donate.stream/anahart" class="u-btn u-button-style u-palette-1-base"
                   style="border-radius: 100px;">Оплатить</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
        products_html += product_block

# Вставляем перед <footer>
insert_index = html_content.lower().find("<footer")
html_content = html_content[:insert_index] + products_html + html_content[insert_index:]

# Сохраняем
with open("maroc.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Готово! Товары обновлены с SEO и уникальными id для каруселей.")