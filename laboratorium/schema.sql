DROP TABLE IF EXISTS post;

CREATE TABLE users
(
  --   id INTEGER PRIMARY KEY AUTOINCREMENT,
  id INTEGER NOT NULL,
  second_id INTEGER NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  mm_username TEXT UNIQUE NOT NULL,
  project TEXT NOT NULL,
  PRIMARY KEY(id, second_id)
);

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );
