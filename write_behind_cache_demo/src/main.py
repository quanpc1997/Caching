from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from loguru import logger

from config.general_config import config
from config.kafka_producer import KafkaProducer

from src.route.ticket import ticket_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Hello")
    yield
    logger.info("Bye bye")



app = FastAPI(docs_url="/docs", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_router)


