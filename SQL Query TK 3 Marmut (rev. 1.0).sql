CREATE SCHEMA MARMUT;


SET SEARCH_PATH TO MARMUT;


CREATE TABLE AKUN (
        email VARCHAR(50) PRIMARY KEY,
        password VARCHAR(50) NOT NULL,
        nama VARCHAR(100) NOT NULL,
        gender INTEGER NOT NULL CHECK(gender IN (0,1)),
        tempat_lahir VARCHAR(50) NOT NULL,
        tanggal_lahir date NOT NULL,
        is_verified BOOLEAN NOT NULL,
        kota_asal VARCHAR(50) NOT NULL
);


CREATE TABLE PAKET (
        jenis VARCHAR(50) PRIMARY KEY,
        harga INTEGER NOT NULL
);


CREATE TABLE TRANSACTION (
        id UUID,
        jenis_paket VARCHAR(50),
        email VARCHAR(50),
        timestamp_dimulai TIMESTAMP NOT NULL,
        timestamp_berakhir TIMESTAMP NOT NULL,
        metode_bayar VARCHAR NOT NULL,
        nominal INTEGER NOT NULL,
        PRIMARY KEY (id, jenis_paket, email),
        FOREIGN KEY (jenis_paket) REFERENCES PAKET(jenis),
        FOREIGN KEY (email) REFERENCES AKUN(email)
);


CREATE TABLE PREMIUM (
        email VARCHAR(50) PRIMARY KEY,
        FOREIGN KEY (email) REFERENCES AKUN(email)
);


CREATE TABLE NONPREMIUM (
        email VARCHAR(50) PRIMARY KEY,
        FOREIGN KEY (email) REFERENCES AKUN(email)
);


CREATE TABLE KONTEN (
        id UUID PRIMARY KEY,
        judul VARCHAR(100) NOT NULL,
        tanggal_rilis DATE NOT NULL,
        tahun INTEGER NOT NULL,
        durasi INTEGER NOT NULL
);


CREATE TABLE GENRE (
        id_konten UUID,
        genre VARCHAR(50),
        PRIMARY KEY (id_konten, genre),
        FOREIGN KEY (id_konten) REFERENCES KONTEN(id)
);


CREATE TABLE PODCASTER (
        email VARCHAR(50) PRIMARY KEY,
        FOREIGN KEY (email) REFERENCES AKUN(email)
);


CREATE TABLE PODCAST (
        id_konten UUID PRIMARY KEY,
        email_podcaster VARCHAR(50),
        FOREIGN KEY (id_konten) REFERENCES KONTEN(id),
        FOREIGN KEY (email_podcaster) REFERENCES PODCASTER(email)
);


CREATE TABLE EPISODE (
        id_episode UUID PRIMARY KEY,
        id_konten_podcast UUID,
        judul VARCHAR(100) NOT NULL,
        deskripsi VARCHAR(500) NOT NULL,
        durasi INTEGER NOT NULL,
        tanggal_rilis DATE NOT NULL,
        FOREIGN KEY (id_konten_podcast) REFERENCES PODCAST(id_konten)
);


CREATE TABLE PEMILIK_HAK_CIPTA (
        id UUID PRIMARY KEY,
        rate_royalti INTEGER NOT NULL
);


CREATE TABLE ARTIST (
        id UUID PRIMARY KEY,
        email_akun VARCHAR(50),
        id_pemilik_hak_cipta UUID,
        FOREIGN KEY(email_akun) REFERENCES AKUN(email),
        FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id)
);


CREATE TABLE SONGWRITER (
        id UUID PRIMARY KEY,
        email_akun VARCHAR(50),
        id_pemilik_hak_cipta UUID,
        FOREIGN KEY(email_akun) REFERENCES AKUN(email),
        FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id)        
);


CREATE TABLE LABEL (
        id UUID PRIMARY KEY,
        nama VARCHAR(100) NOT NULL,
        email VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        kontak VARCHAR(50) NOT NULL,
        id_pemilik_hak_cipta UUID,
        FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id)
);


CREATE TABLE ALBUM (
        id UUID PRIMARY KEY,
        judul VARCHAR(100) NOT NULL,
        jumlah_lagu INTEGER NOT NULL DEFAULT 0,
        id_label UUID,
        total_durasi INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(id_label) REFERENCES LABEL(id)
);


CREATE TABLE SONG (
        id_konten UUID PRIMARY KEY,
        id_artist UUID,
        id_album UUID,
        total_play INTEGER NOT NULL DEFAULT 0,
        total_download INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (id_konten) REFERENCES KONTEN(id),
        FOREIGN KEY (id_artist) REFERENCES ARTIST(id),
        FOREIGN KEY (id_album) REFERENCES ALBUM(id)
);


CREATE TABLE SONGWRITER_WRITE_SONG (
        id_songwriter UUID,
        id_song UUID,
        PRIMARY KEY(id_songwriter, id_song),
        FOREIGN KEY (id_songwriter) REFERENCES SONGWRITER(id),
        FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);


CREATE TABLE DOWNLOADED_SONG (
        id_song UUID,
        email_downloader VARCHAR(50),
        PRIMARY KEY (id_song, email_downloader),
        FOREIGN KEY (id_song) REFERENCES SONG(id_konten),
        FOREIGN KEY (email_downloader) REFERENCES PREMIUM(email)
);


CREATE TABLE PLAYLIST (
        id UUID PRIMARY KEY
);


CREATE TABLE CHART (
        tipe VARCHAR(50) PRIMARY KEY,
        id_playlist UUID,
        FOREIGN KEY (id_playlist) REFERENCES PLAYLIST(id)
);


CREATE TABLE USER_PLAYLIST (
        email_pembuat VARCHAR(50),
        id_user_playlist UUID,
        judul VARCHAR(100) NOT NULL,
        deskripsi VARCHAR(500) NOT NULL,
        jumlah_lagu INTEGER NOT NULL,
        tanggal_dibuat DATE NOT NULL,
        id_playlist UUID,
        total_durasi INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY(email_pembuat, id_user_playlist),
        FOREIGN KEY(email_pembuat) REFERENCES AKUN(email),
        FOREIGN KEY(id_playlist) REFERENCES PLAYLIST(id)
);


CREATE TABLE ROYALTI (
        id_pemilik_hak_cipta UUID,
        id_song UUID,
        jumlah INTEGER NOT NULL,
        PRIMARY KEY (id_pemilik_hak_cipta, id_song),
        FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id),
        FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);


CREATE TABLE AKUN_PLAY_USER_PLAYLIST (
        email_pemain VARCHAR(50),
        id_user_playlist UUID,
        email_pembuat VARCHAR(50),
        waktu TIMESTAMP,
        PRIMARY KEY (email_pemain, id_user_playlist, email_pembuat, waktu),
        FOREIGN KEY (email_pemain) REFERENCES AKUN(email),
        FOREIGN KEY (id_user_playlist, email_pembuat) REFERENCES USER_PLAYLIST(id_user_playlist, email_pembuat)
);


CREATE TABLE AKUN_PLAY_SONG (
        email_pemain VARCHAR(50),
        id_song UUID,
        waktu TIMESTAMP,
        PRIMARY KEY (email_pemain, id_song, waktu),
        FOREIGN KEY (email_pemain) REFERENCES AKUN(email),
        FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);


CREATE TABLE PLAYLIST_SONG (
        id_playlist UUID,
        id_song UUID,
        PRIMARY KEY (id_playlist, id_song),
        FOREIGN KEY (id_playlist) REFERENCES PLAYLIST(id),
        FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);




INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
VALUES
('user1@example.com', 'password1', 'John Doe', 1, 'New York', '1990-05-15', TRUE, 'New York'),
('user2@example.com', 'password2', 'Jane Smith', 0, 'Los Angeles', '1988-08-22', TRUE, 'Los Angeles'),
('user3@example.com', 'password3', 'Michael Johnson', 1, 'Chicago', '1992-01-10', TRUE, 'Chicago'),
('user4@example.com', 'password4', 'Emily Brown', 0, 'Houston', '1995-11-30', TRUE, 'Houston'),
('user5@example.com', 'password5', 'David Williams', 1, 'Phoenix', '1987-03-05', TRUE, 'Phoenix'),
('user6@example.com', 'password6', 'Jessica Martinez', 0, 'Philadelphia', '1991-07-20', TRUE, 'Philadelphia'),
('user7@example.com', 'password7', 'Daniel Jones', 1, 'San Antonio', '1989-09-12', TRUE, 'San Antonio'),
('user8@example.com', 'password8', 'Sarah Taylor', 0, 'San Diego', '1993-04-18', TRUE, 'San Diego'),
('user9@example.com', 'password9', 'Christopher Brown', 1, 'Dallas', '1996-06-25', TRUE, 'Dallas'),
('user10@example.com', 'password10', 'Ashley Wilson', 0, 'Austin', '1990-02-08', TRUE, 'Austin'),
('user11@example.com', 'password11', 'Matthew Anderson', 1, 'Jacksonville', '1994-12-03', FALSE, 'Jacksonville'),
('user12@example.com', 'password12', 'Amanda Garcia', 0, 'San Francisco', '1988-10-17', TRUE, 'San Francisco'),
('user13@example.com', 'password13', 'James Martinez', 1, 'Indianapolis', '1992-07-15', TRUE, 'Indianapolis'),
('user14@example.com', 'password14', 'Lauren Hernandez', 0, 'Columbus', '1995-05-22', TRUE, 'Columbus'),
('user15@example.com', 'password15', 'Ryan Walker', 1, 'Fort Worth', '1987-11-08', TRUE, 'Fort Worth'),
('user16@example.com', 'password16', 'Stephanie King', 0, 'Charlotte', '1991-09-28', TRUE, 'Charlotte'),
('user17@example.com', 'password17', 'Joshua Young', 1, 'Detroit', '1989-03-14', FALSE, 'Detroit'),
('user18@example.com', 'password18', 'Olivia Scott', 0, 'El Paso', '1993-01-02', TRUE, 'El Paso'),
('user19@example.com', 'password19', 'Andrew Perez', 1, 'Seattle', '1996-08-10', TRUE, 'Seattle'),
('user20@example.com', 'password20', 'Megan Flores', 0, 'Denver', '1990-04-04', TRUE, 'Denver'),
('user21@example.com', 'password21', 'Kevin Lopez', 1, 'Washington', '1994-12-20', TRUE, 'Washington'),
('user22@example.com', 'password22', 'Hannah Hill', 0, 'Memphis', '1988-06-18', TRUE, 'Memphis'),
('user23@example.com', 'password23', 'Justin Kelly', 1, 'Boston', '1992-03-05', TRUE, 'Boston'),
('user24@example.com', 'password24', 'Emma Turner', 0, 'Nashville', '1995-10-29', TRUE, 'Nashville'),
('user25@example.com', 'password25', 'Brandon Baker', 1, 'Baltimore', '1987-07-07', TRUE, 'Baltimore'),
('user26@example.com', 'password26', 'Kayla Mitchell', 0, 'Oklahoma City', '1991-05-14', TRUE, 'Oklahoma City'),
('user27@example.com', 'password27', 'Nicholas Perez', 1, 'Louisville', '1989-01-18', TRUE, 'Louisville'),
('user28@example.com', 'password28', 'Samantha Nelson', 0, 'Portland', '1993-09-02', TRUE, 'Portland'),
('user29@example.com', 'password29', 'Jordan Carter', 1, 'Las Vegas', '1996-06-20', TRUE, 'Las Vegas'),
('user30@example.com', 'password30', 'Victoria Ramirez', 0, 'Milwaukee', '1990-02-12', TRUE, 'Milwaukee'),
('user31@example.com', 'password31', 'Cameron Cooper', 1, 'Albuquerque', '1994-11-27', FALSE, 'Albuquerque'),
('user32@example.com', 'password32', 'Madison Morgan', 0, 'Tucson', '1988-10-21', TRUE, 'Tucson'),
('user33@example.com', 'password33', 'Patrick Coleman', 1, 'Fresno', '1992-08-15', TRUE, 'Fresno'),
('user34@example.com', 'password34', 'Brianna Rivera', 0, 'Sacramento', '1995-04-09', TRUE, 'Sacramento'),
('user35@example.com', 'password35', 'Tyler Gray', 1, 'Long Beach', '1987-12-24', TRUE, 'Long Beach'),
('user36@example.com', 'password36', 'Abigail Cox', 0, 'Kansas City', '1991-06-16', FALSE, 'Kansas City'),
('user37@example.com', 'password37', 'Jacob Reyes', 1, 'Mesa', '1989-02-19', FALSE, 'Mesa'),
('user38@example.com', 'password38', 'Grace Stewart', 0, 'Atlanta', '1993-10-03', FALSE, 'Atlanta'),
('user39@example.com', 'password39', 'Ethan Morris', 1, 'Virginia Beach', '1996-07-25', FALSE, 'Virginia Beach'),
('user40@example.com', 'password40', 'Natalie Bailey', 0, 'Raleigh', '1990-03-18', FALSE, 'Raleigh'),
('user41@example.com', 'password41', 'Christian Howard', 1, 'Omaha', '1994-12-11', FALSE, 'Omaha'),
('user42@example.com', 'password42', 'Kylie Coleman', 0, 'Miami', '1988-09-15', FALSE, 'Miami'),
('user43@example.com', 'password43', 'Dylan Sanders', 1, 'Minneapolis', '1992-06-11', FALSE, 'Minneapolis'),
('user44@example.com', 'password44', 'Hailey Evans', 0, 'Colorado Springs', '1995-05-05', FALSE, 'Colorado Springs'),
('user45@example.com', 'password45', 'Brandon Ramirez', 1, 'Tulsa', '1987-12-30', FALSE, 'Tulsa'),
('user46@example.com', 'password46', 'Rachel Foster', 0, 'Arlington', '1991-08-24', FALSE, 'Arlington'),
('user47@example.com', 'password47', 'Aaron Reed', 1, 'New Orleans', '1989-04-17', FALSE, 'New Orleans'),
('user48@example.com', 'password48', 'Courtney Cooper', 0, 'Wichita', '1993-01-11', FALSE, 'Wichita'),
('user49@example.com', 'password49', 'Jasmine Stewart', 1, 'Bakersfield', '1996-10-05', FALSE, 'Bakersfield'),
('user50@example.com', 'password50', 'Austin Brooks', 0, 'Honolulu', '1990-04-29', FALSE, 'Honolulu');


INSERT INTO PAKET (jenis, harga)
VALUES
('1 bulan', 100000),
('3 bulan', 270000),
('6 bulan', 500000),
('1 tahun', 900000);


INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
VALUES
('550e8400-e29b-41d4-a716-446655440000', '1 bulan', 'user3@example.com', '2024-04-27 09:00:00', '2024-05-27 09:00:00', 'Transfer Bank', 100000),
('550e8400-e29b-41d4-a716-446655440001', '3 bulan', 'user7@example.com', '2024-04-26 10:00:00', '2024-07-26 10:00:00', 'Kartu Kredit', 250000),
('550e8400-e29b-41d4-a716-446655440002', '6 bulan', 'user17@example.com', '2024-04-25 11:00:00', '2024-10-25 11:00:00', 'Transfer Bank', 500000),
('550e8400-e29b-41d4-a716-446655440003', '1 tahun', 'user23@example.com', '2024-04-24 12:00:00', '2025-04-24 12:00:00', 'PayPal', 1000000),
('550e8400-e29b-41d4-a716-446655440004', '1 tahun', 'user41@example.com', '2024-04-23 13:00:00', '2025-04-23 13:00:00', 'Kartu Debit', 900000);






INSERT INTO PREMIUM (email)
VALUES
('user3@example.com'),
('user7@example.com'),
('user17@example.com'),
('user23@example.com'),
('user41@example.com');


INSERT INTO NONPREMIUM (email)
VALUES
('user6@example.com'),
('user8@example.com'),
('user9@example.com'),
('user10@example.com'),
('user11@example.com'),
('user12@example.com'),
('user13@example.com'),
('user14@example.com'),
('user15@example.com'),
('user16@example.com'),
('user18@example.com'),
('user19@example.com'),
('user20@example.com'),
('user21@example.com'),
('user22@example.com'),
('user24@example.com'),
('user25@example.com'),
('user26@example.com'),
('user27@example.com'),
('user28@example.com'),
('user29@example.com'),
('user30@example.com'),
('user31@example.com'),
('user32@example.com'),
('user33@example.com');


INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Spider-Man: No Way Home', '2021-12-17', 2021, 148),
('550e8400-e29b-41d4-a716-446655440001', 'Avengers: Endgame', '2019-04-26', 2019, 181),
('550e8400-e29b-41d4-a716-446655440002', 'Joker', '2019-10-04', 2019, 122),
('550e8400-e29b-41d4-a716-446655440003', 'Parasite', '2019-05-30', 2019, 132),
('550e8400-e29b-41d4-a716-446655440004', 'Spider-Man: Far From Home', '2019-07-02', 2019, 129),
('550e8400-e29b-41d4-a716-446655440005', 'Black Panther', '2018-02-16', 2018, 134),
('550e8400-e29b-41d4-a716-446655440006', 'Avengers: Infinity War', '2018-04-27', 2018, 149),
('550e8400-e29b-41d4-a716-446655440007', 'Bohemian Rhapsody', '2018-11-02', 2018, 134),
('550e8400-e29b-41d4-a716-446655440008', 'Spider-Man: Homecoming', '2017-07-07', 2017, 133),
('550e8400-e29b-41d4-a716-446655440009', 'La La Land', '2016-12-09', 2016, 128),
('550e8400-e29b-41d4-a716-446655440010', 'Captain America: Civil War', '2016-05-06', 2016, 147),
('550e8400-e29b-41d4-a716-446655440011', 'Deadpool', '2016-02-12', 2016, 108),
('550e8400-e29b-41d4-a716-446655440012', 'The Martian', '2015-10-02', 2015, 144),
('550e8400-e29b-41d4-a716-446655440013', 'Mad Max: Fury Road', '2015-05-15', 2015, 120),
('550e8400-e29b-41d4-a716-446655440014', 'Interstellar', '2014-11-07', 2014, 169),
('550e8400-e29b-41d4-a716-446655440015', 'Guardians of the Galaxy', '2014-08-01', 2014, 121),
('550e8400-e29b-41d4-a716-446655440016', 'The Wolf of Wall Street', '2013-12-25', 2013, 180),
('550e8400-e29b-41d4-a716-446655440017', 'Gravity', '2013-10-04', 2013, 91),
('550e8400-e29b-41d4-a716-446655440018', 'The Avengers', '2012-05-04', 2012, 143),
('550e8400-e29b-41d4-a716-446655440019', 'The Dark Knight Rises', '2012-07-20', 2012, 164),
('550e8400-e29b-41d4-a716-446655440020', 'Inception', '2010-07-16', 2010, 148),
('550e8400-e29b-41d4-a716-446655440021', 'Avatar', '2009-12-18', 2009, 162),
('550e8400-e29b-41d4-a716-446655440022', 'The Dark Knight', '2008-07-18', 2008, 152),
('550e8400-e29b-41d4-a716-446655440023', 'Iron Man', '2008-05-02', 2008, 126),
('550e8400-e29b-41d4-a716-446655440024', 'The Lord of the Rings: The Return of the King', '2003-12-17', 2003, 201),
('550e8400-e29b-41d4-a716-446655440025', 'The Lord of the Rings: The Two Towers', '2002-12-18', 2002, 179),
('550e8400-e29b-41d4-a716-446655440026', 'The Lord of the Rings: The Fellowship of the Ring', '2001-12-19', 2001, 178),
('550e8400-e29b-41d4-a716-446655440027', 'Gladiator', '2000-05-05', 2000, 155),
('550e8400-e29b-41d4-a716-446655440028', 'Saving Private Ryan', '1998-07-24', 1998, 169),
('550e8400-e29b-41d4-a716-446655440029', 'Titanic', '1997-12-19', 1997, 195),
('550e8400-e29b-41d4-a716-446655440030', 'Forrest Gump', '1994-07-06', 1994, 142),
('550e8400-e29b-41d4-a716-446655440031', 'Jurassic Park', '1993-06-11', 1993, 127),
('550e8400-e29b-41d4-a716-446655440032', 'Terminator 2: Judgment Day', '1991-07-03', 1991, 137),
('550e8400-e29b-41d4-a716-446655440033', 'Back to the Future', '1985-07-03', 1985, 116),
('550e8400-e29b-41d4-a716-446655440034', 'Star Wars: Episode VI - Return of the Jedi', '1983-05-25', 1983, 134),
('550e8400-e29b-41d4-a716-446655440035', 'Raiders of the Lost Ark', '1981-06-12', 1981, 115),
('550e8400-e29b-41d4-a716-446655440036', 'Superman', '1978-12-15', 1978, 143),
('550e8400-e29b-41d4-a716-446655440037', 'Jaws', '1975-06-20', 1975, 124),
('550e8400-e29b-41d4-a716-446655440038', 'The Godfather: Part II', '1974-12-20', 1974, 202),
('550e8400-e29b-41d4-a716-446655440039', 'The Exorcist', '1973-12-26', 1973, 122),
('550e8400-e29b-41d4-a716-446655440040', 'The Godfather', '1972-03-24', 1972, 175),
('550e8400-e29b-41d4-a716-446655440041', '2001: A Space Odyssey', '1968-04-02', 1968, 149),
('550e8400-e29b-41d4-a716-446655440042', 'Lawrence of Arabia', '1962-12-16', 1962, 227),
('550e8400-e29b-41d4-a716-446655440043', 'Psycho', '1960-06-16', 1960, 109),
('550e8400-e29b-41d4-a716-446655440044', '12 Angry Men', '1957-04-10', 1957, 96),
('550e8400-e29b-41d4-a716-446655440045', 'Singin in the Rain', '1952-04-11', 1952, 103),
('550e8400-e29b-41d4-a716-446655440046', 'Casablanca', '1943-11-26', 1943, 102),
('550e8400-e29b-41d4-a716-446655440047', 'Gone with the Wind', '1939-12-15', 1939, 238),
('550e8400-e29b-41d4-a716-446655440048', 'The Wizard of Oz', '1939-08-25', 1939, 101),
('550e8400-e29b-41d4-a716-446655440049', 'Snow White and the Seven Dwarfs', '1937-12-21', 1937, 83),
('550e8400-e29b-41d4-a716-446655440050', 'King Kong', '1933-04-07', 1933, 100),
('550e8400-e29b-41d4-a716-446655440051', 'Dracula', '1931-02-14', 1931, 75),
('550e8400-e29b-41d4-a716-446655440052', 'Metropolis', '1927-01-10', 1927, 153),
('550e8400-e29b-41d4-a716-446655440053', 'The Shawshank Redemption', '1994-10-14', 1994, 142),
('550e8400-e29b-41d4-a716-446655440054', 'The Godfather: Part III', '1990-12-25', 1990, 162),
('550e8400-e29b-41d4-a716-446655440055', 'The Silence of the Lambs', '1991-02-14', 1991, 118),
('550e8400-e29b-41d4-a716-446655440056', 'Schindlers List', '1993-12-15', 1993, 195),
('550e8400-e29b-41d4-a716-446655440057', 'The Green Mile', '1999-12-10', 1999, 189);




INSERT INTO GENRE (id_konten, genre)
VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Action'),
('550e8400-e29b-41d4-a716-446655440000', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440000', 'Fantasy'),
('550e8400-e29b-41d4-a716-446655440001', 'Action'),
('550e8400-e29b-41d4-a716-446655440001', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440001', 'Drama'),
('550e8400-e29b-41d4-a716-446655440002', 'Crime'),
('550e8400-e29b-41d4-a716-446655440002', 'Drama'),
('550e8400-e29b-41d4-a716-446655440002', 'Thriller'),
('550e8400-e29b-41d4-a716-446655440003', 'Comedy'),
('550e8400-e29b-41d4-a716-446655440003', 'Drama'),
('550e8400-e29b-41d4-a716-446655440003', 'Thriller'),
('550e8400-e29b-41d4-a716-446655440004', 'Action'),
('550e8400-e29b-41d4-a716-446655440004', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440005', 'Action'),
('550e8400-e29b-41d4-a716-446655440005', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440005', 'Sci-Fi'),
('550e8400-e29b-41d4-a716-446655440006', 'Action'),
('550e8400-e29b-41d4-a716-446655440006', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440007', 'Biography'),
('550e8400-e29b-41d4-a716-446655440007', 'Drama'),
('550e8400-e29b-41d4-a716-446655440007', 'Music'),
('550e8400-e29b-41d4-a716-446655440008', 'Action'),
('550e8400-e29b-41d4-a716-446655440008', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440009', 'Comedy'),
('550e8400-e29b-41d4-a716-446655440009', 'Drama'),
('550e8400-e29b-41d4-a716-446655440010', 'Action'),
('550e8400-e29b-41d4-a716-446655440010', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440010', 'Sci-Fi'),
('550e8400-e29b-41d4-a716-446655440011', 'Action'),
('550e8400-e29b-41d4-a716-446655440011', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440012', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440012', 'Drama'),
('550e8400-e29b-41d4-a716-446655440013', 'Action'),
('550e8400-e29b-41d4-a716-446655440013', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440013', 'Sci-Fi'),
('550e8400-e29b-41d4-a716-446655440014', 'Action'),
('550e8400-e29b-41d4-a716-446655440014', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440015', 'Action'),
('550e8400-e29b-41d4-a716-446655440015', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440015', 'Comedy'),
('550e8400-e29b-41d4-a716-446655440016', 'Biography'),
('550e8400-e29b-41d4-a716-446655440016', 'Comedy'),
('550e8400-e29b-41d4-a716-446655440017', 'Drama'),
('550e8400-e29b-41d4-a716-446655440018', 'Action'),
('550e8400-e29b-41d4-a716-446655440019', 'Action'),
('550e8400-e29b-41d4-a716-446655440019', 'Adventure'),
('550e8400-e29b-41d4-a716-446655440019', 'Drama'),
('550e8400-e29b-41d4-a716-446655440020', 'Action'),
('550e8400-e29b-41d4-a716-446655440021', 'Action'),
('550e8400-e29b-41d4-a716-446655440022', 'Action'),
('550e8400-e29b-41d4-a716-446655440023', 'Action'),
('550e8400-e29b-41d4-a716-446655440024', 'Action'),
('550e8400-e29b-41d4-a716-446655440025', 'Action'),
('550e8400-e29b-41d4-a716-446655440026', 'Action'),
('550e8400-e29b-41d4-a716-446655440027', 'Action'),
('550e8400-e29b-41d4-a716-446655440028', 'Action'),
('550e8400-e29b-41d4-a716-446655440029', 'Action'),
('550e8400-e29b-41d4-a716-446655440030', 'Action'),
('550e8400-e29b-41d4-a716-446655440031', 'Action'),
('550e8400-e29b-41d4-a716-446655440032', 'Action'),
('550e8400-e29b-41d4-a716-446655440033', 'Action'),
('550e8400-e29b-41d4-a716-446655440034', 'Action'),
('550e8400-e29b-41d4-a716-446655440035', 'Action'),
('550e8400-e29b-41d4-a716-446655440036', 'Action'),
('550e8400-e29b-41d4-a716-446655440037', 'Action'),
('550e8400-e29b-41d4-a716-446655440038', 'Action'),
('550e8400-e29b-41d4-a716-446655440039', 'Action'),
('550e8400-e29b-41d4-a716-446655440040', 'Action'),
('550e8400-e29b-41d4-a716-446655440041', 'Action'),
('550e8400-e29b-41d4-a716-446655440042', 'Action'),
('550e8400-e29b-41d4-a716-446655440043', 'Action'),
('550e8400-e29b-41d4-a716-446655440044', 'Action'),
('550e8400-e29b-41d4-a716-446655440045', 'Action'),
('550e8400-e29b-41d4-a716-446655440046', 'Action'),
('550e8400-e29b-41d4-a716-446655440047', 'Action'),
('550e8400-e29b-41d4-a716-446655440048', 'Action'),
('550e8400-e29b-41d4-a716-446655440049', 'Action'),
('550e8400-e29b-41d4-a716-446655440050', 'Action'),
('550e8400-e29b-41d4-a716-446655440051', 'Action'),
('550e8400-e29b-41d4-a716-446655440052', 'Action');


INSERT INTO PODCASTER (email)
VALUES
('user3@example.com'),
('user7@example.com'),
('user34@example.com'),
('user23@example.com'),
('user41@example.com'),
('user12@example.com'),
('user13@example.com'),
('user14@example.com'),
('user15@example.com'),
('user16@example.com');


INSERT INTO PODCAST (id_konten, email_podcaster)
VALUES
('550e8400-e29b-41d4-a716-446655440000', 'user3@example.com'),
('550e8400-e29b-41d4-a716-446655440001', 'user7@example.com'),
('550e8400-e29b-41d4-a716-446655440002', 'user34@example.com'),
('550e8400-e29b-41d4-a716-446655440003', 'user23@example.com'),
('550e8400-e29b-41d4-a716-446655440004', 'user41@example.com');


INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
VALUES
('550e8400-e29b-41d4-a716-446655450000', '550e8400-e29b-41d4-a716-446655440000', 'Introduction to the Podcast', 'Welcome to our podcast where we discuss various topics related to technology and innovation.', 30, '2024-04-01'),
('550e8400-e29b-41d4-a716-446655450001', '550e8400-e29b-41d4-a716-446655440000', 'The Future of AI', 'In this episode, we explore the current state and future possibilities of artificial intelligence.', 45, '2024-04-08'),
('550e8400-e29b-41d4-a716-446655450002', '550e8400-e29b-41d4-a716-446655440001', 'Cybersecurity Challenges', 'Learn about the latest cybersecurity challenges and how organizations are addressing them.', 40, '2024-04-15'),
('550e8400-e29b-41d4-a716-446655450003', '550e8400-e29b-41d4-a716-446655440001', 'Digital Transformation in Healthcare', 'Discover how technology is transforming the healthcare industry and improving patient care.', 35, '2024-04-22'),
('550e8400-e29b-41d4-a716-446655450004', '550e8400-e29b-41d4-a716-446655440002', 'The Future of Transportation', 'Explore the future of transportation with advancements in autonomous vehicles and sustainable energy.', 50, '2024-04-29'),
('550e8400-e29b-41d4-a716-446655450005', '550e8400-e29b-41d4-a716-446655440002', 'Space Exploration: Beyond Earth', 'Join us as we discuss humanity exploration of space and the exciting possibilities for the future.', 55, '2024-05-06'),
('550e8400-e29b-41d4-a716-446655450006', '550e8400-e29b-41d4-a716-446655440003', 'The Power of Data Analytics', 'Learn about the power of data analytics in driving business decisions and improving performance.', 30, '2024-05-13'),
('550e8400-e29b-41d4-a716-446655450007', '550e8400-e29b-41d4-a716-446655440003', 'The Rise of E-commerce', 'Discover how e-commerce has revolutionized the way we shop and the future trends in online retail.', 40, '2024-05-20'),
('550e8400-e29b-41d4-a716-446655450008', '550e8400-e29b-41d4-a716-446655440004', 'Sustainability in Business', 'Explore the importance of sustainability in business and how companies are integrating eco-friendly practices.', 45, '2024-05-27'),
('550e8400-e29b-41d4-a716-446655450009', '550e8400-e29b-41d4-a716-446655440004', 'The Art of Leadership', 'Join us as we delve into the art of leadership and the qualities that make great leaders.', 35, '2024-06-03');




INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti)
VALUES
('550e8400-e29b-41d4-a716-446655460000', 10),
('550e8400-e29b-41d4-a716-446655460001', 15),
('550e8400-e29b-41d4-a716-446655460002', 20),
('550e8400-e29b-41d4-a716-446655460003', 25),
('550e8400-e29b-41d4-a716-446655460004', 30),
('550e8400-e29b-41d4-a716-446655460005', 35),
('550e8400-e29b-41d4-a716-446655460006', 40),
('550e8400-e29b-41d4-a716-446655460007', 45),
('550e8400-e29b-41d4-a716-446655460008', 50),
('550e8400-e29b-41d4-a716-446655460009', 55),
('550e8400-e29b-41d4-a716-446655460010', 60),
('550e8400-e29b-41d4-a716-446655460011', 65),
('550e8400-e29b-41d4-a716-446655460012', 70),
('550e8400-e29b-41d4-a716-446655460013', 75),
('550e8400-e29b-41d4-a716-446655460014', 80),
('550e8400-e29b-41d4-a716-446655460015', 85),
('550e8400-e29b-41d4-a716-446655460016', 90),
('550e8400-e29b-41d4-a716-446655460017', 95),
('550e8400-e29b-41d4-a716-446655460018', 100),
('550e8400-e29b-41d4-a716-446655460019', 105),
('550e8400-e29b-41d4-a716-446655460020', 110),
('550e8400-e29b-41d4-a716-446655460021', 115),
('550e8400-e29b-41d4-a716-446655460022', 120),
('550e8400-e29b-41d4-a716-446655460023', 125),
('550e8400-e29b-41d4-a716-446655460024', 130);


INSERT INTO ARTIST (id, email_akun, id_pemilik_hak_cipta)
VALUES
('550e8400-e29b-41d4-a716-446655470000', 'user3@example.com', '550e8400-e29b-41d4-a716-446655460000'),
('550e8400-e29b-41d4-a716-446655470001', 'user7@example.com', '550e8400-e29b-41d4-a716-446655460001'),
('550e8400-e29b-41d4-a716-446655470002', 'user17@example.com', '550e8400-e29b-41d4-a716-446655460002'),
('550e8400-e29b-41d4-a716-446655470003', 'user23@example.com', '550e8400-e29b-41d4-a716-446655460003'),
('550e8400-e29b-41d4-a716-446655470004', 'user41@example.com', '550e8400-e29b-41d4-a716-446655460004'),
('550e8400-e29b-41d4-a716-446655470005', 'user9@example.com', '550e8400-e29b-41d4-a716-446655460005'),
('550e8400-e29b-41d4-a716-446655470006', 'user15@example.com', '550e8400-e29b-41d4-a716-446655460006'),
('550e8400-e29b-41d4-a716-446655470007', 'user29@example.com', '550e8400-e29b-41d4-a716-446655460007'),
('550e8400-e29b-41d4-a716-446655470008', 'user35@example.com', '550e8400-e29b-41d4-a716-446655460008'),
('550e8400-e29b-41d4-a716-446655470009', 'user33@example.com', '550e8400-e29b-41d4-a716-446655460009');


INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta)
VALUES
('550e8400-e29b-41d4-a716-446655480000', 'user6@example.com', '550e8400-e29b-41d4-a716-446655460011'),
('550e8400-e29b-41d4-a716-446655480001', 'user12@example.com', '550e8400-e29b-41d4-a716-446655460012'),
('550e8400-e29b-41d4-a716-446655480002', 'user18@example.com', '550e8400-e29b-41d4-a716-446655460013'),
('550e8400-e29b-41d4-a716-446655480003', 'user24@example.com', '550e8400-e29b-41d4-a716-446655460014'),
('550e8400-e29b-41d4-a716-446655480004', 'user30@example.com', '550e8400-e29b-41d4-a716-446655460015'),
('550e8400-e29b-41d4-a716-446655480005', 'user1@example.com', '550e8400-e29b-41d4-a716-446655460016'),
('550e8400-e29b-41d4-a716-446655480006', 'user4@example.com', '550e8400-e29b-41d4-a716-446655460017'),
('550e8400-e29b-41d4-a716-446655480007', 'user29@example.com', '550e8400-e29b-41d4-a716-446655460018'),
('550e8400-e29b-41d4-a716-446655480008', 'user10@example.com', '550e8400-e29b-41d4-a716-446655460019'),
('550e8400-e29b-41d4-a716-446655480009', 'user16@example.com', '550e8400-e29b-41d4-a716-446655460020');


INSERT INTO LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta)
VALUES
('550e8400-e29b-41d4-a716-446655490000', 'Universal Music Group', 'universal@example.com', 'passwordA', '081234567890', '550e8400-e29b-41d4-a716-446655460011'),
('550e8400-e29b-41d4-a716-446655490001', 'Sony Music Entertainment', 'sony@example.com', 'passwordB', '081234567891', '550e8400-e29b-41d4-a716-446655460012'),
('550e8400-e29b-41d4-a716-446655490002', 'Warner Music Group', 'warner@example.com', 'passwordC', '081234567892', '550e8400-e29b-41d4-a716-446655460013'),
('550e8400-e29b-41d4-a716-446655490003', 'Atlantic Records', 'atlantic@example.com', 'passwordD', '081234567893', '550e8400-e29b-41d4-a716-446655460014'),
('550e8400-e29b-41d4-a716-446655490004', 'Columbia Records', 'columbia@example.com', 'passwordE', '081234567894', '550e8400-e29b-41d4-a716-446655460015');




INSERT INTO ALBUM (id, judul, jumlah_lagu, id_label, total_durasi)
VALUES
('550e8400-e29b-41d4-a716-446655500000', '21', 12, '550e8400-e29b-41d4-a716-446655490000', 75),
('550e8400-e29b-41d4-a716-446655500001', 'Back to Black', 11, '550e8400-e29b-41d4-a716-446655490001', 45),
('550e8400-e29b-41d4-a716-446655500002', 'Thriller', 9, '550e8400-e29b-41d4-a716-446655490002', 42),
('550e8400-e29b-41d4-a716-446655500003', 'Abbey Road', 17, '550e8400-e29b-41d4-a716-446655490003', 47),
('550e8400-e29b-41d4-a716-446655500004', 'The Dark Side of the Moon', 10, '550e8400-e29b-41d4-a716-446655490004', 43);


INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download)
VALUES
('550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655470000', '550e8400-e29b-41d4-a716-446655500000', 100, 50),
('550e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655470001', '550e8400-e29b-41d4-a716-446655500001', 200, 100),
('550e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655470002', '550e8400-e29b-41d4-a716-446655500002', 300, 150),
('550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655470003', '550e8400-e29b-41d4-a716-446655500003', 400, 200),
('550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655470004', '550e8400-e29b-41d4-a716-446655500004', 500, 250),
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655470005', '550e8400-e29b-41d4-a716-446655500000', 600, 300),
('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655470006', '550e8400-e29b-41d4-a716-446655500001', 700, 350),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655470007', '550e8400-e29b-41d4-a716-446655500002', 800, 400),
('550e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-446655470008', '550e8400-e29b-41d4-a716-446655500003', 900, 450),
('550e8400-e29b-41d4-a716-446655440014', '550e8400-e29b-41d4-a716-446655470009', '550e8400-e29b-41d4-a716-446655500004', 1000, 500),
('550e8400-e29b-41d4-a716-446655440015', '550e8400-e29b-41d4-a716-446655470000', '550e8400-e29b-41d4-a716-446655500000', 1100, 550),
('550e8400-e29b-41d4-a716-446655440016', '550e8400-e29b-41d4-a716-446655470001', '550e8400-e29b-41d4-a716-446655500001', 1200, 600),
('550e8400-e29b-41d4-a716-446655440017', '550e8400-e29b-41d4-a716-446655470002', '550e8400-e29b-41d4-a716-446655500002', 1300, 650),
('550e8400-e29b-41d4-a716-446655440018', '550e8400-e29b-41d4-a716-446655470003', '550e8400-e29b-41d4-a716-446655500003', 1400, 700),
('550e8400-e29b-41d4-a716-446655440019', '550e8400-e29b-41d4-a716-446655470004', '550e8400-e29b-41d4-a716-446655500004', 1500, 750),
('550e8400-e29b-41d4-a716-446655440020', '550e8400-e29b-41d4-a716-446655470005', '550e8400-e29b-41d4-a716-446655500000', 1600, 800),
('550e8400-e29b-41d4-a716-446655440021', '550e8400-e29b-41d4-a716-446655470006', '550e8400-e29b-41d4-a716-446655500001', 1700, 850),
('550e8400-e29b-41d4-a716-446655440022', '550e8400-e29b-41d4-a716-446655470007', '550e8400-e29b-41d4-a716-446655500002', 1800, 900),
('550e8400-e29b-41d4-a716-446655440023', '550e8400-e29b-41d4-a716-446655470008', '550e8400-e29b-41d4-a716-446655500003', 1900, 950),
('550e8400-e29b-41d4-a716-446655440024', '550e8400-e29b-41d4-a716-446655470009', '550e8400-e29b-41d4-a716-446655500004', 2000, 1000),
('550e8400-e29b-41d4-a716-446655440025', '550e8400-e29b-41d4-a716-446655470000', '550e8400-e29b-41d4-a716-446655500000', 2100, 1050),
('550e8400-e29b-41d4-a716-446655440026', '550e8400-e29b-41d4-a716-446655470001', '550e8400-e29b-41d4-a716-446655500001', 2200, 1100),
('550e8400-e29b-41d4-a716-446655440027', '550e8400-e29b-41d4-a716-446655470002', '550e8400-e29b-41d4-a716-446655500002', 2300, 1150),
('550e8400-e29b-41d4-a716-446655440028', '550e8400-e29b-41d4-a716-446655470003', '550e8400-e29b-41d4-a716-446655500003', 2400, 1200),
('550e8400-e29b-41d4-a716-446655440029', '550e8400-e29b-41d4-a716-446655470004', '550e8400-e29b-41d4-a716-446655500004', 2500, 1250),
('550e8400-e29b-41d4-a716-446655440030', '550e8400-e29b-41d4-a716-446655470005', '550e8400-e29b-41d4-a716-446655500000', 2600, 1300),
('550e8400-e29b-41d4-a716-446655440031', '550e8400-e29b-41d4-a716-446655470006', '550e8400-e29b-41d4-a716-446655500001', 2700, 1350),
('550e8400-e29b-41d4-a716-446655440032', '550e8400-e29b-41d4-a716-446655470007', '550e8400-e29b-41d4-a716-446655500002', 2800, 1400),
('550e8400-e29b-41d4-a716-446655440033', '550e8400-e29b-41d4-a716-446655470008', '550e8400-e29b-41d4-a716-446655500003', 2900, 1450),
('550e8400-e29b-41d4-a716-446655440034', '550e8400-e29b-41d4-a716-446655470009', '550e8400-e29b-41d4-a716-446655500004', 3000, 1500),
('550e8400-e29b-41d4-a716-446655440035', '550e8400-e29b-41d4-a716-446655470000', '550e8400-e29b-41d4-a716-446655500000', 3100, 1550),
('550e8400-e29b-41d4-a716-446655440036', '550e8400-e29b-41d4-a716-446655470001', '550e8400-e29b-41d4-a716-446655500001', 3200, 1600),
('550e8400-e29b-41d4-a716-446655440037', '550e8400-e29b-41d4-a716-446655470002', '550e8400-e29b-41d4-a716-446655500002', 3300, 1650),
('550e8400-e29b-41d4-a716-446655440038', '550e8400-e29b-41d4-a716-446655470003', '550e8400-e29b-41d4-a716-446655500003', 3400, 1700),
('550e8400-e29b-41d4-a716-446655440039', '550e8400-e29b-41d4-a716-446655470004', '550e8400-e29b-41d4-a716-446655500004', 3500, 1750),
('550e8400-e29b-41d4-a716-446655440040', '550e8400-e29b-41d4-a716-446655470005', '550e8400-e29b-41d4-a716-446655500000', 3600, 1800),
('550e8400-e29b-41d4-a716-446655440041', '550e8400-e29b-41d4-a716-446655470006', '550e8400-e29b-41d4-a716-446655500001', 3700, 1850),
('550e8400-e29b-41d4-a716-446655440042', '550e8400-e29b-41d4-a716-446655470007', '550e8400-e29b-41d4-a716-446655500002', 3800, 1900),
('550e8400-e29b-41d4-a716-446655440043', '550e8400-e29b-41d4-a716-446655470008', '550e8400-e29b-41d4-a716-446655500003', 3900, 1950),
('550e8400-e29b-41d4-a716-446655440044', '550e8400-e29b-41d4-a716-446655470009', '550e8400-e29b-41d4-a716-446655500004', 4000, 2000),
('550e8400-e29b-41d4-a716-446655440045', '550e8400-e29b-41d4-a716-446655470000', '550e8400-e29b-41d4-a716-446655500000', 4100, 2050),
('550e8400-e29b-41d4-a716-446655440046', '550e8400-e29b-41d4-a716-446655470001', '550e8400-e29b-41d4-a716-446655500001', 4200, 2100),
('550e8400-e29b-41d4-a716-446655440047', '550e8400-e29b-41d4-a716-446655470002', '550e8400-e29b-41d4-a716-446655500002', 4300, 2150),
('550e8400-e29b-41d4-a716-446655440048', '550e8400-e29b-41d4-a716-446655470003', '550e8400-e29b-41d4-a716-446655500003', 4400, 2200),
('550e8400-e29b-41d4-a716-446655440049', '550e8400-e29b-41d4-a716-446655470004', '550e8400-e29b-41d4-a716-446655500004', 4500, 2250),
('550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655470005', '550e8400-e29b-41d4-a716-446655500000', 4600, 2300),
('550e8400-e29b-41d4-a716-446655440051', '550e8400-e29b-41d4-a716-446655470006', '550e8400-e29b-41d4-a716-446655500001', 4700, 2350),
('550e8400-e29b-41d4-a716-446655440052', '550e8400-e29b-41d4-a716-446655470007', '550e8400-e29b-41d4-a716-446655500002', 4800, 2400),
('550e8400-e29b-41d4-a716-446655440053', '550e8400-e29b-41d4-a716-446655470008', '550e8400-e29b-41d4-a716-446655500003', 4900, 2450),
('550e8400-e29b-41d4-a716-446655440054', '550e8400-e29b-41d4-a716-446655470009', '550e8400-e29b-41d4-a716-446655500004', 5000, 2500),
('550e8400-e29b-41d4-a716-446655440055', '550e8400-e29b-41d4-a716-446655470000', '550e8400-e29b-41d4-a716-446655500000', 5100, 2550),
('550e8400-e29b-41d4-a716-446655440056', '550e8400-e29b-41d4-a716-446655470001', '550e8400-e29b-41d4-a716-446655500001', 5200, 2600),
('550e8400-e29b-41d4-a716-446655440057', '550e8400-e29b-41d4-a716-446655470002', '550e8400-e29b-41d4-a716-446655500002', 5300, 2650);




INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song)
VALUES
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440005'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440006'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440007'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440008'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440009'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440010'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440011'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440012'),
('550e8400-e29b-41d4-a716-446655480004', '550e8400-e29b-41d4-a716-446655440013'),
('550e8400-e29b-41d4-a716-446655480004', '550e8400-e29b-41d4-a716-446655440014'),
('550e8400-e29b-41d4-a716-446655480005', '550e8400-e29b-41d4-a716-446655440015'),
('550e8400-e29b-41d4-a716-446655480005', '550e8400-e29b-41d4-a716-446655440016'),
('550e8400-e29b-41d4-a716-446655480006', '550e8400-e29b-41d4-a716-446655440017'),
('550e8400-e29b-41d4-a716-446655480006', '550e8400-e29b-41d4-a716-446655440018'),
('550e8400-e29b-41d4-a716-446655480007', '550e8400-e29b-41d4-a716-446655440019'),
('550e8400-e29b-41d4-a716-446655480007', '550e8400-e29b-41d4-a716-446655440020'),
('550e8400-e29b-41d4-a716-446655480008', '550e8400-e29b-41d4-a716-446655440021'),
('550e8400-e29b-41d4-a716-446655480008', '550e8400-e29b-41d4-a716-446655440022'),
('550e8400-e29b-41d4-a716-446655480009', '550e8400-e29b-41d4-a716-446655440023'),
('550e8400-e29b-41d4-a716-446655480009', '550e8400-e29b-41d4-a716-446655440024'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440025'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440026'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440027'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440028'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440029'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440030'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440031'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440032'),
('550e8400-e29b-41d4-a716-446655480004', '550e8400-e29b-41d4-a716-446655440033'),
('550e8400-e29b-41d4-a716-446655480004', '550e8400-e29b-41d4-a716-446655440034'),
('550e8400-e29b-41d4-a716-446655480005', '550e8400-e29b-41d4-a716-446655440035'),
('550e8400-e29b-41d4-a716-446655480005', '550e8400-e29b-41d4-a716-446655440036'),
('550e8400-e29b-41d4-a716-446655480006', '550e8400-e29b-41d4-a716-446655440037'),
('550e8400-e29b-41d4-a716-446655480006', '550e8400-e29b-41d4-a716-446655440038'),
('550e8400-e29b-41d4-a716-446655480007', '550e8400-e29b-41d4-a716-446655440039'),
('550e8400-e29b-41d4-a716-446655480007', '550e8400-e29b-41d4-a716-446655440040'),
('550e8400-e29b-41d4-a716-446655480008', '550e8400-e29b-41d4-a716-446655440041'),
('550e8400-e29b-41d4-a716-446655480008', '550e8400-e29b-41d4-a716-446655440042'),
('550e8400-e29b-41d4-a716-446655480009', '550e8400-e29b-41d4-a716-446655440043'),
('550e8400-e29b-41d4-a716-446655480009', '550e8400-e29b-41d4-a716-446655440044'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440045'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440046'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440047'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440048'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440049'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440050'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440051'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440052'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440053'),
('550e8400-e29b-41d4-a716-446655480000', '550e8400-e29b-41d4-a716-446655440054'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440055'),
('550e8400-e29b-41d4-a716-446655480001', '550e8400-e29b-41d4-a716-446655440056'),
('550e8400-e29b-41d4-a716-446655480002', '550e8400-e29b-41d4-a716-446655440057'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440005'),
('550e8400-e29b-41d4-a716-446655480003', '550e8400-e29b-41d4-a716-446655440006'),
('550e8400-e29b-41d4-a716-446655480004', '550e8400-e29b-41d4-a716-446655440007'),
('550e8400-e29b-41d4-a716-446655480005', '550e8400-e29b-41d4-a716-446655440008'),
('550e8400-e29b-41d4-a716-446655480005', '550e8400-e29b-41d4-a716-446655440009'),
('550e8400-e29b-41d4-a716-446655480006', '550e8400-e29b-41d4-a716-446655440010'),
('550e8400-e29b-41d4-a716-446655480006', '550e8400-e29b-41d4-a716-446655440011'),
('550e8400-e29b-41d4-a716-446655480007', '550e8400-e29b-41d4-a716-446655440012'),
('550e8400-e29b-41d4-a716-446655480008', '550e8400-e29b-41d4-a716-446655440013'),
('550e8400-e29b-41d4-a716-446655480009', '550e8400-e29b-41d4-a716-446655440014');








INSERT INTO DOWNLOADED_SONG (id_song, email_downloader)
VALUES
('550e8400-e29b-41d4-a716-446655440005', 'user3@example.com'),
('550e8400-e29b-41d4-a716-446655440006', 'user7@example.com'),
('550e8400-e29b-41d4-a716-446655440007', 'user17@example.com'),
('550e8400-e29b-41d4-a716-446655440008', 'user23@example.com'),
('550e8400-e29b-41d4-a716-446655440009', 'user41@example.com'),
('550e8400-e29b-41d4-a716-446655440010', 'user3@example.com'),
('550e8400-e29b-41d4-a716-446655440011', 'user7@example.com'),
('550e8400-e29b-41d4-a716-446655440012', 'user17@example.com'),
('550e8400-e29b-41d4-a716-446655440013', 'user23@example.com'),
('550e8400-e29b-41d4-a716-446655440014', 'user41@example.com');


INSERT INTO PLAYLIST (id)
VALUES
('550e8400-e29b-41d4-a716-446655510000'),
('550e8400-e29b-41d4-a716-446655510001'),
('550e8400-e29b-41d4-a716-446655510002'),
('550e8400-e29b-41d4-a716-446655510003'),
('550e8400-e29b-41d4-a716-446655510004'),
('550e8400-e29b-41d4-a716-446655510005'),
('550e8400-e29b-41d4-a716-446655510006'),
('550e8400-e29b-41d4-a716-446655510007'),
('550e8400-e29b-41d4-a716-446655510008'),
('550e8400-e29b-41d4-a716-446655510009');


INSERT INTO CHART (tipe, id_playlist)
VALUES
('Daily Top 20', '550e8400-e29b-41d4-a716-446655510000'),
('Weekly Top 20', '550e8400-e29b-41d4-a716-446655510001'),
('Monthly Top 20', '550e8400-e29b-41d4-a716-446655510002'),
('Yearly Top 20', '550e8400-e29b-41d4-a716-446655510003');


INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
VALUES
('user1@example.com', '550e8400-e29b-41d4-a716-446655510004', 'Chill Vibes', 'A collection of relaxing tunes to unwind to.', 15, '2024-04-28', '550e8400-e29b-41d4-a716-446655510000', 450),
('user2@example.com', '550e8400-e29b-41d4-a716-446655510005', 'Workout Beats', 'Get pumped up with these high-energy tracks!', 20, '2024-04-28', '550e8400-e29b-41d4-a716-446655510001', 600),
('user3@example.com', '550e8400-e29b-41d4-a716-446655510006', 'Road Trip Jams', 'Perfect tunes for your next adventure on the open road.', 18, '2024-04-28', '550e8400-e29b-41d4-a716-446655510002', 540),
('user4@example.com', '550e8400-e29b-41d4-a716-446655510007', 'Study Focus', 'Instrumental tracks to help you concentrate while studying.', 12, '2024-04-28', '550e8400-e29b-41d4-a716-446655510003', 360),
('user5@example.com', '550e8400-e29b-41d4-a716-446655510008', 'Party Anthems', 'The ultimate playlist for your next party!', 25, '2024-04-28', '550e8400-e29b-41d4-a716-446655510004', 750);


INSERT INTO ROYALTI (id_pemilik_hak_cipta, id_song, jumlah)
VALUES
('550e8400-e29b-41d4-a716-446655460000', '550e8400-e29b-41d4-a716-446655440005', 100),
('550e8400-e29b-41d4-a716-446655460001', '550e8400-e29b-41d4-a716-446655440006', 120),
('550e8400-e29b-41d4-a716-446655460002', '550e8400-e29b-41d4-a716-446655440007', 90),
('550e8400-e29b-41d4-a716-446655460003', '550e8400-e29b-41d4-a716-446655440008', 110),
('550e8400-e29b-41d4-a716-446655460004', '550e8400-e29b-41d4-a716-446655440009', 130),
('550e8400-e29b-41d4-a716-446655460005', '550e8400-e29b-41d4-a716-446655440010', 95),
('550e8400-e29b-41d4-a716-446655460006', '550e8400-e29b-41d4-a716-446655440011', 105),
('550e8400-e29b-41d4-a716-446655460007', '550e8400-e29b-41d4-a716-446655440012', 115),
('550e8400-e29b-41d4-a716-446655460008', '550e8400-e29b-41d4-a716-446655440013', 85),
('550e8400-e29b-41d4-a716-446655460009', '550e8400-e29b-41d4-a716-446655440014', 125),
('550e8400-e29b-41d4-a716-446655460010', '550e8400-e29b-41d4-a716-446655440015', 100),
('550e8400-e29b-41d4-a716-446655460011', '550e8400-e29b-41d4-a716-446655440016', 120),
('550e8400-e29b-41d4-a716-446655460012', '550e8400-e29b-41d4-a716-446655440017', 90),
('550e8400-e29b-41d4-a716-446655460013', '550e8400-e29b-41d4-a716-446655440018', 110),
('550e8400-e29b-41d4-a716-446655460014', '550e8400-e29b-41d4-a716-446655440019', 130),
('550e8400-e29b-41d4-a716-446655460015', '550e8400-e29b-41d4-a716-446655440020', 95),
('550e8400-e29b-41d4-a716-446655460016', '550e8400-e29b-41d4-a716-446655440021', 105),
('550e8400-e29b-41d4-a716-446655460017', '550e8400-e29b-41d4-a716-446655440022', 115),
('550e8400-e29b-41d4-a716-446655460018', '550e8400-e29b-41d4-a716-446655440023', 85),
('550e8400-e29b-41d4-a716-446655460019', '550e8400-e29b-41d4-a716-446655440024', 125),
('550e8400-e29b-41d4-a716-446655460020', '550e8400-e29b-41d4-a716-446655440025', 100),
('550e8400-e29b-41d4-a716-446655460021', '550e8400-e29b-41d4-a716-446655440026', 120),
('550e8400-e29b-41d4-a716-446655460022', '550e8400-e29b-41d4-a716-446655440027', 90),
('550e8400-e29b-41d4-a716-446655460023', '550e8400-e29b-41d4-a716-446655440028', 110),
('550e8400-e29b-41d4-a716-446655460024', '550e8400-e29b-41d4-a716-446655440029', 130);


INSERT INTO AKUN_PLAY_USER_PLAYLIST (email_pemain, id_user_playlist, email_pembuat, waktu) 
VALUES 
('user6@example.com', '550e8400-e29b-41d4-a716-446655510004', 'user1@example.com', '2024-04-01 08:00:00'),
('user7@example.com', '550e8400-e29b-41d4-a716-446655510005', 'user2@example.com', '2024-04-01 09:30:00'),
('user8@example.com', '550e8400-e29b-41d4-a716-446655510006', 'user3@example.com', '2024-04-01 10:45:00'),
('user9@example.com', '550e8400-e29b-41d4-a716-446655510007', 'user4@example.com', '2024-04-01 12:15:00'),
('user10@example.com', '550e8400-e29b-41d4-a716-446655510008', 'user5@example.com', '2024-04-01 13:45:00'),
('user11@example.com', '550e8400-e29b-41d4-a716-446655510004', 'user1@example.com', '2024-04-02 08:30:00'),
('user12@example.com', '550e8400-e29b-41d4-a716-446655510005', 'user2@example.com', '2024-04-02 10:00:00'),
('user13@example.com', '550e8400-e29b-41d4-a716-446655510006', 'user3@example.com', '2024-04-02 11:15:00'),
('user14@example.com', '550e8400-e29b-41d4-a716-446655510007', 'user4@example.com', '2024-04-02 12:45:00'),
('user15@example.com', '550e8400-e29b-41d4-a716-446655510008', 'user5@example.com', '2024-04-02 14:00:00'),
('user16@example.com', '550e8400-e29b-41d4-a716-446655510004', 'user1@example.com', '2024-04-03 08:45:00'),
('user17@example.com', '550e8400-e29b-41d4-a716-446655510005', 'user2@example.com', '2024-04-03 10:30:00'),
('user18@example.com', '550e8400-e29b-41d4-a716-446655510006', 'user3@example.com', '2024-04-03 12:00:00'),
('user19@example.com', '550e8400-e29b-41d4-a716-446655510007', 'user4@example.com', '2024-04-03 13:30:00'),
('user20@example.com', '550e8400-e29b-41d4-a716-446655510008', 'user5@example.com', '2024-04-03 15:00:00');


INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
VALUES
('user1@example.com', '550e8400-e29b-41d4-a716-446655440005', '2024-04-01 08:00:00'),
('user2@example.com', '550e8400-e29b-41d4-a716-446655440006', '2024-04-01 09:15:00'),
('user3@example.com', '550e8400-e29b-41d4-a716-446655440007', '2024-04-01 10:30:00'),
('user4@example.com', '550e8400-e29b-41d4-a716-446655440008', '2024-04-01 11:45:00'),
('user5@example.com', '550e8400-e29b-41d4-a716-446655440009', '2024-04-01 13:00:00'),
('user6@example.com', '550e8400-e29b-41d4-a716-446655440010', '2024-04-01 14:15:00'),
('user7@example.com', '550e8400-e29b-41d4-a716-446655440011', '2024-04-01 15:30:00'),
('user8@example.com', '550e8400-e29b-41d4-a716-446655440012', '2024-04-01 16:45:00'),
('user9@example.com', '550e8400-e29b-41d4-a716-446655440013', '2024-04-01 18:00:00'),
('user10@example.com', '550e8400-e29b-41d4-a716-446655440014', '2024-04-01 19:15:00'),
('user11@example.com', '550e8400-e29b-41d4-a716-446655440015', '2024-04-01 20:30:00'),
('user12@example.com', '550e8400-e29b-41d4-a716-446655440016', '2024-04-01 21:45:00'),
('user13@example.com', '550e8400-e29b-41d4-a716-446655440017', '2024-04-01 08:00:00'),
('user14@example.com', '550e8400-e29b-41d4-a716-446655440018', '2024-04-01 09:15:00'),
('user15@example.com', '550e8400-e29b-41d4-a716-446655440019', '2024-04-01 10:30:00'),
('user16@example.com', '550e8400-e29b-41d4-a716-446655440020', '2024-04-01 11:45:00'),
('user17@example.com', '550e8400-e29b-41d4-a716-446655440021', '2024-04-01 13:00:00'),
('user18@example.com', '550e8400-e29b-41d4-a716-446655440022', '2024-04-01 14:15:00'),
('user19@example.com', '550e8400-e29b-41d4-a716-446655440023', '2024-04-01 15:30:00'),
('user20@example.com', '550e8400-e29b-41d4-a716-446655440024', '2024-04-01 16:45:00'),
('user21@example.com', '550e8400-e29b-41d4-a716-446655440025', '2024-04-01 18:00:00'),
('user22@example.com', '550e8400-e29b-41d4-a716-446655440026', '2024-04-01 19:15:00'),
('user23@example.com', '550e8400-e29b-41d4-a716-446655440027', '2024-04-01 20:30:00'),
('user24@example.com', '550e8400-e29b-41d4-a716-446655440028', '2024-04-01 21:45:00'),
('user25@example.com', '550e8400-e29b-41d4-a716-446655440029', '2024-04-01 08:00:00'),
('user26@example.com', '550e8400-e29b-41d4-a716-446655440030', '2024-04-01 09:15:00'),
('user27@example.com', '550e8400-e29b-41d4-a716-446655440031', '2024-04-01 10:30:00'),
('user28@example.com', '550e8400-e29b-41d4-a716-446655440032', '2024-04-01 11:45:00'),
('user29@example.com', '550e8400-e29b-41d4-a716-446655440033', '2024-04-01 13:00:00'),
('user30@example.com', '550e8400-e29b-41d4-a716-446655440034', '2024-04-01 14:15:00'),
('user31@example.com', '550e8400-e29b-41d4-a716-446655440035', '2024-04-01 15:30:00'),
('user32@example.com', '550e8400-e29b-41d4-a716-446655440036', '2024-04-01 16:45:00'),
('user33@example.com', '550e8400-e29b-41d4-a716-446655440037', '2024-04-01 18:00:00'),
('user34@example.com', '550e8400-e29b-41d4-a716-446655440038', '2024-04-01 19:15:00'),
('user35@example.com', '550e8400-e29b-41d4-a716-446655440039', '2024-04-01 20:30:00'),
('user36@example.com', '550e8400-e29b-41d4-a716-446655440040', '2024-04-01 21:45:00'),
('user37@example.com', '550e8400-e29b-41d4-a716-446655440041', '2024-04-01 08:00:00'),
('user38@example.com', '550e8400-e29b-41d4-a716-446655440042', '2024-04-01 09:15:00'),
('user39@example.com', '550e8400-e29b-41d4-a716-446655440043', '2024-04-01 10:30:00'),
('user40@example.com', '550e8400-e29b-41d4-a716-446655440044', '2024-04-01 11:45:00'),
('user41@example.com', '550e8400-e29b-41d4-a716-446655440045', '2024-04-01 13:00:00'),
('user42@example.com', '550e8400-e29b-41d4-a716-446655440046', '2024-04-01 14:15:00'),
('user43@example.com', '550e8400-e29b-41d4-a716-446655440047', '2024-04-01 15:30:00'),
('user44@example.com', '550e8400-e29b-41d4-a716-446655440048', '2024-04-01 16:45:00'),
('user45@example.com', '550e8400-e29b-41d4-a716-446655440049', '2024-04-01 18:00:00'),
('user46@example.com', '550e8400-e29b-41d4-a716-446655440050', '2024-04-01 19:15:00'),
('user47@example.com', '550e8400-e29b-41d4-a716-446655440051', '2024-04-01 20:30:00'),
('user48@example.com', '550e8400-e29b-41d4-a716-446655440052', '2024-04-01 21:45:00'),
('user49@example.com', '550e8400-e29b-41d4-a716-446655440053', '2024-04-01 08:00:00'),
('user50@example.com', '550e8400-e29b-41d4-a716-446655440054', '2024-04-01 09:15:00'),
('user1@example.com', '550e8400-e29b-41d4-a716-446655440005', '2024-04-01 10:30:00'),
('user2@example.com', '550e8400-e29b-41d4-a716-446655440006', '2024-04-01 11:45:00'),
('user3@example.com', '550e8400-e29b-41d4-a716-446655440007', '2024-04-01 13:00:00'),
('user4@example.com', '550e8400-e29b-41d4-a716-446655440008', '2024-04-01 14:15:00'),
('user5@example.com', '550e8400-e29b-41d4-a716-446655440009', '2024-04-01 15:30:00'),
('user6@example.com', '550e8400-e29b-41d4-a716-446655440010', '2024-04-01 16:45:00'),
('user7@example.com', '550e8400-e29b-41d4-a716-446655440011', '2024-04-01 18:00:00'),
('user8@example.com', '550e8400-e29b-41d4-a716-446655440012', '2024-04-01 19:15:00'),
('user9@example.com', '550e8400-e29b-41d4-a716-446655440013', '2024-04-01 20:30:00'),
('user10@example.com', '550e8400-e29b-41d4-a716-446655440014', '2024-04-01 21:45:00'),
('user11@example.com', '550e8400-e29b-41d4-a716-446655440015', '2024-04-01 08:00:00'),
('user12@example.com', '550e8400-e29b-41d4-a716-446655440016', '2024-04-01 09:15:00'),
('user13@example.com', '550e8400-e29b-41d4-a716-446655440017', '2024-04-01 10:30:00'),
('user14@example.com', '550e8400-e29b-41d4-a716-446655440018', '2024-04-01 11:45:00'),
('user15@example.com', '550e8400-e29b-41d4-a716-446655440019', '2024-04-01 13:00:00'),
('user16@example.com', '550e8400-e29b-41d4-a716-446655440020', '2024-04-01 14:15:00'),
('user17@example.com', '550e8400-e29b-41d4-a716-446655440021', '2024-04-01 15:30:00'),
('user18@example.com', '550e8400-e29b-41d4-a716-446655440022', '2024-04-01 16:45:00'),
('user19@example.com', '550e8400-e29b-41d4-a716-446655440023', '2024-04-01 18:00:00'),
('user20@example.com', '550e8400-e29b-41d4-a716-446655440024', '2024-04-01 19:15:00'),
('user21@example.com', '550e8400-e29b-41d4-a716-446655440025', '2024-04-01 20:30:00'),
('user22@example.com', '550e8400-e29b-41d4-a716-446655440026', '2024-04-01 21:45:00'),
('user23@example.com', '550e8400-e29b-41d4-a716-446655440027', '2024-04-01 08:00:00'),
('user24@example.com', '550e8400-e29b-41d4-a716-446655440028', '2024-04-01 09:15:00'),
('user25@example.com', '550e8400-e29b-41d4-a716-446655440029', '2024-04-01 10:30:00'),
('user26@example.com', '550e8400-e29b-41d4-a716-446655440030', '2024-04-01 11:45:00'),
('user27@example.com', '550e8400-e29b-41d4-a716-446655440031', '2024-04-01 13:00:00'),
('user28@example.com', '550e8400-e29b-41d4-a716-446655440032', '2024-04-01 14:15:00'),
('user29@example.com', '550e8400-e29b-41d4-a716-446655440033', '2024-04-01 15:30:00'),
('user30@example.com', '550e8400-e29b-41d4-a716-446655440034', '2024-04-01 16:45:00'),
('user31@example.com', '550e8400-e29b-41d4-a716-446655440035', '2024-04-01 18:00:00'),
('user32@example.com', '550e8400-e29b-41d4-a716-446655440036', '2024-04-01 19:15:00'),
('user33@example.com', '550e8400-e29b-41d4-a716-446655440037', '2024-04-01 20:30:00'),
('user34@example.com', '550e8400-e29b-41d4-a716-446655440038', '2024-04-01 21:45:00'),
('user35@example.com', '550e8400-e29b-41d4-a716-446655440039', '2024-04-01 08:00:00'),
('user36@example.com', '550e8400-e29b-41d4-a716-446655440040', '2024-04-01 09:15:00'),
('user37@example.com', '550e8400-e29b-41d4-a716-446655440041', '2024-04-01 10:30:00'),
('user38@example.com', '550e8400-e29b-41d4-a716-446655440042', '2024-04-01 11:45:00'),
('user39@example.com', '550e8400-e29b-41d4-a716-446655440043', '2024-04-01 13:00:00'),
('user40@example.com', '550e8400-e29b-41d4-a716-446655440044', '2024-04-01 14:15:00'),
('user41@example.com', '550e8400-e29b-41d4-a716-446655440045', '2024-04-01 15:30:00'),
('user42@example.com', '550e8400-e29b-41d4-a716-446655440046', '2024-04-01 16:45:00'),
('user43@example.com', '550e8400-e29b-41d4-a716-446655440047', '2024-04-01 18:00:00'),
('user44@example.com', '550e8400-e29b-41d4-a716-446655440048', '2024-04-01 19:15:00'),
('user45@example.com', '550e8400-e29b-41d4-a716-446655440049', '2024-04-01 20:30:00'),
('user46@example.com', '550e8400-e29b-41d4-a716-446655440050', '2024-04-01 21:45:00'),
('user47@example.com', '550e8400-e29b-41d4-a716-446655440051', '2024-04-01 08:00:00'),
('user48@example.com', '550e8400-e29b-41d4-a716-446655440052', '2024-04-01 09:15:00'),
('user49@example.com', '550e8400-e29b-41d4-a716-446655440053', '2024-04-01 10:30:00'),
('user50@example.com', '550e8400-e29b-41d4-a716-446655440054', '2024-04-01 11:45:00');


INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
VALUES
('550e8400-e29b-41d4-a716-446655510000', '550e8400-e29b-41d4-a716-446655440005'),
('550e8400-e29b-41d4-a716-446655510000', '550e8400-e29b-41d4-a716-446655440006'),
('550e8400-e29b-41d4-a716-446655510001', '550e8400-e29b-41d4-a716-446655440007'),
('550e8400-e29b-41d4-a716-446655510001', '550e8400-e29b-41d4-a716-446655440008'),
('550e8400-e29b-41d4-a716-446655510002', '550e8400-e29b-41d4-a716-446655440009'),
('550e8400-e29b-41d4-a716-446655510002', '550e8400-e29b-41d4-a716-446655440010'),
('550e8400-e29b-41d4-a716-446655510003', '550e8400-e29b-41d4-a716-446655440011'),
('550e8400-e29b-41d4-a716-446655510003', '550e8400-e29b-41d4-a716-446655440012'),
('550e8400-e29b-41d4-a716-446655510004', '550e8400-e29b-41d4-a716-446655440013'),
('550e8400-e29b-41d4-a716-446655510004', '550e8400-e29b-41d4-a716-446655440014'),
('550e8400-e29b-41d4-a716-446655510005', '550e8400-e29b-41d4-a716-446655440015'),
('550e8400-e29b-41d4-a716-446655510005', '550e8400-e29b-41d4-a716-446655440016'),
('550e8400-e29b-41d4-a716-446655510006', '550e8400-e29b-41d4-a716-446655440017'),
('550e8400-e29b-41d4-a716-446655510006', '550e8400-e29b-41d4-a716-446655440018'),
('550e8400-e29b-41d4-a716-446655510007', '550e8400-e29b-41d4-a716-446655440019'),
('550e8400-e29b-41d4-a716-446655510007', '550e8400-e29b-41d4-a716-446655440020'),
('550e8400-e29b-41d4-a716-446655510008', '550e8400-e29b-41d4-a716-446655440021'),
('550e8400-e29b-41d4-a716-446655510008', '550e8400-e29b-41d4-a716-446655440022'),
('550e8400-e29b-41d4-a716-446655510009', '550e8400-e29b-41d4-a716-446655440023'),
('550e8400-e29b-41d4-a716-446655510009', '550e8400-e29b-41d4-a716-446655440024'),
('550e8400-e29b-41d4-a716-446655510000', '550e8400-e29b-41d4-a716-446655440025'),
('550e8400-e29b-41d4-a716-446655510000', '550e8400-e29b-41d4-a716-446655440026'),
('550e8400-e29b-41d4-a716-446655510001', '550e8400-e29b-41d4-a716-446655440027'),
('550e8400-e29b-41d4-a716-446655510001', '550e8400-e29b-41d4-a716-446655440028'),
('550e8400-e29b-41d4-a716-446655510002', '550e8400-e29b-41d4-a716-446655440029'),
('550e8400-e29b-41d4-a716-446655510002', '550e8400-e29b-41d4-a716-446655440030'),
('550e8400-e29b-41d4-a716-446655510003', '550e8400-e29b-41d4-a716-446655440031'),
('550e8400-e29b-41d4-a716-446655510003', '550e8400-e29b-41d4-a716-446655440032'),
('550e8400-e29b-41d4-a716-446655510004', '550e8400-e29b-41d4-a716-446655440033'),
('550e8400-e29b-41d4-a716-446655510004', '550e8400-e29b-41d4-a716-446655440034'),
('550e8400-e29b-41d4-a716-446655510005', '550e8400-e29b-41d4-a716-446655440035'),
('550e8400-e29b-41d4-a716-446655510005', '550e8400-e29b-41d4-a716-446655440036'),
('550e8400-e29b-41d4-a716-446655510006', '550e8400-e29b-41d4-a716-446655440037'),
('550e8400-e29b-41d4-a716-446655510006', '550e8400-e29b-41d4-a716-446655440038'),
('550e8400-e29b-41d4-a716-446655510007', '550e8400-e29b-41d4-a716-446655440039'),
('550e8400-e29b-41d4-a716-446655510007', '550e8400-e29b-41d4-a716-446655440040'),
('550e8400-e29b-41d4-a716-446655510008', '550e8400-e29b-41d4-a716-446655440041'),
('550e8400-e29b-41d4-a716-446655510008', '550e8400-e29b-41d4-a716-446655440042'),
('550e8400-e29b-41d4-a716-446655510009', '550e8400-e29b-41d4-a716-446655440043'),
('550e8400-e29b-41d4-a716-446655510009', '550e8400-e29b-41d4-a716-446655440044'),
('550e8400-e29b-41d4-a716-446655510000', '550e8400-e29b-41d4-a716-446655440045'),
('550e8400-e29b-41d4-a716-446655510000', '550e8400-e29b-41d4-a716-446655440046'),
('550e8400-e29b-41d4-a716-446655510001', '550e8400-e29b-41d4-a716-446655440047'),
('550e8400-e29b-41d4-a716-446655510001', '550e8400-e29b-41d4-a716-446655440048'),
('550e8400-e29b-41d4-a716-446655510002', '550e8400-e29b-41d4-a716-446655440049'),
('550e8400-e29b-41d4-a716-446655510002', '550e8400-e29b-41d4-a716-446655440050'),
('550e8400-e29b-41d4-a716-446655510003', '550e8400-e29b-41d4-a716-446655440051'),
('550e8400-e29b-41d4-a716-446655510003', '550e8400-e29b-41d4-a716-446655440052'),
('550e8400-e29b-41d4-a716-446655510004', '550e8400-e29b-41d4-a716-446655440053'),
('550e8400-e29b-41d4-a716-446655510004', '550e8400-e29b-41d4-a716-446655440054'),
('550e8400-e29b-41d4-a716-446655510005', '550e8400-e29b-41d4-a716-446655440055'),
('550e8400-e29b-41d4-a716-446655510005', '550e8400-e29b-41d4-a716-446655440056'),
('550e8400-e29b-41d4-a716-446655510006', '550e8400-e29b-41d4-a716-446655440057');