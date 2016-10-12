package common

import (
  "os"
)

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
