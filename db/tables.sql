CREATE TABLE slack_users (
  slack_id TEXT NOT NULL PRIMARY KEY,
  current_username TEXT NOT NULL,
  first_seen DATETIME NOT NULL DEFAULT NOW()
);
