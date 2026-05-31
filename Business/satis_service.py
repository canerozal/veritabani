from DataAccess.satis_dal import SatisDAL


class SatisService:
    def __init__(self):
        self.satis_dal = SatisDAL()

    def satis_ekle(self, musteri_id, aciklama):
        if musteri_id is None:
            return False, "Lütfen müşteri seçiniz."

        sonuc = self.satis_dal.satis_ekle(musteri_id, aciklama)

        if sonuc:
            return True, "Satış kaydı başarıyla oluşturuldu."
        else:
            return False, "Satış kaydı oluşturulurken hata oluştu."

    def satis_listele(self):
        return self.satis_dal.satis_listele()

    def satis_detay_ekle(self, satis_id, urun_id, miktar, birim_fiyat):
        if satis_id is None:
            return False, "Lütfen satış seçiniz."

        if urun_id is None:
            return False, "Lütfen ürün seçiniz."

        try:
            miktar = float(miktar)
            birim_fiyat = float(birim_fiyat)
        except ValueError:
            return False, "Miktar ve birim fiyat sayısal olmalıdır."

        if miktar <= 0:
            return False, "Miktar 0'dan büyük olmalıdır."

        if birim_fiyat < 0:
            return False, "Birim fiyat negatif olamaz."

        sonuc = self.satis_dal.satis_detay_ekle(
            satis_id,
            urun_id,
            miktar,
            birim_fiyat
        )

        if sonuc:
            return True, "Satış detayı başarıyla eklendi."
        else:
            return False, "Satış detayı eklenirken hata oluştu."

    def satis_detay_listele(self):
        return self.satis_dal.satis_detay_listele()

    def musteri_listele(self):
        return self.satis_dal.musteri_listele()

    def urun_listele(self):
        return self.satis_dal.urun_listele()