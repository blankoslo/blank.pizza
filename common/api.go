package common

import (
	"log"
  "fmt"
)

const PeoplePerEvent = 5
const replyDeadlineInHours = 24
const pizzaChannel = "C2NC8DBN1"

func Rsvp(slackID string, answer string) {
  rsvp(slackID, answer)
}

func InviteIfNeeded() {
  eventID, timestamp, place, numberOfAlreadyInvited := getEventInNeedOfInvitations()
  if(eventID != "") {
    totalNumberOfEmployees := syncDbWithSlackAndReturnCount()
    numberOfUsersToInvite := PeoplePerEvent - numberOfAlreadyInvited
    randomUsers := getUsersToInvite(numberOfUsersToInvite, eventID, totalNumberOfEmployees, PeoplePerEvent)

    saveInvitations(randomUsers, eventID)

    for _,user := range randomUsers {
      SendSlackMessage(user, fmt.Sprintf("Du er invitert til 🍕 på %s, %s. Kan du? (ja/nei)", place, timestamp.Format("02/01 kl 15:04")))
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
    syncDbWithSlackAndReturnCount()
    slackIDs := getAttendingUsers(eventID)
    markEventAsFinalized(eventID)

    for i,slackID := range slackIDs {
      message += fmt.Sprintf("<@%s>", slackID)
      if (i < len(slackIDs) - 1) { message += ", " }
    }
    message += fmt.Sprintf("! Dere skal spise 🍕 på %s, %s. Blank betaler!", place, timestamp.Format("02/01 kl 15:04"))
    SendSlackMessage(pizzaChannel, message)
  }
}

func GetInvitedUsers() []string {
  return getInvitedUsers()
}

func AutoReplyNo() {
  usersThatDidNotReply := autoReplyAfterDeadline(replyDeadlineInHours)

  for _,username := range usersThatDidNotReply {
    SendSlackMessage(username, "Neivel, da antar jeg du ikke er interessert. Håper du blir med neste gang!")
    log.Printf(username + " didn't answer. Setting rsvp to not attending.")
  }
  InviteIfNeeded()
}

func syncDbWithSlackAndReturnCount() int {
  slackUsers := getSlackUsers();
  updateUsers(slackUsers);
	return len(slackUsers)
}
