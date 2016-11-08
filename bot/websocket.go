package main

import (
	"fmt"
	"log"
	"os"
  "strings"
	"encoding/base64"
	"encoding/json"

	"github.com/ddliu/go-httpclient"
  "github.com/nlopes/slack"
  "github.com/blankoslo/blank.pizza/common"
)

type CloudinaryResponse struct {
    PublicID    string `json:"public_id"`
}

func main() {
	var api = slack.New(os.Getenv("SLACK_TOKEN"))
	logger := log.New(os.Stdout, "slack-bot: ", log.Lshortfile|log.LstdFlags)
	slack.SetLogger(logger)
	api.SetDebug(true)

	rtm := api.NewRTM()
	go rtm.ManageConnection()

	httpclient.Defaults(httpclient.Map {
        "Authorization": fmt.Sprintf("Bearer %s", os.Getenv("SLACK_TOKEN")),
    })

Loop:
	for {
		select {
		case msg := <-rtm.IncomingEvents:
			switch ev := msg.Data.(type) {
			case *slack.MessageEvent:
				fmt.Printf("Message received: %v\n", ev)

				if(ev.File != nil){
					common.SendSlackMessage(ev.Channel, fmt.Sprintf("Takk for fil, <@%s> 👍", ev.File.User))
					res, _ := httpclient.Get(ev.File.URLPrivateDownload, nil)
					bodyBytes, _ := res.ReadAll()
					b64 := base64.StdEncoding.EncodeToString([]byte(bodyBytes))
					base := "data:image;base64,"

					resp, _ := httpclient.Post("https://api.cloudinary.com/v1_1/blank/image/upload", map[string]string {
        			"file": base + b64,
							"upload_preset": "blank.pizza",
    			})
		
					cloudBytes, _ := resp.ReadAll()
					var f CloudinaryResponse
					json.Unmarshal(cloudBytes, &f)
					common.SaveImage(f.PublicID, ev.File.User, ev.File.Title)
				}

        invitedSlackIDs := common.GetInvitedUsers()
        userIsInvited := common.StringInSlice(ev.User, invitedSlackIDs)

        if(userIsInvited) {
          if(strings.ToLower(ev.Text) == "ja") {
            common.Rsvp(ev.User, "attending")
						common.SendSlackMessage(ev.Channel, "Sweet! 👍")
            common.FinalizeInvitationIfComplete()
          } else if (strings.ToLower(ev.Text) == "nei") {
            common.Rsvp(ev.User, "not attending")
						common.SendSlackMessage(ev.Channel, "Ok 😏")
            common.InviteIfNeeded()
          } else {
						common.SendSlackMessage(ev.Channel, "Hehe jeg er litt dum, jeg. Skjønner jeg ikke helt hva du mener 😳. Kan du være med? (ja/nei)")
          }
        }

			case *slack.InvalidAuthEvent:
				fmt.Printf("Invalid credentials")
				break Loop

			default:

				// Ignore other events..
				// fmt.Printf("Unexpected: %v\n", msg.Data)
			}
		}
	}
}
