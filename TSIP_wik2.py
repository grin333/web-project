import sys
import requests
import sqlite3
from PIL import Image
import wikipedia
import pymorphy2
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class Page(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Начало.ui', self)
        self.scientist_name = ''
        self.btn.clicked.connect(self.nextpg)

    def nextpg(self):
        self.scientist_name = ''.join(self.lineEd.text().strip().lower().split())
        self.menu_pg = Page_2(self.scientist_name)
        self.menu_pg.show()
        self.close()


class Page_2(QMainWindow): # Меню
    def __init__(self, scientist_name):
        super().__init__()
        self.scientist_name = scientist_name
        uic.loadUi('Меню.ui', self)
        self.btn1.clicked.connect(self.nextpg1)
        self.btn2.clicked.connect(self.nextpg2)
        self.btn3.clicked.connect(self.nextpg3)
        self.btn4.clicked.connect(self.nextpg4)

    def nextpg1(self):
        self.pg_1 = Page1_1(self.scientist_name)
        self.pg_1.show()
        self.close()

    def nextpg2(self):
        self.pg_2 = Page2(self.scientist_name)
        self.pg_2.show()
        self.close()

    def nextpg3(self):
        self.pg_3 = Page3(self.scientist_name)
        self.pg_3.show()
        self.close()

    def nextpg4(self):
        self.pg_4 = Page4(self.scientist_name)
        self.pg_4.show()
        self.close()


class Page1_1(QMainWindow):  # Современники научного деятеля
    def __init__(self, scientist_name):
        super().__init__()
        self.scientist_name = scientist_name
        uic.loadUi('Button1.ui', self)
        self.btn.clicked.connect(self.inpt)

    def inpt(self):
        self.scientist_country = self.lineEd.text()
        self.scientist_industry = self.lineEd2.text()
        self.pg1 = Page1_2(self.scientist_country, self.scientist_name, self.scientist_industry)
        self.pg1.show()
        self.close()


class Page1_2(QMainWindow):  # Поиск современника
    def __init__(self, scientist_country, scientist_name, scientist_industry):
        super().__init__()
        self.scientist_country = scientist_country
        self.scientist_name = scientist_name
        self.scientist_industry = scientist_industry
        uic.loadUi('Button1.2.ui', self)

        try:
            morph = pymorphy2.MorphAnalyzer()
            # Приведение слов в нужные падеж и число
            word = morph.parse(self.scientist_industry)[0]
            word = word.inflect({'nomn', 'plur'}).word
            word2 = morph.parse(self.scientist_country)[0]
            word2 = word2.inflect({'gent', 'sing'}).word

            url = 'https://ru.wikipedia.org/wiki/' + '_'.join([i.capitalize() for i in scientist_name.split()])
            pg = requests.get(url).text.split('\n')
            for i in range(len(pg) - 1):
                if 'Дата рождения' in pg[i]:
                    q = ''.join(pg[i + 1:i + 3])
                    year = q[q.index(' год') - 4:q.index(' год')]
                    break

            url = 'https://ru.wikipedia.org/wiki/Категория:' + word.capitalize() + '_' + word2.capitalize()
            x = requests.get(url).text
            lst = []
            for i in x.splitlines():
                if '<li>' in i and 'title="' in i and 'class=' not in i:
                    lst.append('_'.join(i.split('title="')[1].split('">')[0].split()))

            contemporaries = []
            for j in lst:
                url = 'https://ru.wikipedia.org/wiki/' + j
                pg = requests.get(url).text.split('\n')
                for i in range(len(pg) - 1):
                    if 'Дата рождения' in pg[i]:
                        q = ''.join(pg[i + 1:i + 3])
                        try:
                            year2 = q[q.index(' год') - 4:q.index(' год')]
                        except Exception:
                            pass
                        break
                if abs(int(year) - int(year2)) <= 20:
                    contemporaries.append(' '.join(j.split(',_')))

            if len(contemporaries) == 0:
                raise Exception
            else:
                self.textEd.setPlainText('; '.join(self.contemporaries))
                self.btn.clicked.connect(self.nextpg1_1)
        except Exception:
            self.btn.clicked.connect(self.nextpg1_2)

    def nextpg1_1(self):
        self.pg1_1 = LastPage()
        self.pg1_1.show()
        self.close()

    def nextpg1_2(self):
        self.pg1_2 = NoAnswerPage()
        self.pg1_2.show()
        self.close()


class Page2(QMainWindow):  # Биография
    def __init__(self, scientist_name):
        super().__init__()
        self.scientist_name = scientist_name
        uic.loadUi('Button2.ui', self)

        try:
            self.scientist_biography = wikipedia.summary(self.scientist_name.capitalize())
            if self.scientist_biography is False:
                raise Exception
            else:
                self.textEd.setPlainText(self.scientist_biography)  # Вывод текста через textEdit и функцию toPlainText()
                self.btn3.clicked.connect(self.nextpg2_1)
        except Exception:
            self.btn3.clicked.connect(self.nextpg2_2)   # убраны скобки

    def nextpg2_1(self):
        self.pg2_1 = LastPage()
        self.pg2_1.show()
        self.close()

    def nextpg2_2(self):
        self.pg2_2 = NoAnswerPage()
        self.pg2_2.show()
        self.close()


class Page3(QMainWindow):  # Изображения
    def __init__(self, scientist_name):
        super().__init__()
        self.scientist_name = scientist_name
        uic.loadUi('Button4.ui', self)

        try:
            img_url = wikipedia.page(self.scientist_name).images[0]
            a = requests.get(img_url)
            img = open(self.scientist_name + '_img.jpg', 'wb')
            img.write(a.content)
            img.close()
            if img is False:
                raise Exception
            else:
                self.pixmap = QPixmap(self.scientist_name + '_img.jpg')
                img_size = Image.open(self.scientist_name + '_img.jpg')
                self.lbl.resize(img_size.size[0], img_size.size[1])
                self.lbl.setPixmap(self.pixmap)
                self.btn.clicked.connect(self.nextpg3_1)
        except Exception as e:
            self.btn.clicked.connect(self.nextpg3_2)

    def nextpg3_1(self):
        self.pg3_1 = LastPage()
        self.pg3_1.show()
        self.close()

    def nextpg3_2(self):
        self.pg3_2 = NoAnswerPage()
        self.pg3_2.show()
        self.close()


class Page4(QMainWindow): # Новая информация о научном деятеле
    def __init__(self, scientist_name):
        super().__init__()
        self.scientist_name = scientist_name
        uic.loadUi('New_inf.ui', self)
        self.btn.clicked.connect(self.ent)

    def ent(self):
        self.information = self.lnEd.text()
        self.con = sqlite3.connect("science_inf.sqlite") # соединение с бд
        self.cur = self.con.cursor() # курсор
        self.db_creation()

    def db_creation(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS scientists
                            (name TEXT, inf TEXT)""")
        res = self.cur.execute("""SELECT * FROM scientists
                                WHERE 
                                name = '{}'""".format(self.scientist_name)).fetchall()
        if len(res) == 0:
            self.cur.execute("""INSERT INTO scientists
                                (name, inf)
                                VALUES
                                ({}, {})""".format(self.scientist_name, self.information))
        elif len(res) > 0:
            self.cur.execute("""UPDATE scientists
                                SET {} = {}
                                WHERE name = '{}'""".format(self.scientist_name,
                                                            self.information,
                                                            self.scientist_name))
        self.con.commit()
        self.con.close()
        self.end_it = Page4_2()
        self.end_it.show()
        self.close()


class Page4_2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Written.ui', self)
        self.btn.clicked.connect(self.nextpg)

    def nextpg(self):
        self.lst_pg = Page()
        self.lst_pg.show()
        self.close()


class LastPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Вернуться в начало.ui', self)
        self.btn.clicked.connect(self.nextpg)

    def nextpg(self):
        self.lst_pg = Page()
        self.lst_pg.show()
        self.close()


class NoAnswerPage(QMainWindow):  # При отсутствии ответа
    def __init__(self):
        super().__init__()
        uic.loadUi('No answer.ui', self)
        self.btn.clicked.connect(self.nextpg)

    def nextpg(self):
        self.error_pg = Page()
        self.error_pg.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pg = Page()
    pg.show()
    sys.exit(app.exec_())
