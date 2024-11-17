import redis.asyncio as aioredis

from .general_config import config
from .postgres_config import get_single_db
from sqlalchemy import text
from loguru import logger

# Kết nối Redis
redis_client = aioredis.Redis(host=config.redis_host, port=config.redis_post, db=config.redis_db, decode_responses=True)


async def reserve_ticket(event_id, ticket_id, user_id):
    """
    Đặt vé và ghi thông tin vào Redis (async)
    """
    redis_key = f"event:{event_id}:tickets"

    # Kiểm tra vé đã bán chưa
    is_sold = await redis_client.sismember(redis_key, ticket_id)
    if is_sold:
        return {"status": "error", "message": "Vé đã được bán"}

    # Đánh dấu vé đã được giữ chỗ
    await redis_client.sadd(redis_key, ticket_id)

    # Lưu thông tin cần đồng bộ
    await redis_client.hset("unsynced_tickets", ticket_id, f"{event_id},{user_id}")

    return {"status": "success", "message": "Đặt vé thành công", "ticket_id": ticket_id}


async def load_tickets_to_redis(event_id):
    db = await get_single_db()
    result = await db.execute(
        text(f"SELECT seat_number FROM event_management.tickets WHERE event_id = '{event_id}' AND status = 'available'")
    )

    available_tickets = [row[0] for row in result.fetchall()]
    logger.info(f"There are available {len(available_tickets)} tickets")
    redis_key = f"event:{event_id}:tickets"
    for seat in available_tickets:
        await redis_client.sadd(redis_key, seat)
    logger.info(f"Load available {len(available_tickets)} tickets to redis successful")
    logger.debug(f"{redis_key} = {await redis_client.smembers(redis_key)}")


