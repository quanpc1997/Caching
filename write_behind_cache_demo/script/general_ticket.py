from config.postgres_config import get_single_db
from src.model import Ticket
import asyncio

async def generate_tickets(db, event_id, rows, seats_per_row):
    """
    Tạo danh sách vé với số ghế
    """
    tickets = []
    for row in range(1, rows + 1):
        for seat in range(1, seats_per_row + 1):
            seat_number = f"{chr(64 + row)}{seat}"  # Ví dụ: A1, A2

            tickets.append(Ticket(
                event_id = event_id,
                seat_number = seat_number,
            ))
    db.add_all(tickets)
    await db.commit()


async def main():
    db = await get_single_db()
    await generate_tickets(db, "EV123", rows=100, seats_per_row=100)


if __name__ == "__main__":
    asyncio.run(main())
    print("Vé đã được tạo thành công!")
