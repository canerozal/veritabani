from DataAccess.bugday_dal import BugdayDAL


class BugdayService:
    def __init__(self):
        self.bugday_dal = BugdayDAL()

    def bugday_giris_ekle(self, musteri_id, miktar_kg, kg_fiyat, aciklama):
        if musteri_id is None:
            return False, "Lütfen müşteri seçiniz."

        try:
            miktar_kg = float(miktar_kg)
            kg_fiyat = float(kg_fiyat)
        except ValueError:
            return False, "Miktar ve KG fiyatı sayısal olmalıdır."

        if miktar_kg <= 0:
            return False, "Buğday miktarı 0'dan büyük olmalıdır."

        if kg_fiyat < 0:
            return False, "KG fiyatı negatif olamaz."

        sonuc = self.bugday_dal.bugday_giris_ekle(
            musteri_id,
            miktar_kg,
            kg_fiyat,
            aciklama
        )

        if sonuc:
            return True, "Buğday girişi başarıyla eklendi."
        else:
            return False, "Buğday girişi eklenirken hata oluştu."

    def bugday_giris_listele(self):
        return self.bugday_dal.bugday_giris_listele()

    def musteri_listele(self):
        return self.bugday_dal.musteri_listele()