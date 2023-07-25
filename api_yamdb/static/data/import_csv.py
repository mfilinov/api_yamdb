import csv
import glob
import os
import sqlite3


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Возвращает список всех csv файлов в текущей папке.
csv_files = glob.glob(os.getcwd() + '/*.csv')

for csv_file in csv_files:
    # Получаем имя файла и расширение раздельно.
    table_name, extension = os.path.splitext(os.path.basename(csv_file))
    # Открываем файл для чтения.
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name}"
        f"({', '.join(headers)});"
        cursor.execute(create_table_query)
        insert_query = f"INSERT INTO {table_name}"
        f"VALUES ({', '.join(['?'] * len(headers))});"
        for row in reader:
            cursor.execute(insert_query, row)

conn.commit()
conn.close()

# print("Данные импортированы в db.sqlite3.") - надо, наверно в логи запихнуть?
