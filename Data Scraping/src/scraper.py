import requests
import json
from bs4 import BeautifulSoup, FeatureNotFound

url = 'https://www.billboard.com/charts/hot-100/'

def fetch_html(url, parser="lxml"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ; Reysha/13524137@std.stei.itb.ac.id"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        try:
            return BeautifulSoup(response.text, parser)
        except FeatureNotFound:
            return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return None

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[SUCCESS] Tersimpan: {filename}")

if __name__ == "__main__":
    soup = fetch_html(url)
    
    if soup:
        print("Memulai proses ekstraksi dan relasional mapping...\n")
        
        # Inisialisasi "Database" di memori (menggunakan dictionary agar pencarian cepat)
        artists_db = {}
        songs_db = {}
        chart_rankings = []
        
        # ID Auto-increment
        artist_counter = 1
        song_counter = 1
        
        rows = soup.find_all("div", class_="o-chart-results-list-row-container")
        
        for index, row in enumerate(rows, start=1):
            # --- 1. EKSTRAKSI DATA ---
            title_element = row.find("h3", id="title-of-a-story")
            artist_element = title_element.find_next_sibling("span") if title_element else None
            
            # Billboard menyimpan statisik (Peak) di dalam elemen <ul>
            # Struktur ini membutuhkan penyesuaian jika HTML web berubah
            stats_elements = row.find_all("span", class_="c-label")
            
            # --- 2. CLEANING DATA ---
            song_title = title_element.text.strip().replace('"', '') if title_element else "Unknown Song"
            artist_name = artist_element.text.strip() if artist_element else "Unknown Artist"
            
            # Ekstraksi statistik (mengambil angka dari span, jika error set ke null/0)
            try:
                # Logika indeks ini sangat bergantung pada struktur UI Billboard saat ini
                peak = int(stats_elements[-2].text.strip()) if stats_elements[-2].text.strip().isdigit() else None
            except:
                peak = None

            # --- 3. RELASIONAL MAPPING ---
            
            # A. Proses Tabel Artis
            if artist_name not in artists_db:
                artists_db[artist_name] = {
                    "artist_id": artist_counter,
                    "artist_name": artist_name
                }
                artist_counter += 1
            current_artist_id = artists_db[artist_name]["artist_id"]
            
            # B. Proses Tabel Lagu (Relasi ke Artis)
            if song_title not in songs_db:
                songs_db[song_title] = {
                    "song_id": song_counter,
                    "title": song_title,
                    "artist_id": current_artist_id # Foreign Key
                }
                song_counter += 1
            current_song_id = songs_db[song_title]["song_id"]
            
            # C. Proses Tabel Chart (Relasi ke Lagu)
            chart_rankings.append({
                "ranking_id": index,
                "song_id": current_song_id, # Foreign Key
                "current_rank": index,
                "peak_position": peak,
            })
            
        # --- 4. EXPORT KE BERBAGAI FILE JSON ---
        if chart_rankings:
            # Convert dictionary values kembali menjadi list untuk JSON output
            save_to_json(list(artists_db.values()), "../data/artists.json")
            save_to_json(list(songs_db.values()), "../data/songs.json")
            save_to_json(chart_rankings, "../data/chart_rankings.json")
        else:
            print("[WARNING] Tidak ada data yang berhasil diparsing.")