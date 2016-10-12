package main

import (
  "github.com/blankoslo/blank.pizza/common"
)

func main() {
    common.InviteIfNeeded()
    //TODO check if someone didnt answer in 24h and auto-reply no
}
