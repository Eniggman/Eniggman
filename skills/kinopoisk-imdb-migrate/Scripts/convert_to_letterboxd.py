import csv
import re
from datetime import datetime

# Файлы
input_file = r'data\кинопоиск_база.csv'
output_file = r'data\letterboxd_import.csv'

def clean_data():
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile)
        
        # Заголовок, который понимает Letterboxd
        writer.writerow(['Title', 'Year', 'Rating10', 'WatchedDate'])
        
        # Пропускаем первую строку (заголовок оригинала)
        next(reader, None)
        
        for row in reader:
            if not row or len(row) < 4:
                continue
                
            rus_title_raw = row[0]
            eng_title = row[1]
            rating_raw = row[2]
            date_raw = row[3]
            
            # 1. Достаем год (ищем первые 4 цифры в скобках, например "(2000)" или "(сериал, 2014 – 2018)")
            year = ""
            clean_rus_title = rus_title_raw
            match = re.search(r'\(.*?(19\d{2}|20\d{2}).*?\)', rus_title_raw)
            if match:
                year = match.group(1)
                # Убираем скобки, чтобы получить чистое русское название (на случай, если нет английского)
                clean_rus_title = re.sub(r'\s*\(.*?\)', '', rus_title_raw).strip()
                
            # 2. Определяем итоговое название. 
            # Letterboxd лучше понимает английские названия. Если его нет — берем русское.
            title = eng_title.strip() if eng_title.strip() else clean_rus_title
            
            # 3. Чистим оценку (убираем жирность markdown `**8**` -> `8`)
            rating = rating_raw.replace('*', '').strip()
            
            # 4. Форматируем дату. Letterboxd любит YYYY-MM-DD
            # У нас `12.03.2026, 19:55`
            watched_date = ""
            try:
                date_part = date_raw.split(',')[0].strip()
                dt = datetime.strptime(date_part, '%d.%m.%Y')
                watched_date = dt.strftime('%Y-%m-%d')
            except Exception as e:
                pass # Если дата кривая, оставим пустой
                
            writer.writerow([title, year, rating, watched_date])

    print(f"Готово! Файл {output_file} успешно создан. Можно загружать на Letterboxd!")

if __name__ == '__main__':
    clean_data()
