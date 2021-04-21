import csv
import pandas as pd
from pathlib import Path
import sqlite3

Path('C:/Users/inmor/Desktop/mon_names.db').touch()
conn = sqlite3.connect('C:/Users/inmor/Desktop/mon_names.db')
c = conn.cursor()
c.execute('''CREATE TABLE names (id int, name text)''')

users = pd.read_csv('C:/Users/inmor/Desktop/pokedex.csv')
# write the data to a sqlite table
# users.to_sql('names', conn, if_exists='append', index = False)
# c.execute('''SELECT id, name FROM users''').fetchall()

with open('C:/Users/inmor/Desktop/pokedex.csv', encoding="utf8") as csv_file:
    data_list = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in data_list:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            poke_id = row[0]
            name = row[2]
            print(f'\t{poke_id}, {name}')
            c.execute('''INSERT INTO names(id, name) VALUES(?, ?)''', (poke_id, name))
            conn.commit()
            line_count += 1
    print(f'Processed {line_count} lines.')