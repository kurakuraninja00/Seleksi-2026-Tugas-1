import json
import mysql.connector
from mysql.connector import Error

def load_data_to_warehouse():
    dw_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'billboard_dw'
    }

    try:
        connection = mysql.connector.connect(**dw_config)
        cursor = connection.cursor()

        # 1. Ekstrak Data dari JSON
        with open('../../Data Scraping/data/artists.json', 'r', encoding='utf-8') as f:
            artists_data = json.load(f)
        with open('../../Data Scraping/data/songs.json', 'r', encoding='utf-8') as f:
            songs_data = json.load(f)
        with open('../../Data Scraping/data/chart_rankings.json', 'r', encoding='utf-8') as f:
            charts_data = json.load(f)

        # 2. Transform & Load Dim_Artists
        insert_artist_query = """
            INSERT INTO Dim_Artists (artist_id, artist_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE artist_name = VALUES(artist_name);
        """
        data_artists = [(item['artist_id'], item['artist_name']) for item in artists_data]
        cursor.executemany(insert_artist_query, data_artists)
        artists_inserted = cursor.rowcount

        # 3. Transform & Load Dim_Songs (Hanya ambil song_id dan title)
        insert_song_query = """
            INSERT INTO Dim_Songs (song_id, title)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE title = VALUES(title);
        """
        data_songs = [(item['song_id'], item['title']) for item in songs_data]
        cursor.executemany(insert_song_query, data_songs)
        songs_inserted = cursor.rowcount

        # 4. Transform & Load Fact_Charts
        # Membuat pemetaan (mapping) untuk mencari artist_id berdasarkan song_id
        song_to_artist_map = {song['song_id']: song['artist_id'] for song in songs_data}

        insert_fact_query = """
            INSERT INTO Fact_Charts (ranking_id, song_id, artist_id, current_rank, peak_position)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                song_id = VALUES(song_id), 
                artist_id = VALUES(artist_id),
                current_rank = VALUES(current_rank), 
                peak_position = VALUES(peak_position);
        """
        
        data_facts = []
        for chart in charts_data:
            s_id = chart['song_id']
            # Mengambil artist_id dari mapping yang sudah kita buat
            a_id = song_to_artist_map.get(s_id) 
            
            data_facts.append((
                chart['ranking_id'],
                s_id,
                a_id,
                chart['current_rank'],
                chart['peak_position']
            ))
            
        cursor.executemany(insert_fact_query, data_facts)
        facts_inserted = cursor.rowcount

        # 5. Commit dan Selesai
        connection.commit()
        
        print("\n[SUCCESS] Proses ETL (Extract, Transform, Load) Selesai!")
        print(f"- Data Dim_Artists diproses.")
        print(f"- Data Dim_Songs diproses.")
        print(f"- Data Fact_Charts diproses.")

    except Error as e:
        print(f"[ERROR] Gagal memproses data: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    load_data_to_warehouse()