from DataAccess.urun_dal import UrunDAL


class UrunService:
    def __init__(self):
        self.urun_dal = UrunDAL()

    def urun_ekle(self, urun_adi, birim, stok_miktari, alis_fiyati, satis_fiyati):
        if urun_adi.strip() == "":
            return False, "Ürün adı boş bırakılamaz."

        if birim.strip() == "":
            return False, "Birim boş bırakılamaz."

        try:
            stok_miktari = float(stok_miktari)
            alis_fiyati = float(alis_fiyati)
            satis_fiyati = float(satis_fiyati)
        except ValueError:
            return False, "Stok, alış fiyatı ve satış fiyatı sayısal olmalıdır."

        if stok_miktari < 0:
            return False, "Stok miktarı negatif olamaz."

        if alis_fiyati < 0:
            return False, "Alış fiyatı negatif olamaz."

        if satis_fiyati < 0:
            return False, "Satış fiyatı negatif olamaz."

        sonuc = self.urun_dal.urun_ekle(
            urun_adi,
            birim,
            stok_miktari,
            alis_fiyati,
            satis_fiyati
        )

        if sonuc:
            return True, "Ürün başarıyla eklendi."
        else:
            return False, "Ürün eklenirken hata oluştu."

    def urun_listele(self):
        return self.urun_dal.urun_listele()