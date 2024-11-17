# Mô tả bài hoán

---

### Bối cảnh:
Một ứng dụng bán vé trực tuyến cho các sự kiện (như concert, thể thao). Khi người dùng mua vé, yêu cầu sẽ được ghi vào Redis cache trước để đảm bảo hiệu suất và đồng thời giảm tải cho database chính.

---

### Quy trình:
1. **Redis Cache**:
   - Lưu thông tin vé đã bán trong cache ngay khi giao dịch thành công.
   - Đánh dấu vé đã được giữ chỗ hoặc bán, tránh trường hợp bán trùng (overselling).

2. **Database (PostgreSQL)**:
   - Lưu thông tin vé lâu dài (persistent storage).
   - Worker định kỳ đồng bộ dữ liệu từ Redis sang database.

3. **Worker**:
   - Worker kiểm tra các giao dịch mới trong Redis và ghi vào database chính.

---

### Cấu trúc dữ liệu:
- Redis Key: `event:{event_id}:tickets`
  - Giá trị: Danh sách các vé đã bán (hoặc giữ chỗ).

- Redis Key: `unsynced_tickets`
  - Danh sách các vé cần đồng bộ.

---

### Mã nguồn:

#### Ghi thông tin vào Redis:
```python
import redis

# Kết nối Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def reserve_ticket(event_id, ticket_id, user_id):
    """
    Đặt vé và ghi thông tin vào Redis
    """
    redis_key = f"event:{event_id}:tickets"

    # Kiểm tra vé đã bán chưa
    if redis_client.sismember(redis_key, ticket_id):
        return {"status": "error", "message": "Vé đã được bán"}

    # Đánh dấu vé đã được giữ chỗ
    redis_client.sadd(redis_key, ticket_id)

    # Lưu thông tin cần đồng bộ
    redis_client.hset("unsynced_tickets", ticket_id, f"{event_id},{user_id}")
    
    return {"status": "success", "message": "Đặt vé thành công", "ticket_id": ticket_id}

# Ví dụ đặt vé
response = reserve_ticket(event_id=1, ticket_id="T123", user_id="U456")
print(response)
```

---

#### Đồng bộ với Database:
```python
import psycopg2

# Kết nối tới PostgreSQL
db_conn = psycopg2.connect(
    dbname="ticketing_db",
    user="user",
    password="password",
    host="localhost",
    port=5432
)

def sync_tickets_to_db():
    """
    Worker: Đồng bộ thông tin vé từ Redis sang PostgreSQL
    """
    cursor = db_conn.cursor()
    unsynced_tickets = redis_client.hgetall("unsynced_tickets")

    for ticket_id, ticket_data in unsynced_tickets.items():
        event_id, user_id = ticket_data.split(",")

        # Ghi thông tin vào database
        cursor.execute("""
            INSERT INTO tickets (ticket_id, event_id, user_id, status)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ticket_id)
            DO UPDATE SET status = EXCLUDED.status
        """, (ticket_id, event_id, user_id, "sold"))

        # Xóa vé khỏi danh sách cần đồng bộ
        redis_client.hdel("unsynced_tickets", ticket_id)

    # Commit transaction
    db_conn.commit()
    cursor.close()

# Chạy worker định kỳ (bằng Celery hoặc cron job)
sync_tickets_to_db()
```

---

### Lợi ích của hệ thống:
1. **Hiệu suất cao**:
   - Giao dịch được xử lý nhanh bằng cách lưu cache trước, giúp giảm thời gian phản hồi khi bán vé.
   - Database không bị quá tải khi có nhiều người dùng mua vé cùng lúc.

2. **Tránh bán trùng vé**:
   - Redis với các cấu trúc dữ liệu như `SET` đảm bảo mỗi vé chỉ được bán một lần.

3. **Đồng bộ định kỳ**:
   - Dữ liệu từ Redis được đồng bộ vào database, đảm bảo lưu trữ lâu dài.

---

### Lưu ý:
- **Tính nhất quán**: Cần xử lý lỗi khi Redis hoặc worker gặp sự cố để đảm bảo dữ liệu đồng bộ chính xác.
- **Mất dữ liệu Redis**: Redis cần được cấu hình để giảm thiểu rủi ro mất dữ liệu (bằng cách bật AOF - Append-Only File).