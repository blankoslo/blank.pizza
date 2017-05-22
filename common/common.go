package common

import (
  "os"
  "time"
)

type Invitation struct {
    slackID string
    invitedAt time.Time
    remindedAt time.Time
}

func EnvOr(key, value string) (string) {
  if (os.Getenv(key) != "") {return os.Getenv(key)}
  return value
}

func StringInSlice(a string, list []string) bool {
    for _, b := range list {
        if b == a {
            return true
        }
    }
    return false
}
