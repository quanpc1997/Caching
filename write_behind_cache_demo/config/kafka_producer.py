from confluent_kafka import Producer
import json

class KafkaProducer:
    def __init__(self, config, client_id: str = "quanpc_demo"):
        self.conf = {
            'bootstrap.servers': config.kafka_bootstrap_server,
            'client.id': client_id
        }
        self.producer = Producer(self.conf)

    def delivery_report(self, err, msg):
        """Callback để xử lý khi message được gửi thành công hoặc thất bại"""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send_message(self, topic, key, value):
        """Gửi message vào Kafka"""
        self.producer.produce(topic, key=key, value=json.dumps(value), callback=self.delivery_report)
        self.producer.flush()

    def close(self):
        """Đảm bảo rằng tất cả message đã được gửi trước khi đóng"""
        self.producer.close()
