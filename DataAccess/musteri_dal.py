from DataAccess.db import Database


class MusteriDAL:
    def __init__(self):
        self.db = Database()

    def musteri_ekle(self, ad, soyad, telefon, adres):
        connection = self.db.connect()

        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_musteri_ekle", [ad, soyad, telefon, adres])
            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            print("Müşteri ekleme hatası:", e)
            return False

    def musteri_listele(self):
        connection = self.db.connect()

        if connection is None:
            return []

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_musteri_listele")

            result = []

            for stored_result in cursor.stored_results():
                result = stored_result.fetchall()

            cursor.close()
            connection.close()
            return result

        except Exception as e:
            print("Müşteri listeleme hatası:", e)
            return []