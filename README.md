# Agent Hỗ trợ Tra cứu Lịch học

## Giới thiệu dự án
Dự án này là một MVP (Minimum Viable Product) xây dựng một **ReAct Agent** sử dụng Python và Claude API để hỗ trợ sinh viên tra cứu lịch học trong khoảng thời gian từ 01/06/2026 đến 05/06/2026. Thay vì chỉ là một Chatbot thông thường trả lời dựa trên kiến thức có sẵn, Agent này có khả năng hiểu ngôn ngữ tự nhiên của người dùng, tự động chọn công cụ (tool) phù hợp, gọi công cụ để lấy dữ liệu thực tế và đưa ra câu trả lời chính xác.

## Kiến trúc Agent
Dự án được cấu trúc theo dạng module phối hợp với nhau, bao gồm:
- **Module Dữ liệu (`schedule_data.py`)**: Lưu trữ thông tin lịch học.
- **Module Công cụ (`tools.py`)**: Chứa các hàm hỗ trợ tra cứu lịch học và danh sách JSON schemas định nghĩa công cụ để Claude API có thể hiểu và gọi được.
- **Module Agent (`agent.py`)**: Chứa lõi logic của ReAct loop, kết nối với Claude API để xử lý yêu cầu.
- **Entry Point (`main.py`)**: File khởi chạy và ghép nối toàn bộ ứng dụng.

## Cách cài đặt

1. **Cài đặt thư viện:**
   Bạn cần cài đặt các thư viện phụ thuộc (`anthropic` và `python-dotenv`) bằng lệnh:
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình API Key:**
   Tạo một file `.env` ở thư mục gốc của dự án (cùng cấp với file `main.py`) và cung cấp Anthropic API Key của bạn:
   ```env
   ANTHROPIC_API_KEY=your-api-key-here
   ```

## Cách chạy

Khởi chạy ứng dụng bằng lệnh sau trong terminal:
```bash
python main.py
```
Ứng dụng sẽ mở ra giao diện chat trên terminal. Nhập câu hỏi để trò chuyện với Agent. Để thoát chương trình, hãy nhập `quit` hoặc `exit`.

## Demo flow

Dưới đây là một số ví dụ câu hỏi bạn có thể thử (Test cases) để kiểm tra các luồng tra cứu của Agent:

1. **Tra cứu theo ngày trong tuần:** 
   - *Hỏi:* "Thứ Ba học gì?" 
   - *Kỳ vọng:* Agent gọi tool `get_schedule_by_date("2026-06-02")`.
2. **Tra cứu theo chủ đề:** 
   - *Hỏi:* "Nội dung Vector Store học vào ngày nào?" 
   - *Kỳ vọng:* Agent gọi tool `search_schedule_by_topic("Vector Store")`.
3. **Tra cứu theo buổi học cụ thể:** 
   - *Hỏi:* "Sáng thứ Hai học gì?" 
   - *Kỳ vọng:* Agent gọi tool `get_session_detail("2026-06-01", "morning")`.

## Thought → Action → Observation

Kiến trúc **ReAct (Reasoning and Acting)** cho phép Agent hoạt động theo vòng lặp khép kín:

- **💭 Thought (Suy luận):** Agent tiếp nhận câu hỏi từ người dùng, phân tích và suy luận xem cần dùng công cụ nào để tìm kiếm dữ liệu. (Ví dụ: *"Người dùng hỏi về sáng Thứ Hai, lịch học bắt đầu từ 01/06/2026 là Thứ Hai, vậy mình cần gọi tool lấy chi tiết buổi sáng ngày 01/06/2026"*).
- **⚡ Action (Hành động):** Agent quyết định gọi công cụ với các tham số cụ thể đã được trích xuất (Ví dụ: gọi API function).
- **👁️ Observation (Quan sát):** Công cụ trả về kết quả thật từ hệ thống (JSON). Agent "quan sát" dữ liệu này để quyết định: Nếu đã đủ thông tin, nó sẽ trả lời người dùng; nếu chưa đủ hoặc bị lỗi, nó sẽ quay lại bước **Thought** để thử cách khác hoặc báo lỗi bằng ngôn ngữ tự nhiên.
