CREATE EXTENSION "uuid-ossp";

CREATE TABLE slack_users (
  slack_id TEXT NOT NULL PRIMARY KEY,
  current_username TEXT NOT NULL,
  first_seen DATE NOT NULL DEFAULT NOW()
);

CREATE TABLE events (
  id TEXT PRIMARY KEY DEFAULT uuid_generate_v4(),
  time TIMESTAMP NOT NULL,
  place TEXT NOT NULL,
  finalized BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TYPE RSVP AS ENUM ('attending', 'not attending', 'unanswered');

CREATE TABLE invitations (
  event_id TEXT REFERENCES events (id),
  slack_id TEXT REFERENCES slack_users (slack_id),
  invited_at TIMESTAMP NOT NULL DEFAULT NOW(),
  rsvp RSVP NOT NULL DEFAULT 'unanswered',
  PRIMARY KEY (event_id, slack_id)
);
