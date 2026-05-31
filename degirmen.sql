CREATE DATABASE IF NOT EXISTS degirmencilik_db;
USE degirmencilik_db;

CREATE TABLE deg_musteriler (
    musteri_id INT AUTO_INCREMENT PRIMARY KEY,
    musteri_ad VARCHAR(100) NOT NULL,
    musteri_soyad VARCHAR(100) NOT NULL,
    musteri_tel VARCHAR(25) UNIQUE,
    musteri_adres VARCHAR(250),
    kayit_tarihi DATE DEFAULT (CURRENT_DATE),
    aktif_mi TINYINT(1) DEFAULT 1,

    CHECK (aktif_mi IN (0,1))
);

CREATE TABLE deg_urunler (
    urun_id INT AUTO_INCREMENT PRIMARY KEY,
    urun_adi VARCHAR(100) NOT NULL UNIQUE,
    birim VARCHAR(20) NOT NULL,
    stok_miktari DECIMAL(10,2) DEFAULT 0,
    alis_fiyati DECIMAL(10,2) DEFAULT 0,
    satis_fiyati DECIMAL(10,2) NOT NULL,
    aktif_mi TINYINT(1) DEFAULT 1,

    CHECK (stok_miktari >= 0),
    CHECK (alis_fiyati >= 0),
    CHECK (satis_fiyati >= 0),
    CHECK (birim IN ('KG', 'Cuval', 'Adet')),
    CHECK (aktif_mi IN (0,1))
);

CREATE TABLE deg_bugday_girisleri (
    bugday_giris_id INT AUTO_INCREMENT PRIMARY KEY,
    musteri_id INT NOT NULL,
    miktar_kg DECIMAL(10,2) NOT NULL,
    kg_fiyat DECIMAL(10,2) NOT NULL,
    toplam_tutar DECIMAL(10,2) NOT NULL,
    giris_tarihi DATE DEFAULT (CURRENT_DATE),
    aciklama VARCHAR(250),

    CONSTRAINT fk_bugday_musteri
        FOREIGN KEY (musteri_id)
        REFERENCES deg_musteriler(musteri_id),

    CHECK (miktar_kg > 0),
    CHECK (kg_fiyat >= 0),
    CHECK (toplam_tutar >= 0)
);

CREATE TABLE deg_satislar (
    satis_id INT AUTO_INCREMENT PRIMARY KEY,
    musteri_id INT NOT NULL,
    satis_tarihi DATE DEFAULT (CURRENT_DATE),
    toplam_tutar DECIMAL(10,2) DEFAULT 0,
    aciklama VARCHAR(250),

    CONSTRAINT fk_satis_musteri
        FOREIGN KEY (musteri_id)
        REFERENCES deg_musteriler(musteri_id),

    CHECK (toplam_tutar >= 0)
);

CREATE TABLE deg_satis_detaylari (
    satis_detay_id INT AUTO_INCREMENT PRIMARY KEY,
    satis_id INT NOT NULL,
    urun_id INT NOT NULL,
    miktar DECIMAL(10,2) NOT NULL,
    birim_fiyat DECIMAL(10,2) NOT NULL,
    ara_toplam DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_detay_satis
        FOREIGN KEY (satis_id)
        REFERENCES deg_satislar(satis_id),

    CONSTRAINT fk_detay_urun
        FOREIGN KEY (urun_id)
        REFERENCES deg_urunler(urun_id),

    CHECK (miktar > 0),
    CHECK (birim_fiyat >= 0),
    CHECK (ara_toplam >= 0)
);

CREATE TABLE deg_odemeler (
    odeme_id INT AUTO_INCREMENT PRIMARY KEY,
    musteri_id INT NOT NULL,
    odeme_turu VARCHAR(50) NOT NULL,
    tutar DECIMAL(10,2) NOT NULL,
    odeme_tarihi DATE DEFAULT (CURRENT_DATE),
    aciklama VARCHAR(250),

    CONSTRAINT fk_odeme_musteri
        FOREIGN KEY (musteri_id)
        REFERENCES deg_musteriler(musteri_id),

    CHECK (tutar > 0),
    CHECK (odeme_turu IN ('Nakit', 'Kredi Karti', 'Banka Odemesi'))
);

CREATE TABLE deg_cari_hareketler (
    cari_hareket_id INT AUTO_INCREMENT PRIMARY KEY,
    musteri_id INT NOT NULL,
    islem_tipi VARCHAR(50) NOT NULL,
    borc DECIMAL(10,2) DEFAULT 0,
    alacak DECIMAL(10,2) DEFAULT 0,
    islem_tarihi DATE DEFAULT (CURRENT_DATE),
    aciklama VARCHAR(250),

    CONSTRAINT fk_cari_musteri
        FOREIGN KEY (musteri_id)
        REFERENCES deg_musteriler(musteri_id),

    CHECK (borc >= 0),
    CHECK (alacak >= 0),
    CHECK (islem_tipi IN ('Bugday Girisi', 'Satis', 'Odeme'))
);

CREATE TABLE deg_kullanicilar (
    kullanici_id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_adi VARCHAR(100) NOT NULL UNIQUE,
    sifre VARCHAR(100) NOT NULL,
    ad_soyad VARCHAR(100) NOT NULL,
    rol VARCHAR(50) DEFAULT 'Personel',
    aktif_mi TINYINT(1) DEFAULT 1,

    CHECK (rol IN ('Yonetici', 'Personel')),
    CHECK (aktif_mi IN (0,1))
);

DELIMITER //

CREATE PROCEDURE sp_musteri_ekle(
    IN p_musteri_ad VARCHAR(100),
    IN p_musteri_soyad VARCHAR(100),
    IN p_musteri_tel VARCHAR(25),
    IN p_musteri_adres VARCHAR(250)
)
BEGIN
    INSERT INTO deg_musteriler
    (
        musteri_ad,
        musteri_soyad,
        musteri_tel,
        musteri_adres,
        kayit_tarihi,
        aktif_mi
    )
    VALUES
    (
        p_musteri_ad,
        p_musteri_soyad,
        p_musteri_tel,
        p_musteri_adres,
        CURRENT_DATE,
        1
    );
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_musteri_guncelle(
    IN p_musteri_id INT,
    IN p_musteri_ad VARCHAR(100),
    IN p_musteri_soyad VARCHAR(100),
    IN p_musteri_tel VARCHAR(25),
    IN p_musteri_adres VARCHAR(250),
    IN p_aktif_mi TINYINT
)
BEGIN
    UPDATE deg_musteriler
    SET
        musteri_ad = p_musteri_ad,
        musteri_soyad = p_musteri_soyad,
        musteri_tel = p_musteri_tel,
        musteri_adres = p_musteri_adres,
        aktif_mi = p_aktif_mi
    WHERE musteri_id = p_musteri_id;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_musteri_sil(
    IN p_musteri_id INT
)
BEGIN
    UPDATE deg_musteriler
    SET aktif_mi = 0
    WHERE musteri_id = p_musteri_id;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_musteri_listele()
BEGIN
    SELECT
        musteri_id,
        musteri_ad,
        musteri_soyad,
        musteri_tel,
        musteri_adres,
        kayit_tarihi,
        aktif_mi
    FROM deg_musteriler
    WHERE aktif_mi = 1;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_urun_ekle(
    IN p_urun_adi VARCHAR(100),
    IN p_birim VARCHAR(20),
    IN p_stok_miktari DECIMAL(10,2),
    IN p_alis_fiyati DECIMAL(10,2),
    IN p_satis_fiyati DECIMAL(10,2)
)
BEGIN
    INSERT INTO deg_urunler
    (
        urun_adi,
        birim,
        stok_miktari,
        alis_fiyati,
        satis_fiyati,
        aktif_mi
    )
    VALUES
    (
        p_urun_adi,
        p_birim,
        p_stok_miktari,
        p_alis_fiyati,
        p_satis_fiyati,
        1
    );
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_urun_guncelle(
    IN p_urun_id INT,
    IN p_urun_adi VARCHAR(100),
    IN p_birim VARCHAR(20),
    IN p_stok_miktari DECIMAL(10,2),
    IN p_alis_fiyati DECIMAL(10,2),
    IN p_satis_fiyati DECIMAL(10,2),
    IN p_aktif_mi TINYINT
)
BEGIN
    UPDATE deg_urunler
    SET
        urun_adi = p_urun_adi,
        birim = p_birim,
        stok_miktari = p_stok_miktari,
        alis_fiyati = p_alis_fiyati,
        satis_fiyati = p_satis_fiyati,
        aktif_mi = p_aktif_mi
    WHERE urun_id = p_urun_id;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_urun_sil(
    IN p_urun_id INT
)
BEGIN
    UPDATE deg_urunler
    SET aktif_mi = 0
    WHERE urun_id = p_urun_id;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_urun_sil(
    IN p_urun_id INT
)
BEGIN
    UPDATE deg_urunler
    SET aktif_mi = 0
    WHERE urun_id = p_urun_id;
END //

DELIMITER ;

DELIMITER //

DELIMITER //

CREATE PROCEDURE sp_urun_listele()
BEGIN
    SELECT
        urun_id,
        urun_adi,
        birim,
        stok_miktari,
        alis_fiyati,
        satis_fiyati,
        aktif_mi
    FROM deg_urunler
    WHERE aktif_mi = 1;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_bugday_giris_ekle;

DELIMITER //

CREATE PROCEDURE sp_bugday_giris_ekle(
    IN p_musteri_id INT,
    IN p_miktar_kg DECIMAL(10,2),
    IN p_kg_fiyat DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    INSERT INTO deg_bugday_girisleri
    (
        musteri_id,
        miktar_kg,
        kg_fiyat,
        toplam_tutar,
        giris_tarihi,
        aciklama
    )
    VALUES
    (
        p_musteri_id,
        p_miktar_kg,
        p_kg_fiyat,
        p_miktar_kg * p_kg_fiyat,
        CURRENT_DATE,
        p_aciklama
    );
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_bugday_giris_guncelle;

DELIMITER //

CREATE PROCEDURE sp_bugday_giris_guncelle(
    IN p_bugday_giris_id INT,
    IN p_musteri_id INT,
    IN p_miktar_kg DECIMAL(10,2),
    IN p_kg_fiyat DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    UPDATE deg_bugday_girisleri
    SET
        musteri_id = p_musteri_id,
        miktar_kg = p_miktar_kg,
        kg_fiyat = p_kg_fiyat,
        toplam_tutar = p_miktar_kg * p_kg_fiyat,
        aciklama = p_aciklama
    WHERE bugday_giris_id = p_bugday_giris_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_bugday_giris_sil;

DELIMITER //

CREATE PROCEDURE sp_bugday_giris_sil(
    IN p_bugday_giris_id INT
)
BEGIN
    DELETE FROM deg_bugday_girisleri
    WHERE bugday_giris_id = p_bugday_giris_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_bugday_giris_listele;

DELIMITER //

CREATE PROCEDURE sp_bugday_giris_listele()
BEGIN
    SELECT
        bg.bugday_giris_id,
        bg.musteri_id,
        m.musteri_ad,
        m.musteri_soyad,
        bg.miktar_kg,
        bg.kg_fiyat,
        bg.toplam_tutar,
        bg.giris_tarihi,
        bg.aciklama
    FROM deg_bugday_girisleri bg
    INNER JOIN deg_musteriler m ON bg.musteri_id = m.musteri_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_ekle;

DELIMITER //

CREATE PROCEDURE sp_satis_ekle(
    IN p_musteri_id INT,
    IN p_aciklama VARCHAR(250)
)
BEGIN
    INSERT INTO deg_satislar
    (
        musteri_id,
        satis_tarihi,
        toplam_tutar,
        aciklama
    )
    VALUES
    (
        p_musteri_id,
        CURRENT_DATE,
        0,
        p_aciklama
    );
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_guncelle;

DELIMITER //

CREATE PROCEDURE sp_satis_guncelle(
    IN p_satis_id INT,
    IN p_musteri_id INT,
    IN p_toplam_tutar DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    UPDATE deg_satislar
    SET
        musteri_id = p_musteri_id,
        toplam_tutar = p_toplam_tutar,
        aciklama = p_aciklama
    WHERE satis_id = p_satis_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_sil;

DELIMITER //

CREATE PROCEDURE sp_satis_sil(
    IN p_satis_id INT
)
BEGIN
    DELETE FROM deg_satislar
    WHERE satis_id = p_satis_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_listele;

DELIMITER //

CREATE PROCEDURE sp_satis_listele()
BEGIN
    SELECT
        s.satis_id,
        s.musteri_id,
        m.musteri_ad,
        m.musteri_soyad,
        s.satis_tarihi,
        s.toplam_tutar,
        s.aciklama
    FROM deg_satislar s
    INNER JOIN deg_musteriler m ON s.musteri_id = m.musteri_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_detay_ekle;

DELIMITER //

CREATE PROCEDURE sp_satis_detay_ekle(
    IN p_satis_id INT,
    IN p_urun_id INT,
    IN p_miktar DECIMAL(10,2),
    IN p_birim_fiyat DECIMAL(10,2)
)
BEGIN
    INSERT INTO deg_satis_detaylari
    (
        satis_id,
        urun_id,
        miktar,
        birim_fiyat,
        ara_toplam
    )
    VALUES
    (
        p_satis_id,
        p_urun_id,
        p_miktar,
        p_birim_fiyat,
        p_miktar * p_birim_fiyat
    );
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_detay_guncelle;

DELIMITER //

CREATE PROCEDURE sp_satis_detay_guncelle(
    IN p_satis_detay_id INT,
    IN p_satis_id INT,
    IN p_urun_id INT,
    IN p_miktar DECIMAL(10,2),
    IN p_birim_fiyat DECIMAL(10,2)
)
BEGIN
    UPDATE deg_satis_detaylari
    SET
        satis_id = p_satis_id,
        urun_id = p_urun_id,
        miktar = p_miktar,
        birim_fiyat = p_birim_fiyat,
        ara_toplam = p_miktar * p_birim_fiyat
    WHERE satis_detay_id = p_satis_detay_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_detay_sil;

DELIMITER //

CREATE PROCEDURE sp_satis_detay_sil(
    IN p_satis_detay_id INT
)
BEGIN
    DELETE FROM deg_satis_detaylari
    WHERE satis_detay_id = p_satis_detay_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_satis_detay_listele;

DELIMITER //

CREATE PROCEDURE sp_satis_detay_listele()
BEGIN
    SELECT
        sd.satis_detay_id,
        sd.satis_id,
        sd.urun_id,
        u.urun_adi,
        sd.miktar,
        sd.birim_fiyat,
        sd.ara_toplam
    FROM deg_satis_detaylari sd
    INNER JOIN deg_urunler u ON sd.urun_id = u.urun_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_odeme_ekle;

DELIMITER //

CREATE PROCEDURE sp_odeme_ekle(
    IN p_musteri_id INT,
    IN p_odeme_turu VARCHAR(50),
    IN p_tutar DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    INSERT INTO deg_odemeler
    (
        musteri_id,
        odeme_turu,
        tutar,
        odeme_tarihi,
        aciklama
    )
    VALUES
    (
        p_musteri_id,
        p_odeme_turu,
        p_tutar,
        CURRENT_DATE,
        p_aciklama
    );
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_odeme_guncelle;

DELIMITER //

CREATE PROCEDURE sp_odeme_guncelle(
    IN p_odeme_id INT,
    IN p_musteri_id INT,
    IN p_odeme_turu VARCHAR(50),
    IN p_tutar DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    UPDATE deg_odemeler
    SET
        musteri_id = p_musteri_id,
        odeme_turu = p_odeme_turu,
        tutar = p_tutar,
        aciklama = p_aciklama
    WHERE odeme_id = p_odeme_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_odeme_sil;

DELIMITER //

CREATE PROCEDURE sp_odeme_sil(
    IN p_odeme_id INT
)
BEGIN
    DELETE FROM deg_odemeler
    WHERE odeme_id = p_odeme_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_odeme_sil;

DELIMITER //

CREATE PROCEDURE sp_odeme_sil(
    IN p_odeme_id INT
)
BEGIN
    DELETE FROM deg_odemeler
    WHERE odeme_id = p_odeme_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_odeme_listele;

DELIMITER //

CREATE PROCEDURE sp_odeme_listele()
BEGIN
    SELECT
        o.odeme_id,
        o.musteri_id,
        m.musteri_ad,
        m.musteri_soyad,
        o.odeme_turu,
        o.tutar,
        o.odeme_tarihi,
        o.aciklama
    FROM deg_odemeler o
    INNER JOIN deg_musteriler m ON o.musteri_id = m.musteri_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_cari_hareket_ekle;

DELIMITER //

CREATE PROCEDURE sp_cari_hareket_ekle(
    IN p_musteri_id INT,
    IN p_islem_tipi VARCHAR(50),
    IN p_borc DECIMAL(10,2),
    IN p_alacak DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    INSERT INTO deg_cari_hareketler
    (
        musteri_id,
        islem_tipi,
        borc,
        alacak,
        islem_tarihi,
        aciklama
    )
    VALUES
    (
        p_musteri_id,
        p_islem_tipi,
        p_borc,
        p_alacak,
        CURRENT_DATE,
        p_aciklama
    );
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_cari_hareket_guncelle;

DELIMITER //

CREATE PROCEDURE sp_cari_hareket_guncelle(
    IN p_cari_hareket_id INT,
    IN p_musteri_id INT,
    IN p_islem_tipi VARCHAR(50),
    IN p_borc DECIMAL(10,2),
    IN p_alacak DECIMAL(10,2),
    IN p_aciklama VARCHAR(250)
)
BEGIN
    UPDATE deg_cari_hareketler
    SET
        musteri_id = p_musteri_id,
        islem_tipi = p_islem_tipi,
        borc = p_borc,
        alacak = p_alacak,
        aciklama = p_aciklama
    WHERE cari_hareket_id = p_cari_hareket_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_cari_hareket_sil;

DELIMITER //

CREATE PROCEDURE sp_cari_hareket_sil(
    IN p_cari_hareket_id INT
)
BEGIN
    DELETE FROM deg_cari_hareketler
    WHERE cari_hareket_id = p_cari_hareket_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_cari_hareket_listele;

DELIMITER //

CREATE PROCEDURE sp_cari_hareket_listele()
BEGIN
    SELECT
        ch.cari_hareket_id,
        ch.musteri_id,
        m.musteri_ad,
        m.musteri_soyad,
        ch.islem_tipi,
        ch.borc,
        ch.alacak,
        ch.islem_tarihi,
        ch.aciklama
    FROM deg_cari_hareketler ch
    INNER JOIN deg_musteriler m ON ch.musteri_id = m.musteri_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_kullanici_ekle;

DELIMITER //

CREATE PROCEDURE sp_kullanici_ekle(
    IN p_kullanici_adi VARCHAR(100),
    IN p_sifre VARCHAR(100),
    IN p_ad_soyad VARCHAR(100),
    IN p_rol VARCHAR(50)
)
BEGIN
    INSERT INTO deg_kullanicilar
    (
        kullanici_adi,
        sifre,
        ad_soyad,
        rol,
        aktif_mi
    )
    VALUES
    (
        p_kullanici_adi,
        p_sifre,
        p_ad_soyad,
        p_rol,
        1
    );
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_kullanici_guncelle;

DELIMITER //

CREATE PROCEDURE sp_kullanici_guncelle(
    IN p_kullanici_id INT,
    IN p_kullanici_adi VARCHAR(100),
    IN p_sifre VARCHAR(100),
    IN p_ad_soyad VARCHAR(100),
    IN p_rol VARCHAR(50),
    IN p_aktif_mi TINYINT
)
BEGIN
    UPDATE deg_kullanicilar
    SET
        kullanici_adi = p_kullanici_adi,
        sifre = p_sifre,
        ad_soyad = p_ad_soyad,
        rol = p_rol,
        aktif_mi = p_aktif_mi
    WHERE kullanici_id = p_kullanici_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_kullanici_sil;

DELIMITER //

CREATE PROCEDURE sp_kullanici_sil(
    IN p_kullanici_id INT
)
BEGIN
    UPDATE deg_kullanicilar
    SET aktif_mi = 0
    WHERE kullanici_id = p_kullanici_id;
END //

DELIMITER ;

USE degirmencilik_db;

DROP PROCEDURE IF EXISTS sp_kullanici_listele;

DELIMITER //

CREATE PROCEDURE sp_kullanici_listele()
BEGIN
    SELECT
        kullanici_id,
        kullanici_adi,
        sifre,
        ad_soyad,
        rol,
        aktif_mi
    FROM deg_kullanicilar
    WHERE aktif_mi = 1;
END //

DELIMITER ;

USE degirmencilik_db;

DROP FUNCTION IF EXISTS fn_bugday_tutar_hesapla;

DELIMITER //

CREATE FUNCTION fn_bugday_tutar_hesapla(
    p_miktar_kg DECIMAL(10,2),
    p_kg_fiyat DECIMAL(10,2)
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_toplam_tutar DECIMAL(10,2);

    SET v_toplam_tutar = p_miktar_kg * p_kg_fiyat;

    RETURN v_toplam_tutar;
END //

DELIMITER ;

USE degirmencilik_db;

DROP FUNCTION IF EXISTS fn_musteri_bakiye_hesapla;

DELIMITER //

CREATE FUNCTION fn_musteri_bakiye_hesapla(
    p_musteri_id INT
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_bakiye DECIMAL(10,2);

    SELECT 
        IFNULL(SUM(alacak), 0) - IFNULL(SUM(borc), 0)
    INTO v_bakiye
    FROM deg_cari_hareketler
    WHERE musteri_id = p_musteri_id;

    RETURN v_bakiye;
END //

DELIMITER ;

