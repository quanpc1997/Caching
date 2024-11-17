from sqlalchemy import (
    Column, String, Integer, TIMESTAMP, Enum, Index, UniqueConstraint
)
import enum

from config.postgres_config import Base

# Định nghĩa Enum cho cột 'status'
class TicketStatus(enum.Enum):
    available = "available"
    reserved = "reserved"
    sold = "sold"

# Định nghĩa bảng 'tickets'
class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = (
        UniqueConstraint('event_id', 'seat_number', name='uq_event_seat'),  # Constraint cho event_id và seat_number
        Index('ix_status_purchase_time', 'status', 'purchase_time'),        # Index cho status và purchase_time
        {'schema': 'event_management'}  # Định nghĩa schema
    )

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(50), nullable=False)  # ID sự kiện
    seat_number = Column(String(10))  # Số ghế (nếu có)
    status = Column(Enum(TicketStatus), default=TicketStatus.available)  # Trạng thái: available, reserved, sold
    user_id = Column(String(50))  # Người mua (nếu đã bán)
    purchase_time = Column(TIMESTAMP, default=None)  # Thời gian mua (nếu đã bán)

    def __repr__(self):
        return (f"<Ticket(ticket_id={self.ticket_id}, event_id='{self.event_id}', "
                f"seat_number='{self.seat_number}', status='{self.status}', "
                f"user_id='{self.user_id}', purchase_time='{self.purchase_time}')>")
