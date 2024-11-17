from confluent_kafka import Consumer, KafkaException, KafkaError
from config.postgres_config import get_single_db
import json

class KafkaConsumer:
    def __init__(self, config, group_id='python-consumer-group', topic='test_topic'):
        self.conf = {
            'bootstrap.servers': config.kafka_bootstrap_server,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'  # Bắt đầu từ đầu nếu chưa có offset
        }
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([topic])

    async def consume_messages(self):
        """Lắng nghe và in các message nhận được từ Kafka"""
        db = await get_single_db()
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)  # Thời gian chờ khi không có message
                if msg is None:
                    continue  # Không có message mới
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print(f"End of partition {msg.partition()} reached at offset {msg.offset()}")
                    else:
                        raise KafkaException(msg.error())
                else:
                    data = json.loads(msg.value().decode('utf-8'))
                    print(f"Received message: {data}, type = {type(data)}")
                    try:
                        """
                        TODO: 
                        - Code thêm logic ghi dữ liệu vào DB. 
                        - Nếu ghi vào DB thành công: gửi message sang một kafka topic khác.
                        - Nếu ghi vào DB thất bại: Cập nhật lại trạng thái của ticket đó trong redis
                        """
                        pass
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        await db.rollback()

        except KeyboardInterrupt:
            print("Aborted by user")
        finally:
            self.consumer.close()

    def close(self):
        """Đóng consumer khi không còn cần thiết"""
        self.consumer.close()
