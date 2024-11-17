import asyncio
import redis.asyncio as aioredis

from .general_config import config
from .postgres_config import get_single_db

# Kết nối Redis
class Caching:

    def __init__(self):
        self.redis_client = aioredis.Redis(host=config.redis_host, port=config.redis_post, db=config.redis_db, decode_responses=True)


    async def reserve_ticket(self, event_id, ticket_id, user_id):
        """
        Đặt vé và ghi thông tin vào Redis (async)
        """
        redis_key = f"event:{event_id}:tickets"

        # Kiểm tra vé đã bán chưa
        is_sold = await self.redis_client.sismember(redis_key, ticket_id)
        if is_sold:
            return {"status": "error", "message": "Vé đã được bán"}

        # Đánh dấu vé đã được giữ chỗ
        await self.redis_client.sadd(redis_key, ticket_id)

        # Lưu thông tin cần đồng bộ
        await self.redis_client.hset("unsynced_tickets", ticket_id, f"{event_id},{user_id}")

        return {"status": "success", "message": "Đặt vé thành công", "ticket_id": ticket_id}

    async def load_tickets_to_redis(self, db, event_id):
        result = await db.execute(
            "SELECT seat_number FROM tickets WHERE event_id = %s AND status = 'available'", (event_id,)
        )

        available_tickets = [row[0] for row in db.fetchall()]
        redis_key = f"event:{event_id}:tickets"
        for seat in available_tickets:
            redis_client.sadd(redis_key, seat)


