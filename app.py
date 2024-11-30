import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from twilio.rest import Client

# Konfigurasi Logging
log_file = "monitoring_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Konfigurasi Twilio
TWILIO_SID = 'Isi Twilio SID'
AUTH_TOKEN = 'isi Auth_token Twilio'
TWILIO_WHATSAPP_NUMBER = 'whatsapp: Twilio Number'

# Fungsi untuk mengirim pesan WhatsApp
def send_whatsapp_message(action, file_name, whatsapp_penerima):
    try:
        client = Client(TWILIO_SID, AUTH_TOKEN)

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=f"Notifikasi: File '{file_name}' telah {action} pada folder yang dipantau.",
            to=f'whatsapp:+{whatsapp_penerima}'
        )

        log_message = f"Pesan WhatsApp berhasil terkirim: File '{file_name}' telah {action}. SID: {message.sid}"
        print(log_message)
        logging.info(log_message)  # menyimpan ke log
    except Exception as e:
        error_message = f"Gagal mengirim pesan WhatsApp: {e}"
        print(error_message)
        logging.error(error_message)  # menyimpan ke log

# Fungsi untuk memonitor folder
class MonitorFolder(FileSystemEventHandler):
    def __init__(self, whatsapp_penerima):
        self.whatsapp_penerima = whatsapp_penerima

    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            log_message = f"File baru ditambahkan: {file_name}"
            print(log_message)
            logging.info(log_message)
            send_whatsapp_message("ditambahkan dengan paste", file_name, self.whatsapp_penerima)

    def on_deleted(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            log_message = f"File telah dihapus: {file_name}"
            print(log_message)
            logging.info(log_message)
            send_whatsapp_message("dihapus", file_name, self.whatsapp_penerima)

# Fungsi untuk memantau folder
def monitor_folder(folder_path, whatsapp_penerima):
    if not os.path.exists(folder_path):
        print(f"Path folder '{folder_path}' tidak ditemukan. Mohon periksa kembali.")
        logging.error(f"Path folder '{folder_path}' tidak ditemukan.")
        return

    event_handler = MonitorFolder(whatsapp_penerima)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    log_message = f"Memantau folder: {folder_path}"
    print(log_message)
    logging.info(log_message)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Penghentian monitor folder oleh pengguna.")
        logging.info("Monitor folder dihentikan oleh pengguna.")
        observer.stop()
    observer.join()

# Fungsi utama untuk menjalankan program
if __name__ == "__main__":
    folder_path = input("Masukkan path folder yang akan dipantau: ").strip()
    whatsapp_penerima = input("Masukkan nomor WhatsApp penerima 0851: ").strip()

    # Validasi input nomor WhatsApp

    monitor_folder(folder_path, whatsapp_penerima)
