# Phân công công việc — Agent Hỗ trợ Tra cứu Lịch học

## Tổng quan dự án

Xây dựng MVP Agent ReAct hỗ trợ sinh viên tra cứu lịch học (01–05/06/2026) bằng Python + Claude API.

Agent hiểu câu hỏi tự nhiên → chọn tool phù hợp → gọi tool → trả lời.

**Tech stack:** Python, Claude API (tool_use), python-dotenv

**Cấu trúc file sau khi hoàn thành:**

```
Day03-lab/
├── schedule_data.py      ← Người 1
├── tools.py              ← Người 2
├── agent.py              ← Người 3
├── main.py               ← Người 4
├── requirements.txt      ← Người 4
├── .env                  ← Người 4
├── .gitignore            ← Người 4
└── README.md             ← Người 4
```

---

## Thứ tự phụ thuộc

```
Người 1 (data) ──→ Người 2 (tools) ──→ Người 3 (agent) ──→ Người 4 (entry + test)
```

Người 1 và 4 có thể làm song song.

---

## Người 1 — Module Dữ liệu

| Hạng mục | Chi tiết |
|---|---|
| File | `schedule_data.py` |
| Độ khó | ⭐ Dễ |
| Ước lượng | 15 phút |

### Nhiệm vụ

Tạo dictionary `SCHEDULE` chứa toàn bộ lịch học 5 ngày.

### Yêu cầu kỹ thuật

- Key: chuỗi `"YYYY-MM-DD"`
- Value: dict gồm `"weekday"`, `"morning"`, `"afternoon"`
- Export: biến `SCHEDULE`

### Dữ liệu cần nhập

| Ngày | Thứ | Buổi sáng | Buổi chiều |
|---|---|---|---|
| 2026-06-01 | Thứ Hai | Design Pattern ReAct, kiến trúc Agent, Agent Loop, Thought-Action-Observation | Vibe Coding 3, Agent Loop Prototyping và Lab 3: Chatbot vs Agent – thực hành so sánh và xây dựng luồng Agent |
| 2026-06-02 | Thứ Ba | Prompt Engineering & Tool Calling, bao gồm system prompt, function calling và LangGraph | Vibe Coding 4, Tool Development with AI và Lab 4: Build First AI Agent – ReAct + Tools |
| 2026-06-03 | Thứ Tư | AI Product Thinking & Requirements, PRD cho AI và Risk Assessment | Vibe Coding 5, PRD Generation & Risk Analysis và Lab 5: PRD Writing & Risk Assessment |
| 2026-06-04 | Thứ Năm | AI Product & Project Management, Agile cho AI, MVP và low-code tools | Vibe Coding 6, Business Document Generation và Lab 6: Final PRD and ROI Analysis |
| 2026-06-05 | Thứ Sáu | Data Foundations, gồm Embedding, Chunking, Vector Store, ChromaDB/FAISS | Vibe Coding 7, Data Processing Pipeline và Lab 7: Vector Store Integration |

### Đầu ra mẫu

```python
# schedule_data.py

SCHEDULE = {
    "2026-06-01": {
        "weekday": "Thứ Hai",
        "morning": "Design Pattern ReAct, kiến trúc Agent, Agent Loop, Thought-Action-Observation.",
        "afternoon": "Vibe Coding 3, Agent Loop Prototyping và Lab 3: Chatbot vs Agent – ..."
    },
    # ... 4 ngày còn lại
}
```

### Kiểm tra

```python
from schedule_data import SCHEDULE
assert len(SCHEDULE) == 5
assert SCHEDULE["2026-06-02"]["weekday"] == "Thứ Ba"
```

---

## Người 2 — Module Tools

| Hạng mục | Chi tiết |
|---|---|
| File | `tools.py` |
| Import | `from schedule_data import SCHEDULE` |
| Độ khó | ⭐⭐ Trung bình |
| Ước lượng | 30 phút |

### Nhiệm vụ

Viết 3 hàm tool tra cứu lịch + 1 hàm điều phối `execute_tool` + danh sách schema cho Claude API.

### 3 hàm tool cần viết

**1. `get_schedule_by_date(date: str) -> dict`**
- Input: ngày dạng `"YYYY-MM-DD"`
- Output: `{ "date": "...", "weekday": "...", "morning": "...", "afternoon": "..." }`
- Lỗi: `{ "error": "Không tìm thấy lịch học cho ngày ..." }`

**2. `search_schedule_by_topic(keyword: str) -> dict`**
- Input: từ khóa, ví dụ `"Vector Store"`
- Output: `{ "results": [ { "date": "...", "weekday": "...", "session": "...", "content": "..." }, ... ] }`
- Không tìm thấy: `{ "results": [], "message": "Không tìm thấy nội dung liên quan đến '...'" }`
- Tìm kiếm không phân biệt hoa thường

**3. `get_session_detail(date: str, session: str) -> dict`**
- Input: ngày + buổi (`"morning"` hoặc `"afternoon"`)
- Output: `{ "date": "...", "weekday": "...", "session": "Buổi sáng/chiều", "content": "..." }`
- Session không hợp lệ: `{ "error": "Session không hợp lệ. Dùng 'morning' hoặc 'afternoon'." }`

### Hàm điều phối

```python
TOOL_HANDLERS = {
    "get_schedule_by_date": lambda params: get_schedule_by_date(**params),
    "search_schedule_by_topic": lambda params: search_schedule_by_topic(**params),
    "get_session_detail": lambda params: get_session_detail(**params),
}

def execute_tool(tool_name: str, parameters: dict) -> str:
    """Gọi tool theo tên, trả về JSON string."""
    ...
```

### TOOL_SCHEMAS

Danh sách 3 dict, mỗi dict có:
- `"name"`: tên tool
- `"description"`: mô tả tool
- `"input_schema"`: JSON Schema (type object, properties, required)

Đây là format Claude API yêu cầu cho tham số `tools`.

### Export

- `TOOL_SCHEMAS` — list 3 schema dicts
- `execute_tool` — function

### Kiểm tra

```python
from tools import TOOL_SCHEMAS, execute_tool
assert len(TOOL_SCHEMAS) == 3
import json
r1 = json.loads(execute_tool("get_schedule_by_date", {"date": "2026-06-02"}))
assert r1["weekday"] == "Thứ Ba"
r2 = json.loads(execute_tool("search_schedule_by_topic", {"keyword": "ReAct"}))
assert len(r2["results"]) >= 1
```

---

## Người 3 — Module Agent (ReAct Loop)

| Hạng mục | Chi tiết |
|---|---|
| File | `agent.py` |
| Import | `from tools import TOOL_SCHEMAS, execute_tool` |
| Độ khó | ⭐⭐⭐ Khó nhất |
| Ước lượng | 45 phút |

### Nhiệm vụ

Xây dựng class `ScheduleAgent` chạy ReAct loop với Claude API.

### Class ScheduleAgent

```python
class ScheduleAgent:
    def __init__(self):
        self.client = Anthropic()   # tự đọc ANTHROPIC_API_KEY từ env
        self.messages = []

    def chat(self, user_input: str) -> str:
        """
        Gửi user_input → chạy ReAct loop → trả final answer.
        In ra terminal: 💭 Thought, ⚡ Action, 👁️ Observation
        """
        ...
```

### Logic ReAct Loop

```
while True:
    1. Gọi client.messages.create(model, system, tools, messages)
    2. Tách response.content thành text_blocks và tool_use_blocks
    3. Nếu CÓ tool_use_blocks:
       - In Thought (text_blocks)
       - Append assistant message vào self.messages
       - Với mỗi tool_use: gọi execute_tool() → in Action + Observation
       - Append tool_results vào self.messages (role: "user")
       - Loop lại bước 1
    4. Nếu KHÔNG có tool_use_blocks:
       - Đây là final answer
       - Trả về text
```

### System Prompt

```
Bạn là trợ lý học tập hỗ trợ sinh viên tra cứu lịch học và nội dung khóa học.
Lịch học diễn ra từ ngày 01/06/2026 (Thứ Hai) đến 05/06/2026 (Thứ Sáu).
Bạn có các tool để tra cứu dữ liệu. Hãy sử dụng chúng để trả lời câu hỏi.
Khi người dùng hỏi theo ngày trong tuần, suy ra ngày rồi gọi tool.
Trả lời bằng tiếng Việt, ngắn gọn, rõ ràng.
```

### Hàm main()

```python
def main():
    # Kiểm tra ANTHROPIC_API_KEY
    # Khởi tạo ScheduleAgent
    # Vòng lặp: input → agent.chat() → in kết quả
    # Gõ 'quit'/'exit' để thoát
```

### Lưu ý kỹ thuật

- Dùng `python-dotenv`: `from dotenv import load_dotenv; load_dotenv()`
- Model: `claude-sonnet-4-620250514`
- `max_tokens`: 1024
- Khi append tool results, dùng format: `[{"type": "tool_result", "tool_use_id": ..., "content": ...}]`

### Kiểm tra

```bash
export ANTHROPIC_API_KEY="..."
python -c "from agent import ScheduleAgent; a = ScheduleAgent(); print(a.chat('Thứ Ba học gì?'))"
```

---

## Người 4 — Entry Point + Config + Test

| Hạng mục | Chi tiết |
|---|---|
| Files | `main.py`, `requirements.txt`, `.env`, `.gitignore`, `README.md` |
| Độ khó | ⭐ Dễ + vai trò ghép nối |
| Ước lượng | 15 phút code + 30 phút test |

### 4.1 — main.py

```python
"""Agent Hỗ trợ Tra cứu Lịch học — Entry Point"""
from agent import main

if __name__ == "__main__":
    main()
```

### 4.2 — requirements.txt

```
anthropic>=0.39.0
python-dotenv>=1.0.0
```

### 4.3 — .env

```
ANTHROPIC_API_KEY=your-api-key-here
```

### 4.4 — .gitignore

```
.env
__pycache__/
```

### 4.5 — README.md

Viết hướng dẫn:
- Mô tả dự án
- Cài đặt (`pip install -r requirements.txt`)
- Cấu hình API key
- Chạy (`python main.py`)
- Ví dụ câu hỏi test

### 4.6 — Test toàn bộ

Test 3 kịch bản chính và ghi kết quả:

| # | Câu hỏi test | Tool mong đợi | Ghi chú |
|---|---|---|---|
| 1 | "Thứ Ba học gì?" | `get_schedule_by_date("2026-06-02")` | Test theo ngày trong tuần |
| 2 | "Nội dung Vector Store học vào ngày nào?" | `search_schedule_by_topic("Vector Store")` | Test theo chủ đề |
| 3 | "Sáng thứ Hai học gì?" | `get_session_detail("2026-06-01", "morning")` | Test theo buổi cụ thể |

Nếu lỗi → xác định lỗi ở module nào → báo lại người phụ trách.

---

## Tóm tắt nhanh

| Người | File | Vai trò | Thời gian |
|---|---|---|---|
| 1 | `schedule_data.py` | Nhập dữ liệu lịch học | 15 phút |
| 2 | `tools.py` | Viết 3 tool functions + schemas | 30 phút |
| 3 | `agent.py` | ReAct loop + Claude API | 45 phút |
| 4 | `main.py` + config | Entry point + ghép nối + test | 45 phút |
