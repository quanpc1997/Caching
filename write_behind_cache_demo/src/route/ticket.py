from fastapi import APIRouter
from sqlalchemy import update
from loguru import logger

from config.caching_config import reserve_ticket, load_tickets_to_redis
from config.general_config import config
from config.kafka_producer import KafkaProducer

from src.model.body import TicketBody


ticket_router = APIRouter(prefix="/ticket")

reserve_kafka_producer = KafkaProducer(config)

@ticket_router.get("/load-to-redis")
async def load_to_redis():
    await load_tickets_to_redis(config.event_id)
    return "Ok"


@ticket_router.post("/buy")
async def buy_ticket(reserve_infor: TicketBody):
    result = await reserve_ticket(reserve_infor.event_id, reserve_infor.ticket_id, reserve_infor.user_id)
    logger.info(f"Result: {result}")
    data = reserve_infor.dict()
    if result["status"] != "error":
        reserve_kafka_producer.send_message(
            topic=config.reserve_redis_pg_topic,
            key=reserve_infor.event_id,
            value=reserve_infor.dict()
        )
    return result