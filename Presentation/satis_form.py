from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox
)

from Business.satis_service import SatisService


class SatisForm(QWidget):
    def __init__(self):
        super().__init__()

        self.satis_service = SatisService()

        self.setWindowTitle("Satış İşlemleri")
        self.setGeometry(250, 150, 1050, 650)

        self.musteri_combo = QComboBox()
        self.urun_combo = QComboBox()
        self.satis_combo = QComboBox()

        self.satis_aciklama_input = QLineEdit()
        self.miktar_input = QLineEdit()
        self.birim_fiyat_input = QLineEdit()

        self.satis_olustur_button = QPushButton("Satış Oluştur")
        self.detay_ekle_button = QPushButton("Satış Detayı Ekle")
        self.satis_listele_button = QPushButton("Satışları Listele")
        self.detay_listele_button = QPushButton("Satış Detaylarını Listele")

        self.satis_table = QTableWidget()
        self.satis_table.setColumnCount(7)
        self.satis_table.setHorizontalHeaderLabels([
            "Satış ID", "Müşteri ID", "Ad", "Soyad", "Satış Tarihi", "Toplam Tutar", "Açıklama"
        ])

        self.detay_table = QTableWidget()
        self.detay_table.setColumnCount(7)
        self.detay_table.setHorizontalHeaderLabels([
            "Detay ID", "Satış ID", "Ürün ID", "Ürün Adı", "Miktar", "Birim Fiyat", "Ara Toplam"
        ])

        self.satis_olustur_button.clicked.connect(self.satis_olustur)
        self.detay_ekle_button.clicked.connect(self.satis_detay_ekle)
        self.satis_listele_button.clicked.connect(self.satislari_listele)
        self.detay_listele_button.clicked.connect(self.satis_detaylari_listele)

        main_layout = QVBoxLayout()

        satis_layout = QVBoxLayout()
        satis_layout.addWidget(QLabel("Müşteri:"))
        satis_layout.addWidget(self.musteri_combo)
        satis_layout.addWidget(QLabel("Satış Açıklama:"))
        satis_layout.addWidget(self.satis_aciklama_input)
        satis_layout.addWidget(self.satis_olustur_button)

        detay_layout = QVBoxLayout()
        detay_layout.addWidget(QLabel("Satış Seç:"))
        detay_layout.addWidget(self.satis_combo)
        detay_layout.addWidget(QLabel("Ürün Seç:"))
        detay_layout.addWidget(self.urun_combo)
        detay_layout.addWidget(QLabel("Miktar:"))
        detay_layout.addWidget(self.miktar_input)
        detay_layout.addWidget(QLabel("Birim Fiyat:"))
        detay_layout.addWidget(self.birim_fiyat_input)
        detay_layout.addWidget(self.detay_ekle_button)

        top_layout = QHBoxLayout()
        top_layout.addLayout(satis_layout)
        top_layout.addLayout(detay_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.satis_listele_button)
        button_layout.addWidget(self.detay_listele_button)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)

        main_layout.addWidget(QLabel("Satışlar"))
        main_layout.addWidget(self.satis_table)

        main_layout.addWidget(QLabel("Satış Detayları"))
        main_layout.addWidget(self.detay_table)

        self.setLayout(main_layout)

        self.musterileri_yukle()
        self.urunleri_yukle()
        self.satislari_listele()
        self.satis_detaylari_listele()

    def musterileri_yukle(self):
        self.musteri_combo.clear()
        musteriler = self.satis_service.musteri_listele()

        for musteri in musteriler:
            musteri_id = musteri[0]
            ad = musteri[1]
            soyad = musteri[2]

            self.musteri_combo.addItem(f"{musteri_id} - {ad} {soyad}", musteri_id)

    def urunleri_yukle(self):
        self.urun_combo.clear()
        urunler = self.satis_service.urun_listele()

        for urun in urunler:
            urun_id = urun[0]
            urun_adi = urun[1]
            satis_fiyati = urun[5]

            self.urun_combo.addItem(f"{urun_id} - {urun_adi} ({satis_fiyati} TL)", urun_id)

    def satislari_combo_yukle(self):
        self.satis_combo.clear()
        satislar = self.satis_service.satis_listele()

        for satis in satislar:
            satis_id = satis[0]
            musteri_ad = satis[2]
            musteri_soyad = satis[3]

            self.satis_combo.addItem(f"{satis_id} - {musteri_ad} {musteri_soyad}", satis_id)

    def satis_olustur(self):
        if self.musteri_combo.count() == 0:
            QMessageBox.warning(self, "Hata", "Önce müşteri eklemelisiniz.")
            return

        musteri_id = self.musteri_combo.currentData()
        aciklama = self.satis_aciklama_input.text()

        durum, mesaj = self.satis_service.satis_ekle(musteri_id, aciklama)

        if durum:
            QMessageBox.information(self, "Başarılı", mesaj)
            self.satis_aciklama_input.clear()
            self.satislari_listele()
        else:
            QMessageBox.warning(self, "Hata", mesaj)

    def satis_detay_ekle(self):
        if self.satis_combo.count() == 0:
            QMessageBox.warning(self, "Hata", "Önce satış oluşturmalısınız.")
            return

        if self.urun_combo.count() == 0:
            QMessageBox.warning(self, "Hata", "Önce ürün eklemelisiniz.")
            return

        satis_id = self.satis_combo.currentData()
        urun_id = self.urun_combo.currentData()
        miktar = self.miktar_input.text()
        birim_fiyat = self.birim_fiyat_input.text()

        durum, mesaj = self.satis_service.satis_detay_ekle(
            satis_id,
            urun_id,
            miktar,
            birim_fiyat
        )

        if durum:
            QMessageBox.information(self, "Başarılı", mesaj)
            self.miktar_input.clear()
            self.birim_fiyat_input.clear()
            self.satis_detaylari_listele()
            self.satislari_listele()
        else:
            QMessageBox.warning(self, "Hata", mesaj)

    def satislari_listele(self):
        satislar = self.satis_service.satis_listele()

        self.satis_table.setRowCount(len(satislar))

        for row_index, row_data in enumerate(satislar):
            for column_index, data in enumerate(row_data):
                self.satis_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        self.satislari_combo_yukle()

    def satis_detaylari_listele(self):
        detaylar = self.satis_service.satis_detay_listele()

        self.detay_table.setRowCount(len(detaylar))

        for row_index, row_data in enumerate(detaylar):
            for column_index, data in enumerate(row_data):
                self.detay_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))