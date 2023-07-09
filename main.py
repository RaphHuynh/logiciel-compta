import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCharts import QChartView, QPieSeries, QChart
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QPalette, Qt, QPainter
from PySide6.QtWidgets import QMainWindow, QApplication, QToolBar, QVBoxLayout, QWidget, QLabel, QTableWidget, \
    QHeaderView, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QTableWidgetItem


class WidgetAccounting(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # Left apply
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Type de dépense ou crédit", "Montant"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right apply
        self.inputDebitCreditType = QComboBox()
        self.inputDebitCreditType.addItems(
            ["Loyer", "Electricité", "Nourriture", "Boisson", "Produit entretiens", "Jeu video", "CE", "Restaurant",
             "Eau", "Autres", "Matos info", "Internet", "Transport", "Espèce"])
        self.price = QLineEdit()
        self.add = QPushButton("Ajouter")
        self.clear = QPushButton("Effacer")
        self.plot = QPushButton("Graphique")

        # Disabling "add button"
        self.add.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Ajouter Type Débit ou Crédit"))
        self.right.addWidget(self.inputDebitCreditType)
        self.right.addWidget(QLabel("Prix"))
        self.right.addWidget(self.price)
        self.right.addWidget(self.add)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.clear)

        # widget Layout
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        # Set the layout to the widget
        self.setLayout(self.layout)

        # Signals and slots
        self.add.clicked.connect(self.add_element)
        self.plot.clicked.connect(self.plot_data)
        self.clear.clicked.connect(self.clear_table)
        self.price.textChanged[str].connect(self.check_disable)

    @Slot()
    def add_element(self):
        type = self.inputDebitCreditType.currentText()
        price = self.price.text()

        try:
            price_item = QTableWidgetItem(f"{float(price):.2f}")
            price_item.setTextAlignment(Qt.AlignRight)

            self.table.insertRow(self.items)
            type_item = QTableWidgetItem(type)

            self.table.setItem(self.items, 0, type_item)
            self.table.setItem(self.items, 1, price_item)

            self.items += 1
            self.price.clear()

        except ValueError:
            print("Wrong price", price)

    @Slot()
    def check_disable(self, s):
        if not self.price.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    @Slot()
    def plot_data(self):
        # Get table information
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Logiciel de comptabilité")

        # toolbar
        toolbar = QToolBar("menu")
        self.addToolBar(toolbar)
        # add button Home toolbar
        button_home = QAction("Accueil", self)
        button_home.setStatusTip("Button Home")
        button_home.triggered.connect(self.onButtonHome)

        # add button make_accoutting
        button_accouting = QAction("Faire les comptes du mois", self)
        button_accouting.setStatusTip("Button Accouting")
        button_accouting.triggered.connect(self.onButtonAccouting)

        # add button previous_mouths
        button_previous = QAction("Regarder les mois précédents", self)
        button_previous.setStatusTip("Button previous")
        button_previous.triggered.connect(self.onButtonPrevious)

        # add button on toolbar
        toolbar.addAction(button_home)
        toolbar.addAction(button_accouting)
        toolbar.addAction(button_previous)

        # widgets of mainWindows ( credit debit history )
        layout = QVBoxLayout()  # layout vertical
        text_home = QLabel("Va falloir apprend à économiser", alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(text_home)
        self.widget_home = QWidget()
        self.widget_home.setLayout(layout)
        self.setCentralWidget(self.widget_home)

    # Function to button on toolbar
    def onButtonHome(self, s):
        print("Home", s)

    def onButtonAccouting(self, s):
        widget_history = WidgetAccounting()
        self.setCentralWidget(widget_history)

    def onButtonPrevious(self, s):
        print("Previous", s)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)

    window = MainWindow()

    # app.setStyleSheet("""
    #    QWidget {
    #        background-color: "green";
    #    }
    # """)

    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec())
