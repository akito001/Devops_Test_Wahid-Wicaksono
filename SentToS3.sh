#!/bin/bash

# Direktori lokal tempat file log disimpan
local_log_directory="/var/log/app_1"

# Nama bucket S3
s3_bucket="s3://application-log"

# Membuat array dari file-file log yang ada di direktori lokal
log_files=($(ls -t "$local_log_directory/application-"*".log"))

# Memeriksa apakah ada file log yang tersedia
if [ ${#log_files[@]} -gt 0 ]; then
    # Mengambil file log terbaru
    latest_log="${log_files[0]}"

    # Ekstrak tanggal dari nama file
    date_str=$(echo "$latest_log" | grep -oP '\d{8}')
    date_format=$(date -d "$date_str" +%Y%m%d)

    # Mengirim file log ke Amazon S3
    aws s3 cp "$local_log_directory/$latest_log" "$s3_bucket/"

    # Memeriksa apakah pengiriman berhasil
    if [ $? -eq 0 ]; then
        echo "File log $latest_log berhasil dikirim ke $s3_bucket"
        
        # Menghapus file log lokal setelah berhasil dikirim
        rm "$local_log_directory/$latest_log"
        echo "File log $latest_log dihapus dari lokal"
    else
        echo "Gagal mengirim file log $latest_log ke $s3_bucket"
    fi
else
    echo "Tidak ada file log yang tersedia untuk dikirim."
fi
