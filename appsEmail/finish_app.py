import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from grafic_interface import *
from datetime import datetime
from login_form import *
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Login_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_login.clicked.connect(self.login)
        self.ui.pushButton_add_user.clicked.connect(self.add_user)
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS USERS (id INTEGER PRIMARY KEY AUTOINCREMENT, USER_NAME TEXT NOT NULL, USER_PASS TEXT NOT NULL, USER_EMAIL TEXT NOT NULL, USER_EMAIL_PASS TEXT NOT NULL)')

    def login(self):
        global UserName, UserPass, UserEmail, UserEmailPass
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        try:
            UserName = self.ui.line_login.text()
            UserPass = self.ui.line_pass.text()

            cursor.execute('SELECT * FROM USERS WHERE USER_NAME = ? AND USER_PASS = ?', [UserName, UserPass])
            if len(cursor.fetchall()) > 0:
                conn.commit()
                row = cursor.execute('SELECT * FROM USERS WHERE USER_NAME = ? AND USER_PASS = ?', [UserName, UserPass])
                for i in row:
                    UserEmail = i[3]
                    UserEmailPass = i[4]

                self.myapp = MainWindow()
                self.myapp.show()
                cursor.close()
                conn.close()
                self.close()
            else:
                self.mbox('   Данные введены неверно   !!!   ')
        except:
            self.mbox('   Данные введены неверно, блин   !!!   ')

    def add_user(self):
        global UserName, UserPass, UserEmail, UserEmailPass
        UserName = self.ui.line_login.text()
        UserPass = self.ui.line_pass.text()
        UserEmail = self.ui.line_email.text()
        UserEmailPass = self.ui.line_email_pass.text()
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM USERS WHERE USER_NAME = ?', [UserName])
            if len(cursor.fetchall()) == 0:
                cursor.execute('SELECT * FROM USERS WHERE USER_NAME = ? AND USER_PASS = ?', [UserName, UserPass])
                if UserName == '' or UserPass == '' or UserEmail == '' or UserEmailPass == '':
                    self.mbox('   Заполните все данные при регистрации   !!!   ')
                elif len(cursor.fetchall()) == 0:
                    cursor.execute('INSERT INTO USERS(USER_NAME, USER_PASS, USER_EMAIL, USER_EMAIL_PASS) VALUES(?, ?, ?, ?)', [UserName, UserPass, UserEmail, UserEmailPass])
                    cursor.execute(
                        'CREATE TABLE IF NOT EXISTS ' + UserName + '_Sbor_money (id INTEGER PRIMARY KEY AUTOINCREMENT, money REAL, date TEXT, day TEXT)')
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.myapp = MainWindow()
                    self.myapp.show()
                    self.close()
                else:
                    self.login()
                    self.close()
            else:
                self.mbox('   ТАКОЕ ИМЯ УЖЕ СУЩЕСТВУЕТ   !!!   ')
        except:
            self.mbox('   Данные введены неверно   !!!   ')


    def mbox(self, body, title='  Сообщение!!!  '):
        dialog = QMessageBox(QMessageBox.Information, title, body)
        dialog.exec_()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.date_input.setText(str(datetime.strftime(datetime.now(), '%d.%m.%Y')))
        self.ui.date_period_1.setText(str(6))
        self.in_datebase()
        self.comboBoxItem()
        self.ui.pushButton_sum.clicked.connect(self.plus_money)
        self.ui.pushButton.clicked.connect(self.minus_money)
        self.ui.insert_info.clicked.connect(self.insert_info)
        self.ui.push_email.clicked.connect(self.take_email)
        self.ui.update_datebase.clicked.connect(self.update)
        self.ui.sum.clicked.connect(self.total)
        self.ui.delete_datebase.clicked.connect(self.delete_datebase)
        self.ui.pushButton_2.clicked.connect(self.add_item)
        self.ui.pushButton_3.clicked.connect(self.get_data)
        self.ui.pushButton_4.clicked.connect(self.body_add_text)


    def insert_info(self):
        money = self.ui.money_input.text()
        day = self.ui.comboBox.currentText()
        date = self.ui.date_input.text()
        try:

            money = round(float(money), 2)
            conn = sqlite3.connect('myDB.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO ' + UserName + '_Sbor_money(money, date, day) VALUES(?, ?, ?)', [money, date, day])

            conn.commit()

            cursor.close()
            conn.close()
            self.mbox('''Данные записаны!''')
            self.in_datebase()
        except:
            self.mbox('''Некорректные данные!''')
    def comboBoxItem(self):
        try:
            conn = sqlite3.connect('myDB.db')
            cursor = conn.cursor()
            cursor.execute('SELECT email FROM ' + UserName + '_EmailsList')
            for i in cursor.fetchall():
                self.ui.comboBox_email.addItem(i[0])
        except:
            pass

    def in_datebase(self):
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ' + UserName + '_Sbor_money')
        row = cursor.fetchall()
        o = 'ID          Деньги\t          Дата\t        День\n\n'
        for a in reversed(row):
            o += str(a[0]) + '       ' + str(a[1]) + '\t     ' + a[2] + '\t   ' + a[3] + '\n'
        self.ui.text_datebase.setText(o)
        cursor.close()
        conn.close()

    def add_item(self):
        try:
            o = self.ui.email_lineEdit.text()
            a = self.ui.comboBox_email.currentText()
            if len(o) == 0:
                self.ui.email_lineEdit.setText(a)
            else:
                self.ui.email_lineEdit.setText(o + ',' + a)
        except:
            self.mbox('''Некорректные данные!''')



    def take_email(self):

        addr_to = self.ui.email_lineEdit.text()
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS ' + UserName + '_EmailsList' + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL)')
        conn.commit()
        try:
            cursor.execute('SELECT email FROM ' + UserName + '_EmailsList')
            o = [i for i in addr_to.split(',') if i != '']
            h = [i[0] for i in cursor.fetchall()]
            for i in o:
                if i not in h:
                    cursor.execute('INSERT INTO ' + UserName + '_EmailsList' + '(email) VALUES(?)', [i])
                    conn.commit()
                    cursor.close()
                    conn.close()
            msg = MIMEMultipart()  # Создаем сообщение
            msg['From'] = UserEmail  # Адресат
            msg['To'] = addr_to  # Получатель
            msg['Subject'] = "Сборы"
            body = self.ui.textEdit.toPlainText()
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
            server.login(UserEmail, UserEmailPass)  # Получаем доступ
            server.send_message(msg)
            server.quit()

            self.mbox('''Письмо отправлено!''')
        except:
            self.mbox('''Некорректные данные!''')

    def body_add_text(self):
        money = self.ui.money_input.text()
        date = self.ui.date_input.text()
        message = "Сборы на " + date + " - " + str(money)
        self.ui.textEdit.setText(message)


    def total(self):
        n = self.ui.date_period_1.text()
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        cursor.execute('SELECT money FROM ' + UserName + '_Sbor_money')
        row = cursor.fetchall()
        row.reverse()
        total = 0
        try:
            for i in range(0, int(n)):
                total += row[i][0]
            self.ui.line_total.setText(str(round(total, 2)))
            cursor.close()
            conn.close()
        except:
            self.mbox('''Некорректное число!''')


    def get_data(self):
        try:
            update_id = self.ui.update_end.text()
            conn = sqlite3.connect('myDB.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ' + UserName + '_Sbor_money WHERE id = ?', [int(update_id)])
            row = cursor.fetchone()
            if len(row) == 0:
                self.mbox('''Записи с таким ID не существует!''')
            else:
                self.ui.money_input.setText(str(row[1]))
                self.ui.date_input.setText(str(row[2]))
                for i in range(len(self.ui.comboBox)):
                    if self.ui.comboBox.itemText(i) == row[3]:

                            self.ui.comboBox.setCurrentIndex(i)

            cursor.close()
            conn.close()

        except:
            self.mbox('''Введите корректный ID!''')

    def update(self):
        money = self.ui.money_input.text()
        date = self.ui.date_input.text()
        day = self.ui.comboBox.currentText()
        update_id = self.ui.update_end.text()
        try:
            update_id = int(update_id)
            money = float(money)
            conn = sqlite3.connect('myDB.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ' + UserName + '_Sbor_money WHERE id = ?', [update_id])
            row = cursor.fetchall()
            if len(row) == 0:
                self.mbox('''Записи с таким ID не существует!''')
            else:
                sql = 'UPDATE ' + UserName + '''_Sbor_money SET money = ? , date = ? , day = ?  WHERE id = ?'''

                cursor.execute(sql, [money, date, day, update_id])

                conn.commit()

                cursor.close()
                conn.close()

                self.mbox('''Данные изменены!''')
                self.ui.update_end.setText('')
                self.in_datebase()
        except:
            self.mbox('''Некорректные данные!''')

    def delete_datebase(self):
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        delete_id = self.ui.update_end.text()

        try:
            cursor.execute('SELECT * FROM ' + UserName + '_Sbor_money WHERE id = ?', [int(delete_id)])
            if len(cursor.fetchall()) == 0:

                self.mbox('''Записи с таким ID не существует!''')
            else:
                cursor.execute('DELETE FROM ' + UserName + '_Sbor_money WHERE id = ?', [int(delete_id)])

                conn.commit()

                cursor.close()
                conn.close()
                self.mbox('''Данные удалены!''')
                self.ui.update_end.setText('')
                self.in_datebase()

        except:
            self.mbox('''Введите корректный ID!''')

    def plus_money(self):
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        sum_id = self.ui.update_end.text()
        money = self.ui.money_input.text()
        try:
            sum_id = int(sum_id)
            money = float(money)
            cursor.execute('SELECT money FROM ' + UserName + '_Sbor_money WHERE id = ?', [sum_id])
            row = cursor.fetchone()
            sum = money + row[0]
            cursor.execute('UPDATE ' + UserName + '_Sbor_money SET money = ? WHERE id = ?', [round(sum, 2), sum_id])
            conn.commit()

            cursor.close()
            conn.close()
            self.in_datebase()
        except:
            self.mbox('''Некорректные данные!''')

    def minus_money(self):
        conn = sqlite3.connect('myDB.db')
        cursor = conn.cursor()
        sum_id = self.ui.update_end.text()
        money = self.ui.money_input.text()
        try:
            sum_id = int(sum_id)
            money = float(money)
            cursor.execute('SELECT money FROM ' + UserName + '_Sbor_money WHERE id = ?', [sum_id])
            row = cursor.fetchone()
            sum = row[0] - money
            cursor.execute('UPDATE ' + UserName + '_Sbor_money SET money = ? WHERE id = ?', [round(sum, 2), sum_id])
            conn.commit()

            cursor.close()
            conn.close()
            self.in_datebase()
        except:
            self.mbox('''Некорректные данные!''')


    def mbox(self, body, title='  Сообщение!!!  '):
        dialog = QMessageBox(QMessageBox.Information, title, body)
        dialog.exec_()


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp = LoginWindow()
    myapp.show()
    sys.exit(app.exec_())