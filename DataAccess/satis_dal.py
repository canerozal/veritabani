from DataAccess.db import Database


class SatisDAL:
    def __init__(self):
        self.db = Database()

    def satis_ekle(self, musteri_id, aciklama):
        connection = self.db.connect()

        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_satis_ekle", [
                musteri_id,
                aciklama
            ])

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            print("Satış ekleme hatası:", e)
            return False

    def satis_listele(self):
        connection = self.db.connect()

        if connection is None:
            return []

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_satis_listele")

            result = []

            for stored_result in cursor.stored_results():
                result = stored_result.fetchall()

            cursor.close()
            connection.close()
            return result

        except Exception as e:
            print("Satış listeleme hatası:", e)
            return []

    def satis_detay_ekle(self, satis_id, urun_id, miktar, birim_fiyat):
        connection = self.db.connect()

        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_satis_detay_ekle", [
                satis_id,
                urun_id,
                miktar,
                birim_fiyat
            ])

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            print("Satış detayı ekleme hatası:", e)
            return False

    def satis_detay_listele(self):
        connection = self.db.connect()

        if connection is None:
            return []

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_satis_detay_listele")

            result = []

            for stored_result in cursor.stored_results():
                result = stored_result.fetchall()

            cursor.close()
            connection.close()
            return result

        except Exception as e:
            print("Satış detayı listeleme hatası:", e)
            return []

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

    def urun_listele(self):
        connection = self.db.connect()

        if connection is None:
            return []

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_urun_listele")

            result = []

            for stored_result in cursor.stored_results():
                result = stored_result.fetchall()

            cursor.close()
            connection.close()
            return result

        except Exception as e:
            print("Ürün listeleme hatası:", e)
            return []