# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Lê Đình Sỹ
- **Student ID**: 2A202600770
- **Date**: 6/1/2026
- **Role Assignment**: **Người 4** (Ghép nối Entry Point, Cấu hình môi trường, Soạn thảo tài liệu và Kiểm thử hệ thống)

---

## I. Technical Contribution (15 Points)

Với vai trò **Người 4**, tôi chịu trách nhiệm thiết lập cấu trúc dự án, tạo cổng khởi chạy (`main.py`), cấu hình môi trường, lập danh sách thư viện phụ thuộc (`requirements.txt`), tài liệu hóa hướng dẫn (`README.md`), và trực tiếp thực thi kiểm thử tích hợp (Integration Testing) toàn bộ hệ thống ReAct Agent.

### 1. Modules Implemented & Configured
Tôi đã trực tiếp thiết lập và cài đặt các tệp tin cấu hình và ghép nối nền tảng của dự án:
- `main.py`: Cổng khởi chạy tập trung của Agent.
- `requirements.txt`: Định nghĩa các thư viện phụ thuộc bắt buộc.
- `.env` & `.gitignore`: Thiết lập cấu hình bảo mật biến môi trường.
- `README.md`: Soạn thảo tài liệu hướng dẫn vận hành và thử nghiệm.

### 2. Code Highlights

#### Cổng khởi chạy `main.py`
Ghép nối trực tiếp luồng thực thi với lõi Agent nhằm cung cấp một giao diện chat trực quan trên Terminal:
```python
# main.py
"""Agent Hỗ trợ Tra cứu Lịch học — Entry Point"""
from agent import main

if __name__ == "__main__":
    main()
```

#### Quản lý thư viện `requirements.txt`
Khai báo chính xác phiên bản thư viện cần thiết theo chuẩn kỹ thuật của hệ thống Anthropic và môi trường:
```
anthropic>=0.39.0
python-dotenv>=1.0.0
```

#### Quản lý phiên bản & Bảo mật `.gitignore`
Ngăn chặn tuyệt đối việc lộ khóa API Key cá nhân lên GitHub bằng cách loại trừ file `.env` và các thư mục cache:
```
.env
__pycache__/
*.pyc
.vscode/
.idea/
```

### 3. Documentation & Integration Role
Tôi đã đóng vai trò là "chất keo" kết nối các module của các thành viên khác trong nhóm:
- Tích hợp Module dữ liệu `schedule_data.py` (Người 1) và Module công cụ `tools.py` (Người 2) vào lõi Agent `agent.py` (Người 3).
- Đồng bộ hóa các luồng dữ liệu thông qua cổng khởi chạy `main.py` để đảm bảo sinh viên có thể gõ câu hỏi tự nhiên và nhận về phản hồi chính xác từ cơ sở dữ liệu học tập thông qua ReAct Loop.

---

## II. Debugging Case Study (10 Points)

Trong quá trình ghép nối hệ thống, tôi đã phát hiện và xử lý một lỗi nghiêm trọng liên quan đến cơ chế xác thực và cấu hình Schema của Agent.

### 1. Problem Description
Khi khởi chạy hệ thống bằng lệnh `python main.py` và nhập câu hỏi tra cứu lịch học như `"Thứ Ba học gì?"`, chương trình ngay lập tức crash và trả về mã lỗi xác thực:
```
anthropic.AuthenticationError: Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}}
```

### 2. Log Source (Traceback)
```
Traceback (most recent call last):
  File "C:\Users\Asus\AI_Labs\Day-3-Lab-Chatbot-vs-react-agent\main.py", line 5, in <module>
    main()
  File "C:\Users\Asus\AI_Labs\Day-3-Lab-Chatbot-vs-react-agent\agent.py", line 326, in main
    answer = agent.chat(user_input)
  File "C:\Users\Asus\AI_Labs\Day-3-Lab-Chatbot-vs-react-agent\agent.py", line 218, in chat
    response = self.client.messages.create(
        model=MODEL,
        messages=self.messages,
    )
anthropic.AuthenticationError: Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CbcDBtuDHdp6sqvdSPaMZ'}
```

### 3. Diagnosis
Qua việc kiểm tra kỹ lượng hệ thống cấu hình, tôi đã chẩn đoán nguyên nhân lỗi gồm hai phần:
1. **Xung đột API Key**: Biến môi trường `ANTHROPIC_API_KEY` trong file `.env` đang lưu trữ một khóa API của OpenRouter (có tiền tố `sk-or-v1-`). Tuy nhiên, file `agent.py` lại khởi tạo client native `Anthropic()` mặc định, hướng các yêu cầu trực tiếp đến máy chủ gốc của Anthropic (`api.anthropic.com`), dẫn đến việc khóa bị từ chối và báo lỗi 401.
2. **Sai lệch cấu trúc Schema**: Schema của các công cụ trong `tools.py` đang sử dụng từ khóa `"parameters"` (chuẩn của OpenAI) thay vị `"input_schema"` (chuẩn của Anthropic), khiến mô hình Claude không thể nhận diện đúng tham số đầu vào.

### 4. Solution
Tôi đã trực tiếp phối hợp sửa đổi và khắc phục lỗi này bằng cách:
- Cấu hình lại client `Anthropic` trỏ tới cổng tương thích của OpenRouter thông qua việc thiết lập `base_url` thành `"https://openrouter.ai/api"` (SDK Anthropic sẽ tự động nối `/v1/messages` để tạo thành đường dẫn hợp lệ của OpenRouter):
  ```python
  self.client = Anthropic(
      base_url="https://openrouter.ai/api",
      api_key=os.getenv("ANTHROPIC_API_KEY"),
  )
  ```
- Định nghĩa lại mã mô hình chính xác trên OpenRouter: `MODEL = "anthropic/claude-3-haiku"`.
- Sửa đổi định nghĩa schemas trong `tools.py`, thay thế khóa `"parameters"` bằng `"input_schema"` để mô hình Claude hiểu rõ các tham số.

Sau các thay đổi này, hệ thống chạy trơn tru và gọi công cụ thành công.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

### 1. Reasoning (Khả năng suy luận)
Vòng lặp ReAct mang lại khả năng suy luận vượt trội so với Chatbot thông thường nhờ khối lệnh `Thought`. Chatbot truyền thống thường cố gắng đưa ra câu trả lời trực tiếp dựa trên dữ liệu tĩnh có sẵn trong trọng số (weight) của mô hình dẫn đến việc dễ bị hallucination (bịa đặt lịch học) khi được hỏi về thông tin thay đổi liên tục. 
Ngược lại, khối `Thought` trong ReAct hoạt động như một "không gian nháp" (scratchpad) giúp Agent tự lập kế hoạch trước khi hành động. Agent có thể suy luận: *"Người dùng muốn biết lịch học Thứ Ba, hôm nay là 2026-06-01 (Thứ Hai), vậy Thứ Ba là ngày 2026-06-02. Mình cần gọi công cụ get_schedule_by_date với tham số date='2026-06-02' để lấy dữ liệu thực tế"*.

### 2. Reliability (Độ tin cậy)
Agent ReAct đạt độ tin cậy tuyệt đối khi trả lời về lịch học vì toàn bộ câu trả lời đều dựa trên dữ liệu thực được trích xuất từ file `schedule.csv` thông qua công cụ. 
Tuy nhiên, trong một số trường hợp, Agent ReAct có thể hoạt động *kém hiệu quả hơn* Chatbot thông thường:
- Khi người dùng đưa ra các câu hỏi ngoài lề đơn giản hoặc câu chào (ví dụ: "alo", "hello"). Nếu không cấu hình bộ lọc chặn nhanh (off-topic guard), Agent sẽ tốn nhiều bước suy luận và tokens gọi API vô ích để xử lý các câu hỏi không liên quan.
- Khi API gặp trục trặc về mạng hoặc bị hết hạn mức (rate limit), làm đứt gãy ReAct loop.

### 3. Observation (Tác động của môi trường)
Phản hồi từ môi trường (`Observation`) là yếu tố quyết định hành vi tiếp theo của Agent. Nếu kết quả công cụ trả về lịch học chi tiết, Agent sẽ kết luận thông tin đã đầy đủ và sinh ra câu trả lời cuối cùng (`Final Answer`). 
Nếu `Observation` trả về mã lỗi (ví dụ: `"Không tìm thấy lịch học cho ngày 2026-06-06"`), Agent sẽ tự nhận biết được giới hạn của dữ liệu, suy luận tiếp để sửa đổi tham số gọi công cụ hoặc thông báo lịch sự cho người dùng về phạm vi hỗ trợ thay vì tự bịa câu trả lời.

---

## IV. Future Improvements (5 Points)

Để nâng cấp MVP này lên một hệ thống Agent cấp sản xuất (Production-level AI Agent), tôi đề xuất 3 cải tiến sau:

1. **Scalability (Khả năng mở rộng)**:
   - Áp dụng cơ chế **Asynchronous Execution (Thực thi bất đồng bộ)** bằng thư viện `asyncio` để cho phép Agent gọi song song nhiều công cụ cùng lúc khi xử lý các câu hỏi phức tạp cần tổng hợp thông tin từ nhiều nguồn, rút ngắn thời gian phản hồi (TTFT).
2. **Safety (Tính an toàn & Bảo mật)**:
   - Xây dựng một **Supervisor Agent** (LLM thứ hai) làm nhiệm vụ kiểm duyệt (Audit) các tham số đầu vào của Action và dữ liệu đầu ra của Observation nhằm ngăn chặn triệt để Prompt Injection gián tiếp hoặc các hành vi gọi công cụ trái phép.
3. **Performance (Hiệu năng)**:
   - Sử dụng **Vector Database** (như ChromaDB hoặc pgvector) để lưu trữ lịch học và tích hợp kỹ thuật Semantic Search (Tìm kiếm ngữ nghĩa) thay thế cho việc duyệt từ khóa thủ công bằng code Python. Điều này giúp Agent tra cứu ngữ nghĩa chính xác hơn ngay cả khi người dùng gõ sai chính tả hoặc dùng từ đồng nghĩa.
