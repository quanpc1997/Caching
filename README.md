# Cache

Nguồn: https://www.youtube.com/watch?v=a2RjtpXoWjA

![Cache](/Images/1-cache.png)
**Cache Hit**: là khi dữ liệu được tìm thấy trong cache.
**Cache Miss**: là khi dữ liệu không được tìm thấy trong cache.

## I. Caching Data Access Strategies - Chiến thuật cho cache
### 1. Read Through 
![Cache](/Images/1-cache.png)
- Khi một request được gửi đến, hệ thống sẽ tìm dữ liệu trong cache trước. 
    Nếu: 
        - **Có**: Trả dữ liệu về cho Client.
        - **Không**: Query từ DB -> Ghi và trong cache -> trả dữ liệu về cho người dùng.
#### Ưu điểm
- Không load toàn bộ dữ liệu lên cache.
- Trong trường hợp nhiều node lưu cache, khi một node bị sự cố thì hệ thống vẫn không bị hư hại.

#### Nhược điểm
- Trong trường hợp cache miss thì delay cao vì cần phải tốn 3 network round trip(round 1: Tìm trong Cache, Round 2: Query trong DB, Round 3: Ghi lại vào Cache)
- Nếu có thay đổi trong trong DB và cache chưa hết hạn, thì dữ liệu trả về sẽ là dữ liệu cũ. 

> :boom:  Giải pháp khắc phục nhược điểm là gì?

### 2. Write Through
- Insert/Update và DB thì cũng đồng thời cả trong cache.
- Cả 2 thao tác này cùng phải trong một transaction. 

#### Ưu điểm
- Đảm bảo dữ liệu trong cache luôn là mới nhất. 
- Thích hợp cho hệ thống cần nhu cầu đọc lớn và không chấp nhận dữ liệu cũ. 

#### Nhược điểm
- Mỗi thao tác insert/update sẽ bao gồm 2 thao tác là: ghi vào DB và ghi vào cache.
- Để đảm bảo tính đồng bộ, nếu một trong 2 thao tác write vào cache hoặc db thất bại => thao tác write thất bại.
- Phần lớn dữ liệu trong data không được đọc đến => Giải quyết bằng cách thêm thời gian expire. 

### 3. Write Behind Caching
- Data sẽ được ghi vào trong Cache trước và sau đó data mới được ghi vào DB bất đồng bộ trong 1 khoảng time nhỏ. 
- Phù hợp cho những hệ thống có read/write cao.

![Write Behind Caching](/Images/2-write-behind-caching.png)

Trong hình trên: Khi một data được insert vào thì sẽ được ghi vào trong cache đó. Và sau đó nhiệm vụ được đẩy vào trong 1 queue và sau đó có 1 worker sẽ xử lý các job trong queue và lưu vào trong database.

#### Ưu điểm
- Write/Read trên cache -> tăng performan.
- Tách biệt ứng dụng khỏi "database failure". Tức là khi có một sự cố xảy ra(giả sử như DB tạm chết) thì hệ thống vẫn query được từ cache và hệ thôngs vẫn chạy được bình thường.

#### Nhược điểm
- Bất đồng bộ giữa cache và database(tức là trong khoảng time rất ngắn chưa đồng bộ giữa DB và cache mà ta join hay thao tác gì đó trên db thì nó sẽ hiển thị lỗi)
- Do write cache và database không được xử lý trong cùng 1 transaction nên phải có cơ chế rollback nếu dữ liệu không thể write vào DB. 

## II. Một vài ứng dụng cache hay sử dụng
### 1. Memcached 
- Lưu trữ dữ liệu dưới dạng key/value.
- **Nhược điểm** không có cơ chế tự đồng bộ và không có cơ chế replicate.
    - Khi hệ thống có nhiều node thì việc ghi vào node nào hay lấy từ node nào là một vấn đề 

### 2. Redis
- Hỗ trợ nhiều loại kiểu dữ liệu thay vì chỉ key và value.
- Hỗ trợ cơ chế mỗi khi có sự cố thì redis sẽ lưu dữ liệu vào trong ổ cứng để khi start lên thì sẽ không bị mất dữ liệu.
- Hỗ trợ cơ chế master slave replication.
- Hỗ trợ Pub/sub

### 3. Các tool khác. 
Còn rất nhiều tool khác nhưng tạm thế đã.

### III. Tìm hiểu thêm
[1. Redis trong python](/Redis/README.md)