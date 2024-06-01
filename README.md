# Task Reminder

Task Reminder adalah aplikasi manajemen tugas yang membantu pengguna untuk mengatur, melacak, dan mendapatkan pengingat untuk tugas-tugas pribadi mereka. Aplikasi ini dibangun menggunakan PyQt6 untuk antarmuka pengguna dan Plyer untuk menampilkan notifikasi.

## Fitur

- **Tambah Tugas**: Pengguna dapat menambahkan tugas dengan nama, tanggal, dan waktu pengingat.
- **Lihat Tugas**: Daftar tugas yang sudah ditambahkan dapat dilihat dalam tabel.
- **Pengingat Tugas**: Aplikasi akan menampilkan notifikasi saat waktu pengingat tugas tiba.
- **Kategori dan Prioritas**: Tugas dapat dikategorikan dan diberi prioritas (Low, Medium, High).

## Instalasi

### Prasyarat

- Python 3.7 atau lebih baru
- PyQt6
- Plyer

### Langkah Instalasi

1. Clone repositori ini
   ```
   git clone https://github.com/username/task-reminder-and-management.git
   cd task-reminder-and-management
   ```

2. Buat lingkungan virtual
  ```
  python -m venv venv
  source venv/bin/activate # Untuk pengguna Unix
  venv\Scripts\activate # Untuk pengguna Windows
  ```

## Penggunaan

1. Menambahkan Tugas
![Screenshot (264)](https://github.com/hariexe/Task-Reminder/assets/70479011/a1360e2c-a0e5-47d4-8cb4-c79e2e8f2d7d)
Klik tombol "Add Task".

![image](https://github.com/hariexe/Task-Reminder/assets/70479011/787c8fbd-6b95-4031-8cc7-0de7c4d9685a)
Masukkan nama tugas, tanggal dan waktu pengingat.
Centang kotak "Enable Notification" untuk mengaktifkan pengingat.
Klik "Add Task".

2. Melihat Tugas
Tugas yang telah ditambahkan akan muncul dalam tabel tugas pribadi.
![image](https://github.com/hariexe/Task-Reminder/assets/70479011/9e909069-5b20-426a-9071-c6257f6b15d4)

3. Mendapatkan Pengingat
Aplikasi akan menampilkan notifikasi saat waktu pengingat tugas tiba, jika notifikasi diaktifkan.

> [!IMPORTANT]
> Langkah-langkah deployment tidak perlu dilakukan jika mengunduh semua file yang ada di repositori karena sudah dicompile

## Deployment
Untuk men-deploy aplikasi ini menjadi file executable (.exe), Anda bisa menggunakan pyinstaller.

1. Install PyInstaller
```pip install pyinstaller```
2. Buat file executable
```pyinstaller --onefile --windowed main.py```
File executable akan berada di folder dist.

> [!WARNING]
Pastikan izin firewall dan pengaturan notifikasi di sistem Anda sudah sesuai untuk memungkinkan aplikasi menampilkan notifikasi.

## Lisensi
Proyek ini dilisensikan di bawah lisensi MIT - lihat file LICENSE untuk detail lebih lanjut.

## Kontak
Untuk pertanyaan lebih lanjut, Anda dapat menghubungi kami di alghuroba313@protonmail.com.
