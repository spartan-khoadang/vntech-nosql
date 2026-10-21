# Script thuyết trình — NoSQL Phần 1

> Sinh tự động từ speaker notes trong `sections/*.html` (`<aside class="notes">`). Sửa script ở file section rồi chạy lại `python3 tools/build_script.py`.
> Khi trình chiếu: nhấn **N** để hiện script ngay trên slide, **→ / Space** để qua bước tiếp theo, **O** xem tổng quan, **T** đổi theme, **F** toàn màn hình.
> `[→]` trong script = nhấn phím mũi tên để hiện ý tiếp theo trên cùng slide.

**Tổng thời lượng ước tính:** khoảng 42 phút (chưa tính hỏi đáp), 30 slide.

## Slide 1 · Phần 1 · Nền tảng

Chào mọi người. Hôm nay mình nói về **NoSQL**. Bài chia làm hai phần: **phần 1** hôm nay là nền tảng — NoSQL là gì, tại sao đã có SQL mà vẫn cần NoSQL, và bốn loại NoSQL phổ biến. **Phần 2** buổi sau sẽ đi vào use case thực tế của từng loại.

Hình bên phải là bốn "hình dạng" dữ liệu mình sẽ gặp lại suốt buổi: key-value, document, wide-column và graph. Cuối buổi, mục tiêu là mọi người nhìn một bài toán và đoán được nên dùng hình dạng nào.

_(~1 phút)_

## Slide 2 · Nội dung

Lộ trình hôm nay có năm phần. **Một**, NoSQL là gì. **Hai**, tại sao cần NoSQL khi SQL đã rất tốt — đây là phần quan trọng nhất, vì nếu không hiểu "tại sao" thì rất dễ chọn sai. **Ba**, bốn loại NoSQL. **Bốn**, các khái niệm phân tán: ACID và BASE, CAP, quorum. **Năm**, tổng kết.

Mục cuối mờ đi là Phần 2 — use case — mình sẽ làm ở buổi sau.

_(~30 giây)_

## Slide 3 · Phần 01 — NoSQL là gì?

Phần đầu tiên: NoSQL là gì. Mình sẽ bắt đầu bằng một câu hỏi rất đời thường trước khi đưa ra định nghĩa.

## Slide 4 · Câu hỏi mở đầu

Hãy tưởng tượng mình làm một shop online. Laptop có CPU, RAM. Áo thun có size, màu. Nếu nhét tất cả vào một bảng `products` thì sao? **Đầy NULL**: laptop không có size, áo thì không có CPU.

_[Nhấn → để hiện dòng tai nghe]_ Giờ thêm tai nghe bluetooth — thêm cột nữa, lại `ALTER TABLE` trên bảng hàng triệu dòng. _[→]_ Còn nếu tách mỗi loại một bảng — bảng laptop, bảng áo — thì đọc một laptop rất dễ. Nhưng giỏ hàng trỏ tới bảng nào? Tìm "mọi sản phẩm dưới 500k" thì phải UNION qua tất cả các bảng, và mỗi loại mới lại thêm một bảng, sửa lại mọi query đó.

_[→]_ Vậy nếu mỗi sản phẩm là một "tài liệu" tự mô tả, có đúng những trường của nó thôi? Đó chính là một trong các ý tưởng gốc của NoSQL.

_(~1,5 phút)_

## Slide 5 · Định nghĩa

Định nghĩa: NoSQL thường được hiểu là **"Not only SQL"** — các database **không lấy bảng quan hệ** (hàng, cột, khóa ngoại) làm cách lưu chính.

Bên trái là cách SQL làm: tách ba bảng, khi đọc thì JOIN lại. _[→]_ Bên phải là cách một document database làm: mỗi sản phẩm là một JSON, laptop có `specs`, áo có `size`, `color`. Đọc một lần là đủ, không JOIN.

_(~1,5 phút)_

## Slide 6 · Phần 02 — Why NoSQL?

Phần hai, cũng là phần quan trọng nhất: **đã có SQL rồi, sao còn cần NoSQL?** Mình muốn nói rõ ngay từ đầu: SQL không hề lỗi thời. NoSQL ra đời để giải quyết vài giới hạn **rất cụ thể**. Mình sẽ đi qua hai vấn đề chính.

## Slide 7 · Vấn đề 1 · Mở rộng

Vấn đề đầu tiên là **mở rộng**. Phía trên là cách truyền thống: **scale up** — mọi request vào một server database. Chậm thì mua thêm CPU, RAM, SSD. Cách này đơn giản, giữ ACID dễ, nhưng giá tăng rất nhanh, có trần phần cứng, và nếu máy đó chết thì cả hệ thống chết.

Phía dưới là **scale out**: dữ liệu được chia thành nhiều phần gọi là **shard**. Query router nhìn vào **shard key** — ví dụ key bắt đầu từ A đến H — để biết dữ liệu nằm ở máy nào. Mỗi shard lại có **replica** để nếu một máy chết thì vẫn còn bản sao. Tải tăng gấp đôi thì thêm máy.

_(~2 phút)_

## Slide 8 · Vì sao SQL khó scale ngang?

Câu hỏi tự nhiên: sao không chia SQL ra nhiều máy luôn? Được, nhưng khó. Trên một máy, JOIN và transaction rất rẻ. Khi bảng `orders` ở máy 1 và `users` ở máy 2, một JOIN phải **kéo dữ liệu qua mạng**.

_[→]_ Transaction cũng vậy: muốn đảm bảo "hoặc cả hai máy cùng ghi, hoặc không máy nào ghi" thì cần two-phase commit — chậm, và một máy chậm làm cả giao dịch chờ.

_[→]_ NoSQL né vấn đề này bằng cách thiết kế để **dữ liệu hay đọc cùng nhau nằm cùng một chỗ** — cùng một key, một document hay một partition. Mỗi request chỉ chạm một máy, nên thêm máy là thêm sức chứa gần như tuyến tính.

_(~1,5 phút)_

## Slide 9 · Vấn đề 2 · Schema cứng & lệch mô hình

Vấn đề thứ hai là **schema cứng**. Trong code, một đơn hàng là một object: có khách hàng, danh sách item, địa chỉ giao hàng — lồng vào nhau rất tự nhiên.

_[→]_ Trong SQL, mình phải cắt nó ra bốn bảng, rồi dùng ORM để ghép lại mỗi lần đọc. Và khi sản phẩm cần thêm một trường như "lời nhắn quà tặng", phải `ALTER TABLE` trên bảng có thể hàng trăm triệu dòng — cần lên kế hoạch migration cẩn thận.

_[→]_ Độ lệch này có tên là **impedance mismatch**. Document database lưu thẳng object dưới dạng JSON, nên khớp với code hơn, và thêm trường mới không cần migration lớn.

_(~1,5 phút)_

## Slide 10 · SQL vs NoSQL

Tóm lại thành một bảng. Mình chỉ nhấn mạnh ba dòng.

**Mở rộng**: SQL chủ yếu theo chiều dọc, NoSQL theo chiều ngang. **Giao dịch**: SQL có ACID đầy đủ trên nhiều bảng; NoSQL thường chỉ đảm bảo trong một bản ghi hoặc một partition. **Truy vấn**: SQL rất mạnh với câu hỏi bất chợt — ad-hoc — nhờ JOIN; NoSQL nhanh với các query đã biết trước lúc thiết kế, còn câu hỏi bất chợt thì thường chậm hoặc không làm được.

_(~1,5 phút)_

## Slide 11 · Điểm mấu chốt

Nếu chỉ nhớ một câu của phần này thì đó là: **NoSQL không tốt hơn SQL — nó đánh đổi.**

Nó bỏ bớt JOIN, transaction nhiều bảng, query ad-hoc, đôi khi cả nhất quán mạnh. _[→]_ Để đổi lấy scale ngang, latency thấp, sẵn sàng cao và schema linh hoạt.

_[→]_ Vì vậy câu hỏi đúng không phải "SQL hay NoSQL", mà là "dữ liệu này sẽ được đọc và ghi như thế nào". Và câu trả lời cho câu hỏi đó sẽ dẫn mình tới một trong bốn loại NoSQL ở phần tiếp theo.

_(~1 phút)_

## Slide 12 · Phần 03 — Bốn loại NoSQL

Phần ba: bốn loại NoSQL. Với mỗi loại mình sẽ trả lời ba câu: **nó lưu dữ liệu thế nào**, **nó trả lời nhanh câu hỏi gì**, và **nó yếu ở đâu**.

## Slide 13 · Tổng quan

Đây là bức tranh tổng thể, đi từ đơn giản nhất đến giàu quan hệ nhất.

**Key-value**: như một hash map khổng lồ — Redis, DynamoDB. _[→]_ **Document**: mỗi bản ghi là một JSON — MongoDB, Firestore. _[→]_ **Wide-column**: hàng có số cột thay đổi, chuyên ghi khối lượng lớn — Cassandra, HBase. _[→]_ **Graph**: dữ liệu là node và cạnh, chuyên duyệt quan hệ — Neo4j.

Giờ mình đi vào từng loại.

_(~1 phút)_

## Slide 14 · 3.1 · Key-Value

Loại đầu tiên và đơn giản nhất: **key-value**. Hình dung một cái hash map khổng lồ, phân tán trên nhiều máy. Mình đưa vào một key, nhận lại một value. Database không quan tâm value là chuỗi, JSON hay ảnh — với nó, value là một "hộp đen".

Ví dụ với Redis: `SET` một session kèm `EX 3600` nghĩa là một tiếng sau nó tự biến mất. `INCR` tăng một bộ đếm một cách nguyên tử — dùng cho rate limiting.

Điểm mạnh: đọc ghi theo key là O(1), nhiều hệ chạy trong RAM nên dưới một mili-giây. Phân tán rất dễ vì chỉ cần hash key là biết node. _[→]_ Có TTL cho dữ liệu tạm.

_[→]_ Điểm yếu: **không hỏi được theo nội dung**. Muốn "tìm mọi session của user 42" thì phải tự tạo thêm key làm index.

Ví dụ shop online: giỏ hàng lưu theo key `cart:user:42` — mở giỏ của user 42 thì cực nhanh. Nhưng hỏi "những giỏ nào đang có sản phẩm A1?" (để báo A1 sắp hết hàng) thì Redis chịu, phải mở từng giỏ ra xem. Muốn trả lời nhanh, app phải tự ghi thêm key `product:A1:carts` → [42, 57, …], và tự xoá khỏi đó khi user bỏ A1 ra khỏi giỏ.

_(~2 phút)_

## Slide 15 · 3.2 · Document

Loại thứ hai: **document**. Về bản chất nó giống key-value — mỗi document có một `_id` — nhưng khác ở chỗ database **hiểu cấu trúc** bên trong. Document được nhóm vào **collection**, giống bảng nhưng không có schema cố định.

Đây là một laptop: có `specs` lồng bên trong, có mảng `tags`, có cả `reviews`. _[→]_ Và mình query được thẳng vào trường lồng nhau: laptop có RAM từ 16GB, giá dưới 30 triệu, sắp xếp theo giá. Cũng đánh index được trên các trường đó.

Điểm mạnh: linh hoạt, thân thiện với lập trình viên, đọc một lần là có đủ dữ liệu.

_[→]_ Điểm yếu: quan hệ nhiều–nhiều khó mô hình — slide sau có ví dụ; và một document không được phình vô hạn — MongoDB giới hạn 16 MB.

_(~2 phút)_

## Slide 16 · 3.2 · Document · ví dụ

Ví dụ cho điểm yếu vừa rồi. Một đơn hàng có nhiều sản phẩm, một sản phẩm nằm trong nhiều đơn — quan hệ **nhiều–nhiều**. SQL chỉ cần thêm bảng nối `order_items` rồi JOIN, hỏi chiều nào cũng được. Document thì phải chọn: nhúng vào đâu?

Cách 1: nhúng sản phẩm vào đơn. Xem một đơn rất nhanh, nhưng đổi tên áo A1 thì phải sửa hàng nghìn đơn đang giữ bản sao.

_[→]_ Cách 2: nhúng ngược, danh sách đơn vào sản phẩm. Sản phẩm bán chạy có hàng triệu đơn, mảng phình tới giới hạn 16 MB.

_[→]_ Cách 3: chỉ lưu id rồi tra sau bằng `$lookup`. Gọn, nhưng đó lại chính là JOIN.

Quan hệ 1–nhiều thì document làm rất tốt — cứ nhúng con vào cha. Nhiều–nhiều thì không có "cha" rõ ràng, nên phải chọn theo câu query hay chạy nhất. Thực tế hay dùng cách 1 cho đơn hàng: giá và tên lúc mua vốn nên được giữ nguyên.

_(~1,5 phút)_

## Slide 17 · 3.3 · Wide-column

Loại thứ ba: **wide-column**, tiêu biểu là Cassandra. Cách nghĩ: dữ liệu được chia theo **partition key** — ở đây là `user_id`. Bên trong mỗi partition, các hàng được **sắp xếp sẵn** theo **clustering key** — ở đây là thời gian xem, mới nhất ở trên.

_[→]_ Nên câu "20 sản phẩm user 42 xem gần nhất" chỉ cần đọc đúng một partition, dữ liệu đã nằm theo thứ tự — rất nhanh.

Điểm mạnh lớn nhất là **ghi cực nhanh**: nó ghi vào RAM và commit log trước, sau đó mới dồn xuống đĩa thành các file bất biến — cấu trúc này gọi là LSM-tree.

_[→]_ Điểm yếu: query **bắt buộc** phải theo partition key, không JOIN, nên thường mỗi query thiết kế một bảng riêng.

_(~2 phút)_

## Slide 18 · 3.4 · Graph

Loại cuối: **graph**. Dữ liệu là **node** — An, Bình, Chi, sản phẩm — và **cạnh** có tên — FRIEND, BOUGHT. Điểm khác biệt: quan hệ được **lưu thẳng**, mỗi node trỏ trực tiếp tới hàng xóm, nên duyệt không phụ thuộc tổng kích thước dữ liệu.

_[→]_ Query bằng Cypher của Neo4j đọc gần như vẽ hình: từ An, đi theo cạnh FRIEND tới bạn bè, rồi theo cạnh BOUGHT tới sản phẩm, loại những thứ An đã mua. Kết quả: Laptop X14 được cả Bình và Chi mua → gợi ý cho An.

_[→]_ Trong SQL, mỗi bước "bạn của bạn" là thêm một self-JOIN; đến 4–5 bước thì rất chậm.

_[→]_ Điểm yếu: đồ thị khó cắt ra nhiều máy, và không hợp với thống kê kiểu "tổng doanh thu theo tháng".

_(~2 phút)_

## Slide 19 · So sánh 4 loại

Gom lại thành một bảng. Không có loại nào thắng ở mọi cột: key-value scale dễ nhất nhưng không query được theo nội dung; graph mạnh nhất về quan hệ nhưng khó scale.

Dòng cuối là hình ảnh để dễ nhớ: key-value là **tủ đồ có số** — biết số tủ thì lấy ngay. Document là **tập hồ sơ** — mỗi hồ sơ một kiểu, lục được theo nội dung. Wide-column là **sổ nhật ký theo từng người** — ghi liên tục, đọc theo thứ tự thời gian. Graph là **sơ đồ mạng quan hệ**.

_(~1,5 phút)_

## Slide 20 · Bốn loại trong một hệ thống

Trong thực tế, một hệ thống không chỉ dùng một loại. Đây là một shop online: **Redis** giữ session và giỏ hàng, **MongoDB** giữ catalog sản phẩm, **Neo4j** tính gợi ý, **Cassandra** ghi lịch sử xem và log. Phần thanh toán thường vẫn để ở SQL vì cần ACID.

Cách làm này gọi là **polyglot persistence**. Cái giá là phải vận hành nhiều hệ và đồng bộ dữ liệu giữa chúng. Đây cũng chính là phần mình sẽ đào sâu ở **Phần 2: use case**.

_(~1,5 phút)_

## Slide 21 · Ngoài bốn loại chính

Ngoài bốn loại chính, có vài nhánh chuyên biệt mọi người sẽ hay gặp: **time-series** cho metrics và dữ liệu cảm biến; **search engine** như Elasticsearch cho tìm kiếm full-text; **vector database** — đang rất hot nhờ AI — để tìm theo ý nghĩa bằng embedding; và **multi-model** hỗ trợ nhiều mô hình trong một hệ.

Hôm nay mình chỉ điểm danh; trọng tâm vẫn là bốn loại chính.

_(~1 phút)_

## Slide 22 · Phần 04 — Khái niệm phân tán

Phần bốn: các khái niệm phân tán. Vì NoSQL chạy trên nhiều máy, có vài khái niệm mà ai làm NoSQL cũng phải biết: ACID và BASE, định lý CAP, và quorum. Mình sẽ đi nhanh và trực quan.

## Slide 23 · ACID vs BASE

**ACID** là lời hứa của SQL truyền thống: Atomicity — làm hết hoặc không làm gì; Consistency — luôn thỏa ràng buộc; Isolation — các giao dịch song song không giẫm chân nhau; Durability — đã commit thì không mất. Ví dụ kinh điển: chuyển tiền, không được phép trừ bên này mà chưa cộng bên kia. Để giữ lời hứa đó, hệ thống **thà bắt chờ hoặc báo lỗi** còn hơn trả kết quả sai.

_[→]_ **BASE** là triết lý ngược lại, của nhiều hệ NoSQL: **thà trả lời ngay, đúng dần sau**. Ba chữ cái:

**Basically Available** — hệ thống luôn trả lời, kể cả khi vài máy chết hay mạng chập chờn. Chữ "basically" nghĩa là "về cơ bản": câu trả lời có thể là dữ liệu cũ, nhưng không phải lỗi.

**Soft state** — đây là chữ khó nhất. Trong SQL, dữ liệu chỉ đổi khi có người ghi. Ở đây, dữ liệu trên một máy có thể **tự đổi dù không ai ghi vào nó**, vì các máy đang đồng bộ ngầm với nhau. Đọc hai lần liên tiếp có thể ra hai kết quả khác nhau.

**Eventual consistency** — là lời hứa của hệ thống: không hứa đúng ngay, chỉ hứa nếu ngừng ghi thì **cuối cùng** mọi bản sao sẽ giống nhau, thường chỉ sau vài mili giây đến vài giây.

Ba chữ này thật ra là **một cơ chế nhìn từ ba góc** — slide sau mình sẽ cho mọi người thấy bằng một ví dụ cụ thể.

_(~2,5 phút)_

## Slide 24 · BASE qua một ví dụ

Một bài viết đang có **100 like**. Dữ liệu được sao ra **3 máy** A, B, C — lúc đầu cả ba đều ghi 100. Giờ có hai người bấm like, request ghi đi vào máy A.

_[→]_ Thời điểm t1: A cập nhật thành 102 và **trả OK ngay** cho người dùng, không chờ B và C. Đúng lúc này, ai đó đọc từ máy C sẽ thấy 100 — dữ liệu cũ, nhưng vẫn là một câu trả lời, không phải lỗi, không phải chờ. Đó là **Basically Available**: luôn trả lời, chấp nhận có thể chưa mới nhất.

_[→]_ t2, t3: A gửi cập nhật cho B, rồi tới C, ở chế độ ngầm. Mọi người để ý máy C: **không ai ghi gì vào C**, vậy mà giá trị của nó tự đổi từ 100 thành 102. Đó là **Soft state** — trạng thái "mềm", có thể tự thay đổi do đồng bộ. Trong SQL thì không có chuyện này: dữ liệu chỉ đổi khi có transaction commit.

_[→]_ t3: cả ba máy cùng là 102. Đó là **Eventual consistency** — lời hứa rằng nếu ngừng ghi, các bản sao cuối cùng sẽ giống nhau. Hệ thống không hứa _khi nào_, nhưng thực tế thường chỉ vài mili giây đến vài giây.

Tóm lại một câu: ghi nhanh không chờ đủ máy, nên các máy tạm lệch nhau, đồng bộ dần, rồi cuối cùng giống nhau. Ba chữ B-A-S-E chỉ là ba góc nhìn của cùng một chuyện đó.

_[→]_ Hai lưu ý. Thứ nhất, BASE **không có nghĩa là mất dữ liệu** — 2 like vẫn còn đó, chỉ đến các máy chậm hơn một chút. Thứ hai, cách kiểm tra có nên dùng BASE: nếu người dùng thấy dữ liệu **cũ vài giây** mà **không ai bị thiệt** — như like, lượt xem, feed — thì ổn. Còn số dư tài khoản hay tồn kho lúc đặt hàng thì không: thấy cũ vài giây là có thể bán quá số hàng đang có.

Vậy có cách nào để hệ BASE vẫn đọc được bản mới nhất khi cần không? Có — nhưng trước hết mình cần hiểu vì sao phải đánh đổi như vậy. Đó là định lý CAP.

_(~2,5 phút)_

## Slide 25 · Định lý CAP

**Định lý CAP** nói rằng trong hệ phân tán, khi mạng giữa các máy bị đứt — gọi là partition — hệ thống chỉ đảm bảo được một trong hai: **C**, mọi lần đọc đều thấy bản mới nhất; hoặc **A**, mọi request đều được trả lời.

Hay bị hiểu nhầm là "chọn 2 trong 3". Thực tế, mạng **chắc chắn có lúc đứt**, nên P là bắt buộc. _[→]_ Lựa chọn thật là **CP** hay **AP**.

CP — như MongoDB mặc định, HBase — sẽ từ chối request thay vì trả dữ liệu có thể sai. AP — như Cassandra, DynamoDB — vẫn trả lời, chấp nhận dữ liệu tạm cũ, đồng bộ sau.

Nghe vẫn hơi trừu tượng, nên mình đi qua một ví dụ cụ thể.

_(~2 phút)_

## Slide 26 · CAP qua một ví dụ

Một ví dụ cụ thể. Shop online còn đúng **1 chiếc áo**. Dữ liệu tồn kho được lưu trên 3 máy: 2 máy ở Hà Nội, 1 máy ở TP.HCM. Bình thường, ba máy liên tục báo cho nhau mỗi khi có thay đổi.

_[→]_ Rồi cáp mạng giữa Hà Nội và TP.HCM bị đứt. Cả 3 máy vẫn chạy, khách vẫn vào web được, nhưng hai nơi không nói chuyện được với nhau. Đó chính là **partition**.

_[→]_ Đúng lúc đó, An ở Hà Nội bấm mua — máy Hà Nội trừ kho, còn 0. Cùng lúc, Bình ở TP.HCM cũng bấm mua. Máy 3 vẫn thấy kho bằng 1, vì nó **không biết An vừa mua**. Giờ máy 3 phải chọn: từ chối Bình, hay bán cho Bình?

_[→]_ Cách thứ nhất là **CP**: thà từ chối còn hơn sai. Máy 3 không liên lạc được Hà Nội, không chắc còn hàng, nên trả lỗi "hệ thống bận, thử lại sau". Phía Hà Nội có 2 trên 3 máy, là đa số, nên vẫn bán bình thường. Kết quả: không bao giờ bán trùng — giữ được C — nhưng khách ở TP.HCM bị từ chối — mất A.

_[→]_ Cách thứ hai là **AP**: thà trả lời còn hơn từ chối. Máy 3 thấy còn 1 thì bán luôn. Ai cũng mua được — giữ được A — nhưng một chiếc áo đã bán cho hai người — mất C. Khi mạng nối lại, hệ thống phát hiện xung đột, phải hủy một đơn, hoàn tiền, xin lỗi khách.

Và không có cách thứ ba: máy 3 không thể vừa trả lời ngay vừa chắc chắn đúng, vì nó không có cách nào biết Hà Nội vừa làm gì.

_[→]_ Nhưng nếu đổi tồn kho thành **số like** thì sao? Lệch một like trong vài phút không ai thiệt, nối mạng lại là tự đúng — chọn AP là hợp lý, chặn người dùng chỉ vì sợ lệch một like mới là vô lý. Nên CAP không có lựa chọn đúng hay sai, chỉ có lựa chọn **hợp với dữ liệu**: sai một chút là mất tiền thì CP, sai một chút không ai thiệt thì AP.

_(~2,5 phút)_

## Slide 27 · Quorum

Vậy các hệ AP như Cassandra làm sao vẫn đọc đúng? Câu trả lời là **quorum**.

Mỗi dữ liệu có **N = 3** bản sao. Khi ghi giá mới bằng 200, coordinator gửi tới cả ba, nhưng chỉ chờ **W = 2** máy xác nhận là trả OK. Replica 3 đang mạng chậm, chưa nhận được.

Khi đọc, coordinator hỏi **R = 2** máy — giả sử trúng replica 2 và replica 3. Replica 3 trả giá cũ 150, replica 2 trả 200. Coordinator chọn bản có timestamp mới nhất, trả 200 cho client, và gửi **read repair** để sửa replica 3.

Tại sao luôn đúng? Vì **2 + 2 > 3**: hai máy đọc và hai máy ghi trong tổng ba máy thì luôn chung ít nhất một máy. Muốn ghi nhanh hơn thì giảm W, đổi lại là rủi ro đọc phải dữ liệu cũ.

_(~2,5 phút)_

## Slide 28 · Phần 05 — Tổng kết

Phần cuối: tổng kết. Mình sẽ gói mọi thứ thành một cây quyết định và chốt năm điều nên nhớ.

## Slide 29 · Chọn database

Đây là một cây quyết định đơn giản. Câu hỏi đầu tiên: có cần **ACID trên nhiều bảng** không — tiền, tồn kho? Có thì dùng SQL. Không thì hỏi tiếp: **quan hệ có phải trọng tâm** không? Có thì graph. Tiếp: có phải **chỉ tra theo key**? Có thì key-value. Tiếp: **ghi cực lớn**, time-series, log? Có thì wide-column. Nếu tất cả đều không, document là lựa chọn mặc định linh hoạt.

Nhớ là đây chỉ là heuristic. Phần 2 mình sẽ thấy các hệ thống thật kết hợp nhiều loại thế nào.

_(~1,5 phút)_

## Slide 30 · Năm điều nên nhớ

Năm điều nên nhớ. **Một**, NoSQL là "Not only SQL" — một họ database, không phải một sản phẩm.

_[→]_ **Hai**, nó ra đời vì cần scale ngang và schema linh hoạt — không phải vì SQL kém. _[→]_ **Ba**, bốn loại: key-value để tra theo key, document cho JSON linh hoạt, wide-column cho ghi cực lớn, graph cho quan hệ sâu.

_[→]_ **Bốn**, phân tán luôn là đánh đổi: CAP, BASE, và công thức quorum R cộng W lớn hơn N. _[→]_ **Năm**, thiết kế bắt đầu từ câu hỏi, và hệ thống thật thường kết hợp nhiều loại.

_(~1,5 phút)_
