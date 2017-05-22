package main

import (
  "github.com/blankoslo/blank.pizza/common"
)

func main() {
    common.AutoReplyNo()
    common.InviteIfNeeded()
    common.SendReminders()
}
