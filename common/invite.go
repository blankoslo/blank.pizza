package common

import (
	"log"
  "fmt"
)

const PeoplePerEvent = 5
const pizzaChannel = "C2NC8DBN1"

func InviteIfNeeded() {
  eventID, timeStamp, place, numberOfAlreadyInvited := GetEventInNeedOfInvitations()
  fmt.Printf(eventID)
  if(eventID != "") {
    syncDbWithSlack()
    numberOfUsersToInvite := PeoplePerEvent - numberOfAlreadyInvited
    randomUsers := GetUsersToInvite(numberOfUsersToInvite, eventID)

    SaveInvitations(randomUsers, eventID)

    for _,user := range randomUsers {
      SendSlackMessage("U0A9R2Y1X", user + " er invitert til middag på " + place + " " + timeStamp + ". Kan du? (ja/nei)")
      log.Printf(user + " was invited to event on " + timeStamp)
    }
  } else {
    log.Printf("No users were invited")
  }
}

func FinalizeInvitationIfComplete() {
  eventID, timestamp, place := getEventReadyToFinalize()
  if(eventID != ""){
    var message = "Halloi! "
    syncDbWithSlack()
    usernames := getAttendingUsers(eventID)
    markEventAsFinalized(eventID)

    for i,username := range usernames {
      message += fmt.Sprintf("%s", username)
      if (i < len(usernames) - 1) { message += ", " }
    }
    message += fmt.Sprintf("er invitert til å spise på %s, %s", place, timestamp)
    SendSlackMessage(pizzaChannel, message)
  }


}

func syncDbWithSlack(){
  slackUsers := getSlackUsers();
  updateUsers(slackUsers);
}
