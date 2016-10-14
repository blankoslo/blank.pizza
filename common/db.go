package common

import (
  "fmt"
  "os"
  "log"
	"database/sql"
  "time"

  "github.com/nlopes/slack"
  _ "github.com/lib/pq"
)

func envOr(key, value string) (string) {
  if (os.Getenv(key) != "") {return os.Getenv(key)}
  return value
}

var dbuser = envOr("dbuser", "kedqujopdsikse")
var dbname = envOr("dbname", "dahcjao9t5534p")
var dbpass = envOr("dbpass", "qrUu57g_MoaKAZhd0s20EV0WRt")
var dbhost = envOr("dbhost", "ec2-23-21-71-9.compute-1.amazonaws.com")

var dburl = fmt.Sprintf("user=%s dbname=%s password=%s host=%s", dbuser, dbname, dbpass, dbhost)
var db, err = sql.Open("postgres", dburl)

func updateUsers(users []slack.User) {
  var usersSQLValues string
  for i,user := range users {
    usersSQLValues += fmt.Sprintf("('%s', '%s')", user.ID, user.Name)
    if (i < len(users) - 1) { usersSQLValues += ", " }
  }

  db.Exec(fmt.Sprintf("INSERT INTO slack_users (slack_id, current_username) VALUES %s ON CONFLICT (slack_id) DO UPDATE SET current_username = EXCLUDED.current_username;", usersSQLValues))
  if err != nil {
    log.Fatal(err)
  }
}

func getUsersToInvite(numberOfUsers int, eventID string) []string {
  //TODO expand this with how many attended, and how many eligible for
  var userSlackIDs []string
  rows, err := db.Query(fmt.Sprintf("select * from (select distinct slack_users.slack_id from slack_users where not exists (select * from invitations where invitations.event_id = '%s' and invitations.slack_id = slack_users.slack_id)) as slack_id order by random() limit %d;", eventID, numberOfUsers))
  if err != nil {
    log.Fatal(err)
  }

  defer rows.Close()
  for rows.Next() {
    var slackID string
    if err := rows.Scan(&slackID); err != nil {
      log.Fatal(err)
    }
    userSlackIDs = append(userSlackIDs, slackID)
  }

  return userSlackIDs
}

func saveInvitations(slackIDs []string, eventID string) {
  var SQLValues string
  for i,slackID := range slackIDs {
    SQLValues += fmt.Sprintf("('%s', '%s')", eventID, slackID)
    if (i < len(slackIDs) - 1) { SQLValues += ", " }
  }

  db.Exec(fmt.Sprintf("INSERT INTO invitations (event_id, slack_id) VALUES %s;", SQLValues))
  if err != nil {
    log.Fatal(err)
  }
}

func getEventInNeedOfInvitations()(string, time.Time, string, int)  {
    var id, place string
    var timestamp time.Time
    var numberOfInvited int
    err := db.QueryRow(fmt.Sprintf("select id, time, place, count(event_id) as invited from events left outer join invitations on event_id = id and (rsvp = 'unanswered' or rsvp = 'attending') where time  < NOW() + interval '10 days' group by id having count(event_id) < %d;", PeoplePerEvent)).Scan(&id, &timestamp, &place, &numberOfInvited)
    switch {
      case err == sql.ErrNoRows:
              log.Printf("No upcoming events without invitations")
      case err != nil:
              log.Fatal(err)
      default:
              log.Printf("Event with ID  %s needs invitations \n", id)
    }

    return id, timestamp, place, numberOfInvited
}

func getInvitedUsers() []string {
    var userSlackIDs []string
    rows, err := db.Query("SELECT DISTINCT slack_id FROM invitations WHERE rsvp = 'unanswered';")

    if err != nil {
      log.Fatal(err)
    }

    defer rows.Close()
    for rows.Next() {
      var slackID string
      if err := rows.Scan(&slackID); err != nil {
        log.Fatal(err)
      }
      userSlackIDs = append(userSlackIDs, slackID)
    }

    return userSlackIDs
}

func rsvp(slackID string, answer string) {
  db.Exec(fmt.Sprintf("UPDATE invitations SET rsvp = '%s' WHERE slack_id = '%s' AND rsvp = 'unanswered';", answer, slackID))
  if err != nil {
    log.Fatal(err)
  }
}

func markEventAsFinalized(eventID string) {
  db.Exec(fmt.Sprintf("UPDATE events SET finalized = true WHERE id = '%s';", eventID))
  if err != nil {
    log.Fatal(err)
  }
}

func getEventReadyToFinalize()(string, time.Time, string) {
  var eventID, place string
  var timestamp time.Time
  err := db.QueryRow(fmt.Sprintf("select event_id, time, place from slack_users, invitations, events where invitations.slack_id = slack_users.slack_id and invitations.event_id = events.id and rsvp = 'attending' and not finalized group by event_id, time, place having count(event_id) = %d;", PeoplePerEvent)).Scan(&eventID, &timestamp, &place)
  switch {
    case err == sql.ErrNoRows:
      log.Printf("No events ready to finalize")
    case err != nil:
      log.Fatal(err)
    default:
      log.Printf("Event with ID %s is ready for finalizing \n", eventID)
  }
  return eventID, timestamp, place
}

func getAttendingUsers(eventID string) []string {
  var slackIDs []string
  rows, err := db.Query(fmt.Sprintf("SELECT slack_id FROM invitations WHERE rsvp = 'attending' and event_id = '%s';", eventID))

  if err != nil {
    log.Fatal(err)
  }

  defer rows.Close()
  for rows.Next() {
    var slackID string
    if err := rows.Scan(&slackID); err != nil {
      log.Fatal(err)
    }
    slackIDs = append(slackIDs, slackID)
  }
  return slackIDs
}

func autoReplyAfterDeadline(deadline int) []string {
  var slackUsernames []string
  rows, err := db.Query(fmt.Sprintf("update invitations set rsvp = 'not attending' where rsvp = 'unanswered' and invited_at < NOW() - interval '%d hours' returning slack_id;", deadline))
  if err != nil {
    log.Fatal(err)
  }

  defer rows.Close()
  for rows.Next() {
    var slackUsername string
    if err := rows.Scan(&slackUsername); err != nil {
      log.Fatal(err)
    }
    slackUsernames = append(slackUsernames, slackUsername)
  }
  return slackUsernames
}
