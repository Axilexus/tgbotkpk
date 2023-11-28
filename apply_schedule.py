from docx import Document
import os
from DataBase import DataBase
import gdown
class Schedule:
    def __init__(self):
        pass
    def download(self, url):
        url = url.split("/")

        url = f'https://{url[2]}/uc?id={url[5]}'
        gdown.download(url, quiet=False)

    def search(self, search, name):
        self.doc = Document(name)

        tables = self.doc.tables

        text = ""
        for p in range(len(tables)):
            for i in range(len(tables[p].rows)):
                if i%5 == 0:
                    for j in range(len(tables[p].rows[i].cells)):
                        if j%3==0:
                            if search == tables[p].rows[i].cells[j].text.strip():
                                text += tables[p].rows[i].cells[j].text.strip() + '\t'
                                text += tables[p].rows[i].cells[j+2].text.strip() + '\n'
                                for k in range(1, 5):
                                    text += tables[p].rows[i+k].cells[j].text.strip() + '\t'
                                    text += tables[p].rows[i+k].cells[j+1].text.strip() + '\t'
                                    text += tables[p].rows[i+k].cells[j+2].text.strip() + "\n"
                                return text

    def send_schelude(self, chat_id):
        Schedule = self
        groups = DataBase('groups.db')
        # Создаем таблицу для хранения данных о чатах
        groups.cur.execute('''CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY, group_name TEXT)''')
        groups.conn.commit()
        words = os.listdir()
        groups.cur.execute("SELECT * FROM groups WHERE chat_id=?", (chat_id,))
        group = groups.cur.fetchone()
        text = ""
        filtred_files = []
        days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']
        sorted_files = [word for day in days for word in words if day in word]
        for file in sorted_files:
            if "docx" in file:
                text += "```" + file.split(".")[0] + '\n'
            if "ПОНЕДЕЛЬНИК" in file:
                text += Schedule.search(group[1], file)
            if "ВТОРНИК" in file:
                text += Schedule.search(group[1], file)
            if "СРЕДА" in file:
                text += Schedule.search(group[1], file)
            if "ЧЕТВЕРГ" in file:
                text += Schedule.search(group[1], file)
            if "ПЯТНИЦА" in file:
                text += Schedule.search(group[1], file)
            if "СУББОТА" in file:
                text += Schedule.search(group[1], file)
            text += '```\n'
        return text