DROP TABLE IF EXISTS users;

CREATE TABLE users
(
  user_id TEXT UNIQUE PRIMARY KEY NOT NULL,
  second_id TEXT UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  mm_username TEXT UNIQUE,
  project TEXT NOT NULL,
  administrator BOOLEAN DEFAULT 0
);

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );
