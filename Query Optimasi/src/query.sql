-- ==========================================
-- QUERY OPTIMASI 1: Subquery ke JOIN
-- ==========================================
-- Penjelasan: Query ini mencari judul lagu dari artis tertentu. 
-- Kueri awal menggunakan IN (Subquery) yang membebani memori karena harus mengevaluasi kueri di dalam kurung berulang kali. 
-- Saya mengubahnya menjadi INNER JOIN karena langsung memetakan indeks kedua tabel.

-- Kueri Sebelum Optimasi:
SELECT title FROM Songs 
WHERE artist_id IN (SELECT artist_id FROM Artists WHERE artist_name = 'Taylor Swift');

-- Kueri Setelah Optimasi:
SELECT s.title FROM Songs s
JOIN Artists a ON s.artist_id = a.artist_id
WHERE a.artist_name = 'Taylor Swift';

-- ==========================================
-- QUERY OPTIMASI 2: Menghindari Operasi
-- ==========================================
-- Penjelasan: Query ini mencari lagu di peringkat top 10
-- MariaDB dapat bekerja lebih cepat jika langsung membaca nilai, dibandingkan harus menghitung operasi matematika terlebih dahulu

-- Kueri Sebelum OPtimasi:
SELECT song_id, current_rank FROM Charts 
WHERE current_rank - 5 <= 5;

-- Kueri Setelah Optimasi:
SELECT song_id, current_rank FROM Charts 
WHERE current_rank <= 10;

-- ==========================================
-- QUERY OPTIMASI 3: EXISTS ke IN
-- ==========================================
-- Penjelasan: Query ini mencari artis yang memiliki kata "Love" di judul lagunya.
-- EXISTS akan langsung berhenti mencari begitu ia menemukan suatu kecocokan pertama di tabel Charts. Sedangkan IN akan mencari dan mengumpulkan semua data kecocokan terlebih dahulu

-- Kueri sebelum optimasi:
SELECT artist_name 
FROM Artists 
WHERE artist_id IN (
    SELECT artist_id 
    FROM Songs 
    WHERE title LIKE '%Love%'
);

-- Kueri setelah optimasi:
SELECT a.artist_name 
FROM Artists a
WHERE EXISTS (
    SELECT 1 
    FROM Songs s 
    WHERE s.artist_id = a.artist_id AND s.title LIKE '%Love%'
);

