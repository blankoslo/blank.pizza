package main

import (
  "log"
  "time"
  "github.com/blankoslo/blank.pizza/common"
)

func findNextDate() {
  time.Now()
}

func main() {

  id, time, place := common.GetEventInNeedOfInvitations()

  if(id != "") {
    slackUsers := common.GetSlackUsers();
    common.UpdateUsers(slackUsers);

    randomUsers := common.GetRandomUsers(5)

    common.SaveInvitations(randomUsers, id)

    for _,user := range randomUsers {
      common.SendSlackMessage("U0A9R2Y1X", user + " er invitert til middag på " + place + " " + time + ". Kan du? (ja/nei)")
      log.Printf(user + " was invited to event on " + time)
    }


  } else {
    log.Printf("No users were invited")
  }
}
