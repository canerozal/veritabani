from DataAccess.db import Database


class BugdayDAL:
    def __init__(self):
        self.db = Database()

    def bugday_giris_ekle(self, musteri_id, miktar_kg, kg_fiyat, aciklama):
        connection = self.db.connect()

        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_bugday_giris_ekle", [
                musteri_id,
                miktar_kg,
                kg_fiyat,
                aciklama
            ])

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            print("Buğday girişi ekleme hatası:", e)
            return False

    def bugday_giris_listele(self):
        connection = self.db.connect()

        if connection is None:
            return []

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_bugday_giris_listele")

            result = []

            for stored_result in cursor.stored_results():
                result = stored_result.fetchall()

            cursor.close()
            connection.close()
            return result

        except Exception as e:
            print("Buğday girişi listeleme hatası:", e)
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