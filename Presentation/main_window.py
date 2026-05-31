from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from Presentation.musteri_form import MusteriForm
from Presentation.urun_form import UrunForm
from Presentation.bugday_form import BugdayForm
from Presentation.satis_form import SatisForm


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Değirmencilik İşletmesi Yönetim Sistemi")
        self.setGeometry(300, 200, 500, 350)

        self.musteri_form = None
        self.urun_form = None
        self.bugday_form = None
        self.satis_form = None

        title = QLabel("Değirmencilik İşletmesi Yönetim Sistemi")
        title.setAlignment(Qt.AlignCenter)

        self.musteri_button = QPushButton("Müşteri İşlemleri")
        self.urun_button = QPushButton("Ürün İşlemleri")
        self.bugday_button = QPushButton("Buğday Girişi İşlemleri")
        self.satis_button = QPushButton("Satış İşlemleri")

        self.musteri_button.clicked.connect(self.musteri_ekrani_ac)
        self.urun_button.clicked.connect(self.urun_ekrani_ac)
        self.bugday_button.clicked.connect(self.bugday_ekrani_ac)
        self.satis_button.clicked.connect(self.satis_ekrani_ac)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.musteri_button)
        layout.addWidget(self.urun_button)
        layout.addWidget(self.bugday_button)
        layout.addWidget(self.satis_button)

        self.setLayout(layout)

    def musteri_ekrani_ac(self):
        self.musteri_form = MusteriForm()
        self.musteri_form.show()

    def urun_ekrani_ac(self):
        self.urun_form = UrunForm()
        self.urun_form.show()

    def bugday_ekrani_ac(self):
        self.bugday_form = BugdayForm()
        self.bugday_form.show()

    def satis_ekrani_ac(self):
        self.satis_form = SatisForm()
        self.satis_form.show()