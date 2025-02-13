-- -------------------------------------------------------
-- 1) Alle Tabellen droppen
-- -------------------------------------------------------
DROP TABLE IF EXISTS 
    Friendships,
    Likes,
    Messages,
    ProfilePictures,
    AdditionalPhotos,
    UserHobbies,
    Hobbies,
    Addresses,
    Users
CASCADE;

-- -------------------------------------------------------
-- 2) Addresses
-- -------------------------------------------------------
CREATE TABLE Addresses (
    address_id    SERIAL PRIMARY KEY,
    street        VARCHAR(100),
    house_number  VARCHAR(20),
    postal_code   VARCHAR(20),
    city          VARCHAR(100)
);

-- -------------------------------------------------------
-- 3) Users
-- -------------------------------------------------------
CREATE TABLE Users (
    user_id         SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    address_id      INT REFERENCES Addresses(address_id) ON DELETE CASCADE,
    phone           TEXT,
    gender          VARCHAR(50),
    interested_in   TEXT,
    birthdate       DATE
);

-- -------------------------------------------------------
-- 4) Hobbies
-- -------------------------------------------------------
CREATE TABLE Hobbies (
    hobby_id  SERIAL PRIMARY KEY,
    hobby     VARCHAR(255) NOT NULL UNIQUE
);

-- -------------------------------------------------------
-- 5) UserHobbies
-- -------------------------------------------------------
CREATE TABLE UserHobbies (
    user_id   INT REFERENCES Users(user_id) ON DELETE CASCADE,
    hobby_id  INT REFERENCES Hobbies(hobby_id) ON DELETE CASCADE,
    priority  INT CHECK (priority BETWEEN -100 AND 100),
    PRIMARY KEY (user_id, hobby_id)
);

-- -------------------------------------------------------
-- 6) Friendships
-- -------------------------------------------------------
CREATE TABLE Friendships (
    user_id1  INT NOT NULL,
    user_id2  INT NOT NULL,
    status    VARCHAR(50),
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- 7) Likes
-- -------------------------------------------------------
CREATE TABLE Likes (
    like_id        SERIAL PRIMARY KEY,
    user_id        INT REFERENCES Users(user_id) ON DELETE CASCADE,
    liked_user_id  INT REFERENCES Users(user_id) ON DELETE CASCADE,
    like_status    VARCHAR(50),
    like_time      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
-- 8) Messages
-- -------------------------------------------------------
CREATE TABLE Messages (
    message_id      SERIAL PRIMARY KEY,
    sender_id       INT REFERENCES Users(user_id) ON DELETE CASCADE,
    receiver_id     INT REFERENCES Users(user_id) ON DELETE CASCADE,
    conversation_id INT,
    message_text    TEXT,
    message_time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
-- 9) ProfilePictures
-- -------------------------------------------------------
CREATE TABLE ProfilePictures (
    profile_pic_id SERIAL PRIMARY KEY,
    user_id        INT REFERENCES Users(user_id) ON DELETE CASCADE,
    image_data     BYTEA
);

-- -------------------------------------------------------
-- 10) AdditionalPhotos
-- -------------------------------------------------------
CREATE TABLE AdditionalPhotos (
    add_pic_id   SERIAL PRIMARY KEY,
    user_id      INT REFERENCES Users(user_id) ON DELETE CASCADE,
    image_data   BYTEA,
    add_pic_link TEXT
);
