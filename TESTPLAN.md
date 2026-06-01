# Kế hoạch Kiểm thử (Test Plan) - Agent Hỗ trợ Tra cứu Lịch học

Tài liệu này mô tả chi tiết các kịch bản kiểm thử (Test Cases) để đảm bảo Agent hoạt động đúng theo yêu cầu thiết kế của kiến trúc ReAct và gọi chính xác các công cụ (Tools).

## 1. Mục tiêu kiểm thử (Test Objectives)
- Đảm bảo Agent hiểu đúng ý định của người dùng.
- Đảm bảo Agent gọi đúng Tool và truyền tham số (parameters) chính xác.
- Đảm bảo Agent xử lý tốt các trường hợp lỗi (ví dụ: không tìm thấy dữ liệu, tham số sai) và phản hồi lại cho người dùng bằng ngôn ngữ tự nhiên, thân thiện.

---

## 2. Các Kịch Bản Kiểm Thử (Test Cases)

### 2.1. Nhóm 1: Kiểm thử `get_schedule_by_date` (Tra cứu theo ngày)

| ID | Câu hỏi của người dùng | Hành động kỳ vọng (Tool & Tham số) | Phản hồi kỳ vọng của Agent | Trạng thái |
|---|---|---|---|---|
| 1.1 | "Lịch học ngày 02/06/2026 là gì?" | Gọi `get_schedule_by_date("2026-06-02")` | Trả lời đầy đủ lịch học sáng và chiều của Thứ Ba. | ⬜ Chưa test |
| 1.2 | "Thứ Ba học gì?" | Agent suy luận Thứ Ba là ngày 02/06/2026 -> Gọi `get_schedule_by_date("2026-06-02")` | Trả lời giống mục 1.1. | ⬜ Chưa test |
| 1.3 | "Chủ nhật có lịch học không?" | Agent suy luận Chủ nhật nằm ngoài khoảng 01/06-05/06 hoặc gọi Tool với ngày ngoài phạm vi | Thông báo không có lịch học vào Chủ nhật (hoặc báo lỗi từ Tool trả về một cách khéo léo). | ⬜ Chưa test |

### 2.2. Nhóm 2: Kiểm thử `search_schedule_by_topic` (Tra cứu theo chủ đề)

| ID | Câu hỏi của người dùng | Hành động kỳ vọng (Tool & Tham số) | Phản hồi kỳ vọng của Agent | Trạng thái |
|---|---|---|---|---|
| 2.1 | "Nội dung Vector Store học vào ngày nào?" | Gọi `search_schedule_by_topic("Vector Store")` | Trả lời đúng ngày 05/06/2026 (Thứ Sáu) và chi tiết session. | ⬜ Chưa test |
| 2.2 | "react" (Chữ thường) | Gọi `search_schedule_by_topic("react")` | Tìm thấy và trả lời ngày 01/06 và 02/06 (Không phân biệt hoa/thường). | ⬜ Chưa test |
| 2.3 | "Học Machine Learning vào ngày nào?" | Gọi `search_schedule_by_topic("Machine Learning")` | Tool trả về list rỗng. Agent thông báo không tìm thấy khóa học nào liên quan đến từ khóa này. | ⬜ Chưa test |

### 2.3. Nhóm 3: Kiểm thử `get_session_detail` (Tra cứu theo buổi)

| ID | Câu hỏi của người dùng | Hành động kỳ vọng (Tool & Tham số) | Phản hồi kỳ vọng của Agent | Trạng thái |
|---|---|---|---|---|
| 3.1 | "Sáng thứ Hai học gì?" | Gọi `get_session_detail("2026-06-01", "morning")` | Trả lời nội dung buổi sáng: "Design Pattern ReAct..." | ⬜ Chưa test |
| 3.2 | "Chiều ngày 4 tháng 6 học gì?" | Gọi `get_session_detail("2026-06-04", "afternoon")` | Trả lời nội dung buổi chiều của Thứ Năm. | ⬜ Chưa test |
| 3.3 | "Tối thứ Hai học gì?" | Có thể gọi Tool hoặc nhận ra không có ca tối. | Tool trả lỗi session không hợp lệ, hoặc Agent tự trả lời là chỉ có ca sáng và chiều. | ⬜ Chưa test |

### 2.4. Nhóm 4: Kiểm thử Nhận thức chung (General Conversation)

| ID | Câu hỏi của người dùng | Hành động kỳ vọng (Tool & Tham số) | Phản hồi kỳ vọng của Agent | Trạng thái |
|---|---|---|---|---|
| 4.1 | "Xin chào, bạn làm được gì?" | **KHÔNG** gọi Tool nào (hoặc không cần thiết). | Giới thiệu bản thân là trợ lý tra cứu lịch học từ 01/06 đến 05/06/2026. | ⬜ Chưa test |
| 4.2 | "Thời tiết hôm nay thế nào?" | **KHÔNG** gọi Tool nào. | Từ chối khéo léo, nói rằng chỉ hỗ trợ trả lời về lịch học của khóa học. | ⬜ Chưa test |

---

## 3. Cách thực hiện Test (Quy trình cho Người 4)
1. Mở terminal và chạy lệnh: `python main.py`
2. Đóng vai người dùng, lần lượt nhập các câu hỏi trong cột **Câu hỏi của người dùng**.
3. Quan sát logs trên terminal để kiểm tra phần **💭 Thought** và **⚡ Action** xem Agent có gọi đúng Tool và Tham số như kỳ vọng hay không.
4. Kiểm tra xem câu trả lời cuối cùng của Agent có chính xác, thân thiện không.
5. Cập nhật trạng thái `[x] Đã test` hoặc ghi chú lỗi (nếu có) vào bảng trên.
