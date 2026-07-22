import mysql.connector
from mysql.connector import Error

def create_database_and_tables():
    # Ganti dengan kredensial MariaDB kamu
    db_config = {
        'host': 'localhost',
        'user': 'root',     
        'password': ''       
    }

    try:
        # 1. Koneksi awal ke server MySQL/MariaDB
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # 2. Membuat Database
        print("Membuat database 'billboard_db'...")
        cursor.execute("DROP DATABASE IF EXISTS billboard_db;")
        cursor.execute("CREATE DATABASE billboard_db;")         
        
        # Menggunakan database yang baru dibuat
        cursor.execute("USE billboard_db;")

        # 3. Definisi DDL untuk Tabel
        tables = {}
        
        tables['Artists'] = """
            CREATE TABLE IF NOT EXISTS Artists (
                artist_id INT,
                artist_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (artist_id),
                CONSTRAINT unique_artist_name UNIQUE (artist_name)
            ) ENGINE=InnoDB;
        """

        tables['Songs'] = """
            CREATE TABLE IF NOT EXISTS Songs (
                song_id INT,
                title VARCHAR(255) NOT NULL,
                artist_id INT NOT NULL,
                PRIMARY KEY (song_id),
                CONSTRAINT fk_song_artist 
                    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
            ) ENGINE=InnoDB;
        """

        tables['Charts'] = """
            CREATE TABLE IF NOT EXISTS Charts (
                ranking_id INT, 
                song_id INT NOT NULL,
                current_rank INT NOT NULL,
                peak_position INT,
                PRIMARY KEY (ranking_id),
                CONSTRAINT fk_chart_song 
                    FOREIGN KEY (song_id) REFERENCES Songs(song_id) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE,
                CONSTRAINT chk_current_rank CHECK (current_rank >= 1 AND current_rank <= 100)
            ) ENGINE=InnoDB;
        """

        # Eksekusi pembuatan tabel
        for table_name in tables:
            print(f"Membuat tabel {table_name}...")
            cursor.execute(tables[table_name])


        # Commit perubahan
        connection.commit()
        print("\n[SUCCESS] Seluruh skema database relasional berhasil diimplementasikan!")

    except Error as e:
        print(f"[ERROR] Terjadi kesalahan saat koneksi atau eksekusi query: {e}")
        
    finally:
        # Menutup koneksi dengan aman
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Koneksi MariaDB ditutup.")

if __name__ == "__main__":
    create_database_and_tables()