from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
from Database import *


class Window(QMainWindow):
    current_table = -1

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(600, 300, 800, 500)
        #self.setFixedSize(600, 500)
        self.setWindowTitle("Book loans database")
        self.initUI()

    def initUI(self):

        # widget centralny
        widget = QWidget()
        self.setCentralWidget(widget)

        # widget dla comboboxów
        combo_boxes = QWidget()
        combo_boxes.setFixedHeight(40)
        hbox1 = QHBoxLayout(combo_boxes)
        hbox1.setContentsMargins(50, 0, 50, 0)
        hbox1.setSpacing(20)

        # comboboxy
        self.combo_in = QComboBox()
        self.combo_in.addItems(
            ['Add person', 'Add book', 'Lend book', 'Return book'])
        self.combo_in.setFixedHeight(40)
        self.combo_in.setView(QListView())
        self.combo_in.setStyleSheet("QListView::item {height:20px;}")
        hbox1.addWidget(self.combo_in)

        self.combo_out = QComboBox()
        self.combo_out.addItems(['Persons', 'Books', 'Loans'])
        self.combo_out.setFixedHeight(40)
        self.combo_out.setView(QListView())
        self.combo_out.setStyleSheet("QListView::item {height:20px;}")
        hbox1.addWidget(self.combo_out)

        self.combo_edit = QComboBox()
        self.combo_edit.addItems(['Persons', 'Books'])
        self.combo_edit.setFixedHeight(40)
        self.combo_edit.setView(QListView())
        self.combo_edit.setStyleSheet("QListView::item {height:20px;}")
        hbox1.addWidget(self.combo_edit)

        # widget dla submitów
        submits = QWidget()
        submits.setFixedHeight(50)
        hbox2 = QHBoxLayout(submits)
        hbox2.setContentsMargins(60, 0, 60, 0)
        hbox2.setSpacing(40)

        # submity
        submit_in = QPushButton()
        submit_in.setText("Submit")
        submit_in.setFixedHeight(50)
        submit_in.clicked.connect(self.pop_add_window)
        hbox2.addWidget(submit_in)

        submit_out = QPushButton()
        submit_out.setText("Print table")
        submit_out.setFixedHeight(50)
        submit_out.clicked.connect(self.print_table)
        hbox2.addWidget(submit_out)

        submit_edit = QPushButton()
        submit_edit.setText("Edit table")
        submit_edit.setFixedHeight(50)
        submit_edit.clicked.connect(self.pop_edit_window)
        hbox2.addWidget(submit_edit)

        # tabela
        self.table = QTableWidget()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self.on_select)
        self.table_title = QLabel()
        self.table_title.setAlignment(QtCore.Qt.AlignCenter)

        # vbox
        vbox = QVBoxLayout()
        vbox.addWidget(combo_boxes)
        vbox.addWidget(submits)
        vbox.addSpacing(30)
        vbox.addWidget(self.table_title)
        vbox.addWidget(self.table)

        main_panel = QWidget()
        main_panel.setLayout(vbox)
        main_panel.setFixedWidth(600)

        # kontrolka do wyświetlania dokładnych danych o rekordzie
        grid = QGridLayout()
        self.label1, self.label2, self.label3, self.label4 = QLabel(), QLabel(), QLabel(), QLabel()
        self.label3.setText("Year")
        self.label4.setText("Lent")
        self.line1, self.line2, self.line3, self.line4 = QLineEdit(
        ), QLineEdit(), QLineEdit(), QLineEdit()
        self.line1.setReadOnly(True)
        self.line2.setReadOnly(True)
        self.line3.setReadOnly(True)
        self.line4.setReadOnly(True)
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.label2, 1, 0)
        grid.addWidget(self.label3, 2, 0)
        grid.addWidget(self.label4, 3, 0)
        grid.addWidget(self.line1, 0, 1)
        grid.addWidget(self.line2, 1, 1)
        grid.addWidget(self.line3, 2, 1)
        grid.addWidget(self.line4, 3, 1)
        grid.setRowStretch(4, 1)
        self.side_panel = QWidget()
        self.side_panel.setLayout(grid)

        hbox = QHBoxLayout()
        hbox.addWidget(main_panel)
        hbox.addWidget(self.side_panel)
        self.side_panel.hide()

        widget.setLayout(hbox)

    def print_table(self):
        self.clear_preview()
        self.side_panel.show()
        Window.current_table = self.combo_out.currentIndex()
        match self.combo_out.currentIndex():
            case 0:
                self.label1.setText("Name: ")
                self.label2.setText("Email: ")
                self.label3.hide()
                self.label4.hide()
                self.line3.hide()
                self.line4.hide()
                persons = session.query(Person).all()
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table_title.setText("PERSONS")
                self.table.setColumnCount(2)
                self.table.setRowCount(len(persons))
                self.table.setHorizontalHeaderLabels(
                    ['Name', 'Email'])
                row = 0
                for person in persons:
                    self.table.setItem(row, 0, QTableWidgetItem(person.name))
                    self.table.setItem(row, 1, QTableWidgetItem(person.email))
                    row += 1
                """ print("| ID | NAME | EMAIL | - PERSONS")
                for person in persons:
                    print(person.id, "-", person.name, "-", person.email) """
            case 1:
                self.label1.setText("Title: ")
                self.label2.setText("Author: ")
                self.label3.show()
                self.label4.show()
                self.line3.show()
                self.line4.show()
                books = session.query(Book).all()
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table.horizontalHeader().setSectionResizeMode(
                    0, QHeaderView.ResizeToContents)

                self.table_title.setText("BOOKS")
                self.table.setColumnCount(4)
                self.table.setRowCount(len(books))
                self.table.setHorizontalHeaderLabels(
                    ['Title', 'Author', 'Year', 'Lent'])
                row = 0
                for book in books:
                    self.table.setItem(row, 0, QTableWidgetItem(book.title))
                    self.table.setItem(row, 1, QTableWidgetItem(book.author))
                    self.table.setItem(
                        row, 2, QTableWidgetItem(str(book.year)))
                    self.table.setItem(
                        row, 3, QTableWidgetItem(str(book.lent)))
                    row += 1
                """ print("| ID | AUTHOR | TITLE | YEAR | LENT | - BOOKS")
                for book in books:
                    print(book.id, "-", book.author, "-",
                          book.title, "-", book.year, "-", book.lent) """
            case 2:
                self.label1.setText("Borrower id: ")
                self.label2.setText("Book id: ")
                self.label3.hide()
                self.label4.hide()
                self.line3.hide()
                self.line4.hide()
                loans = session.query(Loan).all()
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table_title.setText("LOANS")
                self.table.setRowCount(0)
                self.table.setColumnCount(2)
                self.table.setRowCount(len(loans))
                self.table.setHorizontalHeaderLabels(
                    ['Borrower id', 'Book id'])
                row = 0
                for loan in loans:
                    self.table.setItem(
                        row, 0, QTableWidgetItem(str(loan.borrower_id)))
                    self.table.setItem(
                        row, 1, QTableWidgetItem(str(loan.book_id)))
                    row += 1
                """ print("| BORROWER_ID | BOOK_ID | - LOANS")
                for loan in loans:
                    print(loan.borrower_id, "-", loan.book_id) """
            case _:
                print("Wrong opt")

    def on_select(self, selected):
        for x in selected.indexes():
            k = x.row()
            self.line1.setText(self.table.item(k, 0).text())
            self.line2.setText(self.table.item(k, 1).text())
            if Window.current_table == 1:
                self.line3.setText(self.table.item(k, 2).text())
                self.line4.setText(self.table.item(k, 3).text())

    def edit_table(self):
        pass

    def clear_preview(self):
        self.line1.setText('')
        self.line2.setText('')
        self.line3.setText('')
        self.line4.setText('')

    def pop_add_window(self):
        self.pop = PopUpWindow(self.combo_in.currentIndex())
        self.pop.show()
        self.pop.exec_()
        # automatyczne odświeżanie tabeli
        if(PopUpWindow.op_num != -1 != Window.current_table and
           (PopUpWindow.op_num == Window.current_table == 0 or
                (PopUpWindow.op_num in [1, 2, 3] and Window.current_table in [1, 2]))):
            self.print_table()

    def pop_edit_window(self):
        self.pop = PopUpWindow(self.combo_edit.currentIndex()+4)
        self.pop.show()
        self.pop.exec_()
        # automatyczne odświeżanie tabeli
        if(PopUpWindow.op_num != -1 != Window.current_table and
           (PopUpWindow.op_num == 4 and Window.current_table == 0) or
                (PopUpWindow.op_num == 5 and Window.current_table == 1)):
            self.print_table()


class PopUpWindow(QDialog):
    op_num = -1

    def __init__(self, opt):
        super().__init__()
        self.opt = opt

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        submit = QPushButton()
        submit.clicked.connect(self.save_data)
        submit.setFixedSize(100, 30)
        submit.setText("Submit")

        self.grid = QGridLayout()
        match opt:
            case 0:
                self.setWindowTitle("Add person")
                self.personUI()
            case 1:
                self.setWindowTitle("Add book")
                self.bookUI()
            case 2:
                self.setWindowTitle("Lend book")
                self.lendUI()
            case 3:
                self.setWindowTitle("Return book")
                self.returnUI()
            case 4:
                self.setWindowTitle("Edit persons")
                self.editPersonsUI()
            case 5:
                self.setWindowTitle("Edit books")
                self.editBooksUI()
            case _:
                print("Wrong opt")
        vbox.addLayout(self.grid)
        vbox.addStretch()
        vbox.addWidget(submit, alignment=QtCore.Qt.AlignCenter)

    def save_data(self):
        PopUpWindow.op_num = self.opt
        match self.opt:
            case 0:
                add_person(self.line1.text(), self.line2.text())
            case 1:
                add_book(self.line1.text(),
                         self.line2.text(), self.line3.text())
            case 2:
                lend_book(self.line1.text(), self.line2.text())
            case 3:
                return_book(self.line1.text())
            case 4:
                if self.line_id.text() == '':
                    print("No id given")
                    return
                person = session.query(Person)\
                    .filter_by(id=self.line_id.text())
                if self.line1.text() != '':
                    person.update({Person.name: self.line1.text()})
                if self.line2.text() != '':
                    person.update({Person.email: self.line2.text()})
                session.commit()
            case 5:
                if self.line_id.text() == '':
                    print("No id given")
                    return
                book = session.query(Book)\
                    .filter_by(id=self.line_id.text())
                if self.line1.text() != '':
                    book.update({Book.title: self.line1.text()})
                if self.line2.text() != '':
                    book.update({Book.author: self.line2.text()})
                if self.line3.text() != '':
                    book.update({Book.year: self.line3.text()})
                session.commit()
            case _:
                print("Wrong opt")
        self.close()

    def personUI(self):
        #self.setGeometry(700, 400, 200, 120)
        self.setFixedSize(250, 120)
        label1, label2 = QLabel(), QLabel()
        self.line1, self.line2 = QLineEdit(), QLineEdit()
        label1.setText("Name: ")
        label2.setText("Email: ")
        self.grid.addWidget(label1, 0, 0)
        self.grid.addWidget(label2, 1, 0)
        self.grid.addWidget(self.line1, 0, 1)
        self.grid.addWidget(self.line2, 1, 1)

    def bookUI(self):
        self.setFixedSize(250, 140)
        label1, label2, label3 = QLabel(), QLabel(), QLabel()
        self.line1, self.line2, self.line3 = QLineEdit(), QLineEdit(), QLineEdit()
        label1.setText("Title: ")
        label2.setText("Author: ")
        label3.setText("Year: ")
        self.grid.addWidget(label1, 0, 0)
        self.grid.addWidget(label2, 1, 0)
        self.grid.addWidget(label3, 2, 0)
        self.grid.addWidget(self.line1, 0, 1)
        self.grid.addWidget(self.line2, 1, 1)
        self.grid.addWidget(self.line3, 2, 1)

    def lendUI(self):
        self.setFixedSize(250, 120)
        label1, label2 = QLabel(), QLabel()
        self.line1, self.line2, = QLineEdit(), QLineEdit()
        label1.setText("Borrower id: ")
        label2.setText("Book id: ")
        self.grid.addWidget(label1, 0, 0)
        self.grid.addWidget(label2, 1, 0)
        self.grid.addWidget(self.line1, 0, 1)
        self.grid.addWidget(self.line2, 1, 1)

    def returnUI(self):
        self.setFixedSize(250, 90)
        label1 = QLabel()
        self.line1 = QLineEdit()
        label1.setText("Book id: ")
        self.grid.addWidget(label1, 0, 0)
        self.grid.addWidget(self.line1, 0, 1)

    def editPersonsUI(self):
        self.setFixedSize(250, 140)
        label_id, label1, label2 = QLabel(), QLabel(), QLabel()
        self.line_id, self.line1, self.line2 = QLineEdit(), QLineEdit(), QLineEdit()
        label_id.setText("Id: ")
        label1.setText("Name: ")
        label2.setText("Email: ")
        self.grid.addWidget(label_id, 0, 0)
        self.grid.addWidget(label1, 1, 0)
        self.grid.addWidget(label2, 2, 0)
        self.grid.addWidget(self.line_id, 0, 1)
        self.grid.addWidget(self.line1, 1, 1)
        self.grid.addWidget(self.line2, 2, 1)

    def editBooksUI(self):
        self.setFixedSize(250, 160)
        label_id, label1, label2, label3 = QLabel(), QLabel(), QLabel(), QLabel()
        self.line_id, self.line1, self.line2, self.line3 = QLineEdit(
        ), QLineEdit(), QLineEdit(), QLineEdit()
        label_id.setText("Id: ")
        label1.setText("Title: ")
        label2.setText("Author: ")
        label3.setText("Year: ")
        self.grid.addWidget(label_id, 0, 0)
        self.grid.addWidget(label1, 1, 0)
        self.grid.addWidget(label2, 2, 0)
        self.grid.addWidget(label3, 3, 0)
        self.grid.addWidget(self.line_id, 0, 1)
        self.grid.addWidget(self.line1, 1, 1)
        self.grid.addWidget(self.line2, 2, 1)
        self.grid.addWidget(self.line3, 3, 1)


def RunWindow():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


RunWindow()
