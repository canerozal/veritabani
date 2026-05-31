from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox
)

from Business.urun_service import UrunService


class UrunForm(QWidget):
    def __init__(self):
        super().__init__()

        self.urun_service = UrunService()

        self.setWindowTitle("Ürün İşlemleri")
        self.setGeometry(350, 220, 850, 500)

        self.urun_adi_input = QLineEdit()

        self.birim_combo = QComboBox()
        self.birim_combo.addItems(["KG", "Cuval", "Adet"])

        self.stok_input = QLineEdit()
        self.alis_fiyati_input = QLineEdit()
        self.satis_fiyati_input = QLineEdit()

        self.kaydet_button = QPushButton("Ürün Ekle")
        self.listele_button = QPushButton("Ürünleri Listele")

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ürün Adı", "Birim", "Stok", "Alış Fiyatı", "Satış Fiyatı", "Aktif Mi"
        ])

        self.kaydet_button.clicked.connect(self.urun_ekle)
        self.listele_button.clicked.connect(self.urunleri_listele)

        form_layout = QVBoxLayout()

        form_layout.addWidget(QLabel("Ürün Adı:"))
        form_layout.addWidget(self.urun_adi_input)

        form_layout.addWidget(QLabel("Birim:"))
        form_layout.addWidget(self.birim_combo)

        form_layout.addWidget(QLabel("Stok Miktarı:"))
        form_layout.addWidget(self.stok_input)

        form_layout.addWidget(QLabel("Alış Fiyatı:"))
        form_layout.addWidget(self.alis_fiyati_input)

        form_layout.addWidget(QLabel("Satış Fiyatı:"))
        form_layout.addWidget(self.satis_fiyati_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.kaydet_button)
        button_layout.addWidget(self.listele_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def urun_ekle(self):
        urun_adi = self.urun_adi_input.text()
        birim = self.birim_combo.currentText()
        stok = self.stok_input.text()
        alis_fiyati = self.alis_fiyati_input.text()
        satis_fiyati = self.satis_fiyati_input.text()

        durum, mesaj = self.urun_service.urun_ekle(
            urun_adi,
            birim,
            stok,
            alis_fiyati,
            satis_fiyati
        )

        if durum:
            QMessageBox.information(self, "Başarılı", mesaj)

            self.urun_adi_input.clear()
            self.stok_input.clear()
            self.alis_fiyati_input.clear()
            self.satis_fiyati_input.clear()

            self.urunleri_listele()
        else:
            QMessageBox.warning(self, "Hata", mesaj)

    def urunleri_listele(self):
        urunler = self.urun_service.urun_listele()

        self.table.setRowCount(len(urunler))

        for row_index, row_data in enumerate(urunler):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))