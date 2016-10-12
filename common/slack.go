package common

import (
	"log"
  "fmt"
  "os"
  "github.com/nlopes/slack"
)

var api = slack.New(os.Getenv("SLACK_TOKEN"))

func getSlackUsers() []slack.User {
  allUsers, err := api.GetUsers()
  if err != nil {
    log.Fatal(err)
  }

  var employeeUsers []slack.User

  for _,user := range allUsers {
    if(!user.Deleted && !user.IsBot && !user.IsRestricted && user.Name != "slackbot"){
        employeeUsers = append(employeeUsers, user)
    }
  }

  return employeeUsers
}

func SendSlackMessage(channelID, text string) {
  params := slack.PostMessageParameters{}
  params.AsUser = true
  channelID, _, err := api.PostMessage(channelID, text, params)
    if err != nil {
      fmt.Printf("%s\n", err)
      return
    }
}
