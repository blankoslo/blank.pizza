package main

import (
  "github.com/blankoslo/blank.pizza/common"
)

func main() {
  slackUsers := common.GetSlackUsers();
  common.UpdateUsers(slackUsers);

  randomUsers := common.GetRandomUsers(5)

  for _,user := range randomUsers {
    common.SendSlackMessage("U0A9R2Y1X", user + " er herved invitert til middah.")
  }
}
