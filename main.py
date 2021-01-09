import sys
import time

from PyQt5 import QtWidgets

import register
import start
import student
import admin
import lection
import test
import result
import session

from db import *

# Основной класс интерфейса
class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = start.Ui_MainWindow()
        self.ui.setupUi(self)

        self.userid = 0
        self.reg = Reg()
        self.student = Student()
        self.admin = Admin()

        self.ui.log_in.clicked.connect(self.log_in_func)
        self.ui.sign_in.clicked.connect(self.sign_in_func)

    def log_in_func(self):
        self.ui.label.setText("")
        login = self.ui.login.text()
        password = self.ui.password.text()

        result = log_in_db(login, password)
        session.userid, session.first_name, session.second_name, session.login, session.password, session.course, session.group, session.access, session.statistic_tests, session.statistic_lections = result[1]
        if result[0]:
            self.ui.label.setText("успешный вход")
            if session.access:
                self.destroy()
                self.admin.show()

            else:
                self.destroy()
                self.student.update_all()
                self.student.show()

        else:
            self.ui.label.setText("Данные неверные")

    def sign_in_func(self):
        self.reg.show()


class Reg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = register.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.reg.clicked.connect(self.register)

    def register(self):
        first_name = self.ui.first_name.text()
        second_name = self.ui.second_name.text()
        group = self.ui.group.text()
        login = self.ui.login.text()
        password = self.ui.password.text()

        if first_name != '' and second_name != '' and group != '' and login != '' and password != '':
            if registration_db(first_name, second_name, login, password, group):
                self.ui.label.setText("Успешно зарегестрирован")
            else:
                self.ui.label.setText("Логин занят")
        else:
            self.ui.label.setText("Заполните все данные")


class Student(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = student.Ui_MainWindow()
        self.ui.setupUi(self)

        self.lection = Lection()
        self.test = Test()

        self.ui.edit_data.clicked.connect(self.edit_data)
        self.ui.lections_start.clicked.connect(self.open_lection)
        self.ui.tests_start.clicked.connect(self.open_test)

    def edit_data(self):
        login = self.ui.login.text()
        new_password = self.ui.new_password.text()
        old_password = self.ui.old_password.text()

        if editdata(login, new_password, old_password, session.userid):
            self.ui.status_data.setText("Данные изменены успешно!")
        else:
            self.ui.status_data.setText("Старый пароль не подошёл")

    def update_all(self):
        self.ui.name.setText('{} {}'.format(session.first_name, session.second_name))
        self.ui.course.setText('{} курс'.format(session.course))
        self.ui.login.setText(session.login)
        self.ui.tests_total.setText("{}/{} ({}%)".format(len(session.statistic_tests.split("|"))-1, counttests(), str("%.2f" % ((len(session.statistic_tests.split("|"))-1)*100/counttests()))))
        self.ui.tests_answers.setText(countanswers(session.statistic_tests))
        self.ui.lections_total.setText("{}/{} ({}%)".format(len(session.statistic_lections.split("|"))-1, countlections(), str("%.2f" % ((len(session.statistic_lections.split("|"))-1) *100/countlections()))))
        for name in os.listdir("lections"):
            self.ui.lections_list.addItem(name[:name.rfind(".")])
        for name in get_tests():
            self.ui.tests_list.addItem(name)

    def open_lection(self):
        self.lection.loadlection(self.ui.lections_list.currentText())

    def open_test(self):
        self.test.name = self.ui.tests_list.currentText()
        self.test.get_info()
        self.test.update()
        self.test.show()
        self.destroy()


class Admin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = admin.Ui_MainWindow()
        self.ui.setupUi(self)

        self.update_test_list()
        self.loadstat()

        self.ui.refresh_tests.clicked.connect(self.update_tests)
        self.ui.add_test.clicked.connect(self.add_test)
        self.ui.delete_test.clicked.connect(self.delete_test)
        self.ui.search_student.clicked.connect(self.update_info)

    def update_info(self):
        second_name = self.ui.second_name.text()
        total = ""
        if search_by_second_name(second_name):
            self.ui.info.setText("")
            total = "Тестов пройдено: {}/{} ({}%)\n".format(len(search_by_second_name(second_name)[8].split("|")) - 1, counttests(),
                                                             str("%.2f" % ((len(search_by_second_name(second_name)[8].split(
                                                                 "|")) - 1) * 100 / counttests())))
            total += "Правильных ответов: {}\n".format(countanswers(search_by_second_name(second_name)[8]))
            total += "Лекций пройдено: {}/{} ({}%)".format(len(search_by_second_name(second_name)[9].split("|")) - 1, countlections(), str(
                    "%.2f" % ((len(search_by_second_name(second_name)[9].split("|")) - 1) * 100 / countlections())))
            if len(search_by_second_name(second_name)[9].split("|")) > 1:
                total += "\n\nПройденые лекции:\n"
                for i in search_by_second_name(second_name)[9].split("|")[:-1]:
                    total += "- {}\n".format(i)

            if len(search_by_second_name(second_name)[8].split("|")) > 1:
                total += "\n\nПройденные тесты:\n"
                for i in search_by_second_name(second_name)[8].split("|")[:-1]:
                    temp = get_test_name_by_id(i.split("(")[0])
                    total += "- {}\n".format(temp)
            self.ui.textBrowser.setText(total)
        else:
            self.ui.textBrowser.setText("")
            self.ui.info.setText("Неверная фамилия")

    def update_test_list(self):
        for i in range(100):
            self.ui.tests_list.removeItem(self.ui.tests_list.currentIndex())
        for name in get_tests():
            self.ui.tests_list.addItem(name)

    def update_tests(self):
        test = get_test(self.ui.tests_list.currentText())
        test_text = "{}\n\n\n".format(self.ui.tests_list.currentText())
        for i in range(len(test[0])):
            test_text += "{}\n-{}\n-{}\n\n".format(test[0][i], test[1][i][0], test[1][i][1])
        self.ui.test_output.setText(test_text)

    def add_test(self):
        add_test(self.ui.test_name.text(), self.ui.test_questions.toPlainText())
        self.update_test_list()

    def delete_test(self):
        delete_test_by_id(get_test_id_by_name(self.ui.tests_list.currentText()))
        self.update_test_list()

    def loadstat(self):
        self.ui.statistic_list.setRowCount(0)
        result = loaddata()
        for row_number, row_data in enumerate(result):
            self.ui.statistic_list.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.statistic_list.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))


class Lection(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = lection.Ui_MainWindow()
        self.ui.setupUi(self)

    def loadlection(self, file):
        f = open('lections/{}.txt'.format(file), 'r')
        self.ui.textBrowser.setText(f.read())
        self.show()
        add_lecion(session.userid, file + "|")


class Test(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = test.Ui_MainWindow()
        self.ui.setupUi(self)

        self.result = Result()

        self.total = []
        self.info = []
        self.question = 1
        self.name = ''
        self.ui.next.clicked.connect(self.next_qustion)

    def get_info(self):
        self.info = get_test(self.name)

    def update(self):
        self.ui.question.setText(self.info[0][self.question-1])
        self.ui.ans1.setText(self.info[1][self.question-1][0])
        self.ui.ans2.setText(self.info[1][self.question-1][1])

    def next_qustion(self):
        self.total.append([self.question, self.ui.ans1.isChecked()])
        if len(self.info[0]) > self.question:
            self.question += 1
            self.update()
        else:
            self.result.name = self.name
            self.result.total = self.total
            self.result.update()
            self.result.show()
            self.destroy()


class Result(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = result.Ui_MainWindow()
        self.ui.setupUi(self)

        self.name = ''
        self.total = []

    def update(self):

        count = 0
        text = "Ваши результаты:\n"
        for row in self.total:
            text += "{}: {}\n".format(row[0], "+" if row[1] else "-")
            if row[1]:
                count += 1
        text += "\nИтого: {}/{} ({}%)".format(count, len(self.total), count*100/len(self.total))
        add_test_result(session.userid, get_test_id_by_name(self.name), [count, len(self.total)])
        self.ui.total.setText(text)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())
