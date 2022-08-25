import enum

class Age(str, enum.Enum):
  New = "New"
  Old = "Old"

class RSVP(str, enum.Enum):
  attending = "attending"
  not_attending = "not attending"
  unanswered = "unanswered"