import time
import subprocess
import os

def jalankan_pipeline(batch_ke):
    print(f"\n=== Memulai Eksekusi Batch {batch_ke} ===")
    
    # 1. Jalankan script Scraping
    print("Menjalankan proses scraping...")
    scraping_dir = os.path.join("..", "..", "Data Scraping", "src")
    subprocess.run(["python", "scraper.py"], cwd=scraping_dir)
    
    # 2. Jalankan script Storing
    print("Menjalankan proses storing ke database...")
    subprocess.run(["python", "insert_to_dw.py"], cwd=".")
    
    print(f"=== Batch {batch_ke} Selesai! ===")

if __name__ == "__main__":
    # 1. Eksekusi Batch 1 Normal (Scraping + Storing)
    jalankan_pipeline(1)
    
    # 2. Waktu Sabotase
    print("\nMenunggu 2 menit untuk Batch 2...")
    time.sleep(120) 
    
    # 3. Eksekusi Batch 2 Khusus (Hanya Storing, TANPA Scraping) untuk keperluan uji coba otmated scheduling
    print("\n=== Memulai Eksekusi Batch 2 (Hanya Storing) ===")
    print("Menjalankan proses storing ke database...")
    subprocess.run(["python", "insert_to_dw.py"], cwd=".")
    print("=== Batch 2 Selesai! ===")