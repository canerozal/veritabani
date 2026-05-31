from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox
)

from Business.musteri_service import MusteriService


class MusteriForm(QWidget):
    def __init__(self):
        super().__init__()

        self.musteri_service = MusteriService()

        self.setWindowTitle("Müşteri İşlemleri")
        self.setGeometry(300, 200, 800, 500)

        self.ad_input = QLineEdit()
        self.soyad_input = QLineEdit()
        self.telefon_input = QLineEdit()
        self.adres_input = QLineEdit()

        self.kaydet_button = QPushButton("Müşteri Ekle")
        self.listele_button = QPushButton("Müşterileri Listele")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ad", "Soyad", "Telefon", "Adres", "Kayıt Tarihi", "Aktif Mi"
        ])

        self.kaydet_button.clicked.connect(self.musteri_ekle)
        self.listele_button.clicked.connect(self.musterileri_listele)

        form_layout = QVBoxLayout()

        form_layout.addWidget(QLabel("Ad:"))
        form_layout.addWidget(self.ad_input)

        form_layout.addWidget(QLabel("Soyad:"))
        form_layout.addWidget(self.soyad_input)

        form_layout.addWidget(QLabel("Telefon:"))
        form_layout.addWidget(self.telefon_input)

        form_layout.addWidget(QLabel("Adres:"))
        form_layout.addWidget(self.adres_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.kaydet_button)
        button_layout.addWidget(self.listele_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def musteri_ekle(self):
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        telefon = self.telefon_input.text()
        adres = self.adres_input.text()

        durum, mesaj = self.musteri_service.musteri_ekle(ad, soyad, telefon, adres)

        if durum:
            QMessageBox.information(self, "Başarılı", mesaj)
            self.ad_input.clear()
            self.soyad_input.clear()
            self.telefon_input.clear()
            self.adres_input.clear()
            self.musterileri_listele()
        else:
            QMessageBox.warning(self, "Hata", mesaj)

    def musterileri_listele(self):
        musteriler = self.musteri_service.musteri_listele()

        self.table.setRowCount(len(musteriler))

        for row_index, row_data in enumerate(musteriler):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))