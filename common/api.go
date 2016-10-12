package common

import (
	"log"
  "fmt"
)

const PeoplePerEvent = 5
const pizzaChannel = "C2NC8DBN1"

func Rsvp(slackID string, answer string) {
  rsvp(slackID, answer)
}

func InviteIfNeeded() {
  eventID, timestamp, place, numberOfAlreadyInvited := GetEventInNeedOfInvitations()
  fmt.Printf(eventID)
  if(eventID != "") {
    syncDbWithSlack()
    numberOfUsersToInvite := PeoplePerEvent - numberOfAlreadyInvited
    randomUsers := GetUsersToInvite(numberOfUsersToInvite, eventID)

    SaveInvitations(randomUsers, eventID)

    for _,user := range randomUsers {
      SendSlackMessage("U0A9R2Y1X", fmt.Sprintf("Du er invitert til 🍕 på %s, %s. Kan du? (ja/nei)", place, timestamp.Format("02. jan kl 15:04")))
      log.Printf(user + " was invited to event on " + timestamp.Format("02/01/06 kl 15:04"))
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
    message += fmt.Sprintf(" skal spise 🍕 på %s, %s", place, timestamp.Format("02. jan kl 15:04"))
    SendSlackMessage(pizzaChannel, message)
  }
}

func syncDbWithSlack(){
  slackUsers := getSlackUsers();
  updateUsers(slackUsers);
}
