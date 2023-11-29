import os
import boto3
from datetime import datetime

# Direktori lokal tempat file log disimpan
local_log_directory = "/var/log/app_1"

# Nama bucket S3
s3_bucket = "application-log"

# Membuat daftar file-file log yang ada di direktori lokal
log_files = sorted(
    [f for f in os.listdir(local_log_directory) if f.startswith("application-") and f.endswith(".log")],
    key=lambda x: os.path.getmtime(os.path.join(local_log_directory, x)),
    reverse=True
)

# Memeriksa apakah ada file log yang tersedia
if log_files:
    # Mengambil file log terbaru
    latest_log = log_files[0]

    # Ekstrak tanggal dari nama file
    date_str = latest_log.split('-')[1].split('.')[0]
    date_format = datetime.strptime(date_str, "%Y%m%d").strftime("%Y%m%d")

    # Mengirim file log ke Amazon S3
    s3_client = boto3.client("s3")
    s3_key = f"{date_format}/{latest_log}"
    s3_client.upload_file(
        os.path.join(local_log_directory, latest_log),
        s3_bucket,
        s3_key
    )

    # Memeriksa apakah pengiriman berhasil
    print(f"File log {latest_log} berhasil dikirim ke s3://{s3_bucket}/{s3_key}")

    # Menghapus file log lokal setelah berhasil dikirim
    os.remove(os.path.join(local_log_directory, latest_log))
    print(f"File log {latest_log} dihapus dari lokal")
else:
    print("Tidak ada file log yang tersedia untuk dikirim.")
