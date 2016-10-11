package common

import (
  "fmt"
  "os"
  "log"
	"database/sql"

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

func UpdateUsers(users []slack.User) {
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


func GetRandomUsers(numberOfUsers int) []string {
  //TODO expand this with how many attended, and how many eligible for
  var userSlackIDs []string
  rows, err := db.Query("select slack_id from slack_users order by random() limit 5;")

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

func SaveInvitations(slackIDs []string, eventID string) {
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

func GetEventInNeedOfInvitations()(string, string, string)  {
    var id, time, place string
    err := db.QueryRow("SELECT id, time, place FROM events WHERE time  < NOW() + interval '10 day' AND NOT EXISTS (SELECT * FROM invitations WHERE invitations.event_id = events.id)").Scan(&id, &time, &place)
    switch {
    case err == sql.ErrNoRows:
            log.Printf("No upcoming events without invitations")
    case err != nil:
            log.Fatal(err)
    default:
            log.Printf("Event with ID  %s needs invitations \n", id)
    }

    return id, time, place

}
