from DataAccess.db import Database


class UrunDAL:
    def __init__(self):
        self.db = Database()

    def urun_ekle(self, urun_adi, birim, stok_miktari, alis_fiyati, satis_fiyati):
        connection = self.db.connect()

        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.callproc("sp_urun_ekle", [
                urun_adi,
                birim,
                stok_miktari,
                alis_fiyati,
                satis_fiyati
            ])

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Exception as e:
            print("Ürün ekleme hatası:", e)
            return False

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