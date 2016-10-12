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
  eventID, timestamp, place, numberOfAlreadyInvited := getEventInNeedOfInvitations()
  if(eventID != "") {
    syncDbWithSlack()
    numberOfUsersToInvite := PeoplePerEvent - numberOfAlreadyInvited
    randomUsers := getUsersToInvite(numberOfUsersToInvite, eventID)

    saveInvitations(randomUsers, eventID)

    for _,user := range randomUsers {
      SendSlackMessage(user, fmt.Sprintf("Du er invitert til 🍕 på %s, %s. Kan du? (ja/nei)", place, timestamp.Format("02. jan kl 15:04")))
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
      message += fmt.Sprintf("@%s", username)
      if (i < len(usernames) - 1) { message += ", " }
    }
    message += fmt.Sprintf("! Dere skal spise 🍕 på %s, %s", place, timestamp.Format("02. jan kl 15:04"))
    SendSlackMessage(pizzaChannel, message)
  }
}

func GetInvitedUsers() []string {
  return getInvitedUsers()
}

func syncDbWithSlack(){
  slackUsers := getSlackUsers();
  updateUsers(slackUsers);
}
