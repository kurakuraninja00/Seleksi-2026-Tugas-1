import mysql.connector
from mysql.connector import Error

def setup_data_warehouse():
    dw_config = {
        'host': 'localhost',
        'user': 'root',     
        'password': ''       
    }

    try:
        connection = mysql.connector.connect(**dw_config)
        cursor = connection.cursor()

        # 1. Reset Database
        print("Mereset dan membuat ulang data warehouse 'billboard_dw'...")
        cursor.execute("DROP DATABASE IF EXISTS billboard_dw;")
        cursor.execute("CREATE DATABASE billboard_dw;")         
        cursor.execute("USE billboard_dw;")

        tables = {}
        
        # 2. Membuat Tabel Dimensi Artis (Tanpa Auto Increment)
        tables['Dim_Artists'] = """
            CREATE TABLE IF NOT EXISTS Dim_Artists (
                artist_id INT,
                artist_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (artist_id),
                CONSTRAINT unique_artist_name UNIQUE (artist_name)
            ) ENGINE=Innodb;
        """

        # 3. Membuat Tabel Dimensi Lagu (Tanpa artist_id di sini)
        tables['Dim_Songs'] = """
            CREATE TABLE IF NOT EXISTS Dim_Songs (
                song_id INT,
                title VARCHAR(255) NOT NULL,
                PRIMARY KEY (song_id)
            ) ENGINE=Innodb;
        """

        # 4. Membuat Tabel Fakta (Pusat Bintang yang memegang semua FK dan Metrik)
        tables['Fact_Charts'] = """
            CREATE TABLE IF NOT EXISTS Fact_Charts (
                ranking_id INT, 
                song_id INT NOT NULL,
                artist_id INT NOT NULL,
                current_rank INT NOT NULL,
                peak_position INT,
                PRIMARY KEY (ranking_id),
                CONSTRAINT fk_fact_song 
                    FOREIGN KEY (song_id) REFERENCES Dim_Songs(song_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                CONSTRAINT fk_fact_artist 
                    FOREIGN KEY (artist_id) REFERENCES Dim_Artists(artist_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
            ) ENGINE=Innodb;
        """

        for table_name in tables:
            print(f"Membuat tabel {table_name}...")
            cursor.execute(tables[table_name])

        connection.commit()
        print("\n[SUCCESS] Skema Star Schema (Data Warehouse) berhasil diimplementasikan!")

    except Error as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Koneksi Mariadb ditutup.")

if __name__ == "__main__":
    setup_data_warehouse()