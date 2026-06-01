# Agent Hỗ trợ Tra cứu Lịch học

ReAct Agent sử dụng Claude API (via OpenRouter) hỗ trợ sinh viên tra cứu lịch học và nội dung khóa học AI tuần 01–05/06/2026. Agent có khả năng hiểu ngôn ngữ tự nhiên, tự động chọn tool phù hợp, gọi tool để lấy dữ liệu thực và trả lời chính xác.

---

## Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────┐
│                    app.py (Streamlit)                │
│              Chat UI + Suggestion buttons            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  agent.py (ReAct Loop)               │
│  ┌─────────┐   ┌─────────┐   ┌──────────────────┐  │
│  │ Thought │──▶│ Action  │──▶│  Observation     │  │
│  └─────────┘   └────┬────┘   └──────────────────┘  │
│                     │                               │
│         ┌───────────▼────────────┐                  │
│         │   Claude API (Haiku)   │                  │
│         │   via OpenRouter       │                  │
│         └────────────────────────┘                  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│               tools.py (3 Tools)                    │
│  • get_schedule_by_date(date)                       │
│  • search_schedule_by_topic(keyword)                │
│  • get_session_detail(date, session)                │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│           schedule_data.py → data/schedule.csv      │
│           5 ngày × 2 buổi (sáng + chiều)            │
└─────────────────────────────────────────────────────┘
```

---

## Cấu trúc thư mục

```
├── app.py                  # Streamlit UI (chat interface)
├── agent.py                # ReAct Agent loop + Claude API
├── tools.py                # 3 tool functions + schemas + dispatcher
├── schedule_data.py        # Load & validate CSV data
├── main.py                 # CLI entry point
├── test_agent.py           # Test suite đánh giá agent
├── data/
│   └── schedule.csv        # Dữ liệu lịch học 5 ngày
├── logs/                   # JSON-lines session logs (auto-created)
├── report/
│   ├── group_report/
│   └── individual_reports/
├── .env                    # ANTHROPIC_API_KEY (không commit)
├── .env.example            # Template cho .env
├── .gitignore
└── README.md
```

---

## Các tool Agent sử dụng

| Tool | Tham số | Mô tả |
|------|---------|-------|
| `get_schedule_by_date` | `date` (YYYY-MM-DD) | Tra cứu lịch cả ngày (sáng + chiều) |
| `search_schedule_by_topic` | `keyword` (string) | Tìm buổi học theo từ khóa/chủ đề |
| `get_session_detail` | `date` + `session` (morning/afternoon) | Chi tiết 1 buổi cụ thể |

---

## Cài đặt

### 1. Cài dependencies

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install anthropic python-dotenv streamlit
```

### 2. Cấu hình API Key

Tạo file `.env` ở thư mục gốc:

```env
ANTHROPIC_API_KEY=sk-or-v1-xxxxxxxxxxxx
```

> Sử dụng OpenRouter key (`sk-or-v1-...`). Agent đã cấu hình `base_url` trỏ đến OpenRouter.

### 3. Chạy ứng dụng

**Streamlit UI (khuyến nghị):**

```bash
streamlit run app.py
```

Mở trình duyệt tại `http://localhost:8501`

**CLI:**

```bash
python main.py
```

---

## Demo Flow

### Tình huống 1: Tra cứu theo ngày

```
Bạn: Thứ Ba học gì?
Agent: Thứ Ba, ngày 2026-06-02:
- Buổi sáng: Prompt Engineering & Tool Calling...
- Buổi chiều: Vibe Coding 4, Tool Development with AI...
```

### Tình huống 2: Tra cứu theo chủ đề

```
Bạn: Nội dung Vector Store học vào ngày nào?
Agent: Nội dung "Vector Store" được học vào:
- Buổi sáng Thứ Sáu (2026-06-05): Data Foundations...
- Buổi chiều Thứ Sáu (2026-06-05): Vibe Coding 7...
```

### Tình huống 3: Tra cứu theo buổi cụ thể

```
Bạn: Sáng thứ Hai học gì?
Agent: Buổi sáng Thứ Hai, ngày 2026-06-01:
- Design Pattern ReAct, kiến trúc Agent, Agent Loop...
```

---

## ReAct Loop (Thought → Action → Observation)

```
User: "Thứ Ba học gì?"

💭 Thought: Người dùng hỏi theo Thứ Ba → 2026-06-02
⚡ Action:  get_schedule_by_date({"date": "2026-06-02"})
👁️ Observation: {"date": "2026-06-02", "weekday": "Thứ Ba", "morning": "...", "afternoon": "..."}

→ Final Answer: Thứ Ba, ngày 2026-06-02: ...
```

---

## Guardrails & Safety

| Cơ chế | Mô tả |
|--------|-------|
| **Off-topic filter** | Chặn câu hỏi không liên quan (tin tức, toán, code...) trước khi gọi API |
| **Injection detection** | Regex phát hiện prompt injection (ignore instructions, roleplay, jailbreak...) |
| **Rate limiting** | Tối đa 5 request/phút/session |
| **Token budget** | Giới hạn 40,000 tokens/session |
| **Tool result sanitization** | Loại bỏ URL và injection phrases từ tool output |
| **PII masking** | Mask email, SĐT, MSSV trong logs |

---

## Tech Stack

- **LLM**: Claude 3.5 Haiku (via OpenRouter)
- **Framework**: Anthropic Python SDK
- **UI**: Streamlit
- **Data**: CSV (5 ngày × 2 buổi)
- **Logging**: JSON-lines per session
