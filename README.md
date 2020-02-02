# Instagram-Posts-Crawler-Users-v1

Merupakan program yang berguna untuk mendapatkan dan mengolah konten post di Instagram menjadi Dataset.

# Tentang

   * Tujuan

     1. Menghasilkan Dataset Posts berupa username, caption, hashtag, likes, dan comments.

   - Cara Kerja

      1. Program ini akan mengambil followers dari akun pengguna program
      2. Kemudian akan dilanjutkan mengambil konten post dari setiap followers
      3. Setelah selesai, target selanjutnya akan dipilih dengan cara menargetkan yang memiliki followers terbanyak dari daftar followers   pertama
      4. Kembali ke langkah 1, tetapi dengan target yang sudah dipilih sebelumnya
      5. Program akan berhenti ketika koneksi tidak mendukung atau mencapai besar data yang ditentukan dalam format MB (MegaByte).
      6. Hasil berupa Dataset Posts dengan format CSV berupa username, caption, hashtag, likes, dan comments.

# Yang di Butuhkan

  - [x] Python 3.5+
  - [x] Koneksi yang Bagus
  - [x] Akun Instagram
  - [x] Library Python berupa: selenium, emoji, time, emoji, string, csv, os
  - [x] Chrome WebDriver

# Cara Penggunaan

   - Mengumpulkan Dataset Posts

   1. Unduh/clone repository ini.
   2. Install python dan library yang diperlukan. Untuk library dapat diinstall melalui cmd: pip install <nama library>
   3. Download Chrome WebDriver dan taruh file exe nya di folder yang sama dengan file ini.
   4. Jalankan script python crawl.py dengan mengklik 2x atau dengan command InstagramCrawler.py
   5. Isi input nama file akun dan username pertama yang ingin dipakai, kemudian masukan nama file sesuai keinginan
   6. Hasil terdapat di folder yang sama seperti penyimpan code InstagramCrawler.py

# Kontak

  - Muhammad Bagas Pradana - @bagas050201 - bagaspradana0201@gmail.com
  - Resa Fajar Sukma - @zeHapOs9875Ea - rezasukma96@gmail.com

Project Link: https://https://github.com/bagas050201/InstagramCrawler/
