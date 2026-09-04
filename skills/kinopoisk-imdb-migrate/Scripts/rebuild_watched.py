import pandas as pd
import re

def rebuild_markdown(csv_path, output_path):
    # Читаем базу с сохранением оригинальных строк для оценок
    df = pd.read_csv(csv_path, sep=';', dtype={'Оценка': str})
    
    # Заголовок
    md_content = "# 🎬 Мой Киноархив\n\n"
    md_content += "| № | Название фильма | ⭐ Оценка | 📅 Дата просмотра |\n"
    md_content += "|---|-----------------|-----------|-------------------|\n"
    
    # Строки таблицы
    for i, row in df.iterrows():
        title = str(row['Название (RUS)'])
        eng_title = str(row['Название (ENG)'])
        rating = str(row['Оценка'])
        date = str(row['Дата просмотра'])
        
        # 1. Форматируем название: **Название (Год)** [English]
        # Если в названии есть скобки с годом, берем их внутрь жирного
        if '(' in title and ')' in title:
            # Ищем последнюю закрывающую скобку, чтобы захватить год
            last_bracket = title.rfind(')')
            formatted_title = f"**{title[:last_bracket+1]}**"
            suffix = title[last_bracket+1:].strip()
            if suffix:
                formatted_title += f" {suffix}"
        else:
            formatted_title = f"**{title}**"
            
        # Добавляем английское название в квадратных скобках, если оно есть
        if eng_title and eng_title.lower() != 'nan' and eng_title.strip():
            formatted_title += f" [{eng_title.strip()}]"
            
        # 2. Оценка остается как в CSV (с ** если были)
        
        md_content += f"| {i+1} | {formatted_title} | {rating} | {date} |\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

if __name__ == "__main__":
    rebuild_markdown('data/кинопоиск_база.csv', 'watched.md')
