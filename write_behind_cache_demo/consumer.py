from config.kafka_consumer import KafkaConsumer
from config.general_config import config

consumer = KafkaConsumer(config, group_id="quanpc_consumer", topic=config.reserve_redis_pg_topic)
consumer.consume_messages()