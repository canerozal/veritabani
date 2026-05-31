from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox
)

from Business.bugday_service import BugdayService


class BugdayForm(QWidget):
    def __init__(self):
        super().__init__()

        self.bugday_service = BugdayService()
        self.musteriler = []

        self.setWindowTitle("Buğday Girişi İşlemleri")
        self.setGeometry(350, 220, 950, 550)

        self.musteri_combo = QComboBox()
        self.miktar_input = QLineEdit()
        self.kg_fiyat_input = QLineEdit()
        self.aciklama_input = QLineEdit()

        self.kaydet_button = QPushButton("Buğday Girişi Ekle")
        self.listele_button = QPushButton("Buğday Girişlerini Listele")

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Müşteri ID", "Ad", "Soyad", "Miktar KG",
            "KG Fiyat", "Toplam Tutar", "Giriş Tarihi", "Açıklama"
        ])

        self.kaydet_button.clicked.connect(self.bugday_giris_ekle)
        self.listele_button.clicked.connect(self.bugday_giris_listele)

        form_layout = QVBoxLayout()

        form_layout.addWidget(QLabel("Müşteri:"))
        form_layout.addWidget(self.musteri_combo)

        form_layout.addWidget(QLabel("Miktar KG:"))
        form_layout.addWidget(self.miktar_input)

        form_layout.addWidget(QLabel("KG Fiyatı:"))
        form_layout.addWidget(self.kg_fiyat_input)

        form_layout.addWidget(QLabel("Açıklama:"))
        form_layout.addWidget(self.aciklama_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.kaydet_button)
        button_layout.addWidget(self.listele_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.musterileri_yukle()
        self.bugday_giris_listele()

    def musterileri_yukle(self):
        self.musteri_combo.clear()
        self.musteriler = self.bugday_service.musteri_listele()

        for musteri in self.musteriler:
            musteri_id = musteri[0]
            ad = musteri[1]
            soyad = musteri[2]

            self.musteri_combo.addItem(f"{musteri_id} - {ad} {soyad}", musteri_id)

    def bugday_giris_ekle(self):
        if self.musteri_combo.count() == 0:
            QMessageBox.warning(self, "Hata", "Önce müşteri eklemelisiniz.")
            return

        musteri_id = self.musteri_combo.currentData()
        miktar_kg = self.miktar_input.text()
        kg_fiyat = self.kg_fiyat_input.text()
        aciklama = self.aciklama_input.text()

        durum, mesaj = self.bugday_service.bugday_giris_ekle(
            musteri_id,
            miktar_kg,
            kg_fiyat,
            aciklama
        )

        if durum:
            QMessageBox.information(self, "Başarılı", mesaj)
            self.miktar_input.clear()
            self.kg_fiyat_input.clear()
            self.aciklama_input.clear()
            self.bugday_giris_listele()
        else:
            QMessageBox.warning(self, "Hata", mesaj)

    def bugday_giris_listele(self):
        bugday_girisleri = self.bugday_service.bugday_giris_listele()

        self.table.setRowCount(len(bugday_girisleri))

        for row_index, row_data in enumerate(bugday_girisleri):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))