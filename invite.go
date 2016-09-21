package main

import (
  "fmt"
  "os"
  "log"
	"database/sql"

  _ "github.com/lib/pq"
  //"github.com/nlopes/slack"
)

func envOr(key, value string) (string) {
  if (os.Getenv(key) != "") {return os.Getenv(key)}
  return value
}

var dbuser = envOr("dbuser", "ftsqrcla")
var dbname = envOr("dbname", "ftsqrcla")
var dbpass = envOr("dbpass", "7rg83W5BLvM9XNrnPUZNtl4cagEu6fEr")
var dbhost = envOr("dbhost", "horton.elephantsql.com")

func main() {
  dburl := fmt.Sprintf("user=%s dbname=%s password=%s host=%s sslmode=verify-full", dbuser, dbname, dbpass, dbhost)
  //fmt.Printf(dburl)
  db, err := sql.Open("postgres", dburl)
	if err != nil {
		log.Fatal(err)
	}

  rows, err := db.Query("SELECT slack_id, current_username FROM slack_users")

  var (
  	slackID string
  	currentUsername string
  )

  defer rows.Close()
  for rows.Next() {
	  err := rows.Scan(&slackID, &currentUsername)
	  if err != nil {
		  log.Fatal(err)
	  }
	log.Println(slackID, currentUsername)
  }


}
