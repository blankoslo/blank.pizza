package common

import (
  "os"
)

func EnvOr(key, value string) (string) {
  if (os.Getenv(key) != "") {return os.Getenv(key)}
  return value
}
