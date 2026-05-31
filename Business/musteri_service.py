from DataAccess.musteri_dal import MusteriDAL


class MusteriService:
    def __init__(self):
        self.musteri_dal = MusteriDAL()

    def musteri_ekle(self, ad, soyad, telefon, adres):
        if ad.strip() == "":
            return False, "Müşteri adı boş bırakılamaz."

        if soyad.strip() == "":
            return False, "Müşteri soyadı boş bırakılamaz."

        if telefon.strip() == "":
            return False, "Telefon boş bırakılamaz."

        sonuc = self.musteri_dal.musteri_ekle(ad, soyad, telefon, adres)

        if sonuc:
            return True, "Müşteri başarıyla eklendi."
        else:
            return False, "Müşteri eklenirken hata oluştu."

    def musteri_listele(self):
        return self.musteri_dal.musteri_listele()