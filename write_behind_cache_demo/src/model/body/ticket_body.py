from pydantic import BaseModel

class TicketBody(BaseModel):
    event_id: str = "EV123"
    ticket_id: str
    seat_number: str
    user_id: str
