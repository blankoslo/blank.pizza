import enum

class RSVP(str, enum.Enum):
  attending = "attending"
  not_attending = "not attending"
  unanswered = "unanswered"