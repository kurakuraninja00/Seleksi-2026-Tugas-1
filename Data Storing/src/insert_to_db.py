import json
import mysql.connector
from mysql.connector import Error

def insert_json_to_db():
    db_config = {
        'host': 'localhost',
        'user': 'root',      
        'password': '',      
        'database': 'billboard_db' # Langsung tembak ke database yang sudah dibuat
    }

    try:
        # 1. Buka Koneksi
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # 2. Baca file JSON 
        # =======artis========
        file_path = '../../Data Scraping/data/artists.json' 
        with open(file_path, 'r', encoding='utf-8') as file:
            artists_data = json.load(file)

        print(f"Berhasil membaca {len(artists_data)} data dari {file_path}")

        # =======songs========
        file_path = '../../Data Scraping/data/songs.json' 
        with open(file_path, 'r', encoding='utf-8') as file:
            songs_data = json.load(file)

        print(f"Berhasil membaca {len(songs_data)} data dari {file_path}")

        # =======charts========
        file_path = '../../Data Scraping/data/chart_rankings.json'  
        with open(file_path, 'r', encoding='utf-8') as file:
            charts_data = json.load(file)

        print(f"Berhasil membaca {len(charts_data)} data dari {file_path}")

        # 3. Siapkan Query SQL INSERT SECARA TERPISAH
        insert_artist_query = """
            INSERT INTO Artists (artist_id, artist_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE artist_name = VALUES(artist_name);
        """
        
        insert_song_query = """
            INSERT INTO Songs (song_id, title, artist_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                title = VALUES(title), 
                artist_id = VALUES(artist_id);
        """
        
        insert_chart_query = """
            INSERT INTO Charts (ranking_id, song_id, current_rank, peak_position)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                song_id = VALUES(song_id), 
                current_rank = VALUES(current_rank), 
                peak_position = VALUES(peak_position);
        """
        
        # 4. Ekstrak data JSON ke bentuk Tuple
        data_insert_artists = []
        for item in artists_data:
            data_insert_artists.append((item['artist_id'], item['artist_name']))

        data_insert_songs = []
        for item in songs_data:
            data_insert_songs.append((item['song_id'], item['title'], item['artist_id']))

        data_insert_charts = []
        for item in charts_data:
            data_insert_charts.append((item['ranking_id'], item['song_id'], item['current_rank'], item['peak_position']))
        
        # 5. Eksekusi Query secara massal (Batch Insert) dengan Query masing-masing
        cursor.executemany(insert_artist_query, data_insert_artists)
        row_artists = cursor.rowcount # Simpan jumlah row yang terdampak
        
        cursor.executemany(insert_song_query, data_insert_songs)
        row_songs = cursor.rowcount
        
        cursor.executemany(insert_chart_query, data_insert_charts)
        row_charts = cursor.rowcount
        
        # 6. COMMIT agar tersimpan!
        connection.commit()
        
        print("\n[SUCCESS] Proses Import Selesai!")
        print(f"- {row_artists} baris data Artists berhasil diproses.")
        print(f"- {row_songs} baris data Songs berhasil diproses.")
        print(f"- {row_charts} baris data Charts berhasil diproses.")

    except Error as e:
        print(f"[ERROR] Terjadi kesalahan database: {e}")
    except FileNotFoundError:
        print(f"[ERROR] File JSON tidak ditemukan di path: {file_path}")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan lain: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_json_to_db()