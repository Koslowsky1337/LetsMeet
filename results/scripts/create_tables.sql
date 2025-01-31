-- SQL-Skript zur Erstellung der Tabellenstruktur (vollständig aktualisiert)

-- Tabelle: Users
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    street VARCHAR(100),
    house_number VARCHAR(20),
    postal_code VARCHAR(20),
    city VARCHAR(100),
    phone TEXT,
    gender VARCHAR(50),
    interested_in TEXT,
    birthdate DATE
);

-- Tabelle: Hobbies
CREATE TABLE Hobbies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Tabelle: UserHobbies (Zwischentabelle)
CREATE TABLE UserHobbies (
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    hobby_id INT REFERENCES Hobbies(id) ON DELETE CASCADE,
    priority INT CHECK (priority BETWEEN -100 AND 100),
    PRIMARY KEY (user_id, hobby_id)
);

-- Tabelle: Likes
CREATE TABLE Likes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    liked_user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    status VARCHAR(50),
    timestamp TIMESTAMP
);

-- Tabelle: Messages
CREATE TABLE Messages (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES Users(id) ON DELETE CASCADE,
    receiver_id INT REFERENCES Users(id) ON DELETE CASCADE,
    conversation_id INT,
    message TEXT,
    timestamp TIMESTAMP
);

-- Tabelle: ProfilePictures
CREATE TABLE ProfilePictures (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    image_data BYTEA
);

-- Tabelle: AdditionalPhotos
CREATE TABLE AdditionalPhotos (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    image_data BYTEA,
    link TEXT
);