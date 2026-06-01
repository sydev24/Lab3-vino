# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Vũ Quốc Bảo
- **Student ID**: 2A202600541
- **Date**: 01/06/2026

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implemented**: `app.py` (Streamlit UI), `agent.py` (Claude API integration & tool conversion), `.env` setup
- **Code Highlights**:

```python
# agent.py — Convert OpenAI tool schemas sang Anthropic format
def _convert_to_anthropic_tools(schemas: list[dict]) -> list[dict]:
    tools = []
    for s in schemas:
        func = s["function"]
        tools.append({
            "name": func["name"],
            "description": func["description"],
            "input_schema": func["parameters"],
        })
    return tools
```

```python
# app.py — Streamlit chat interface with session state
if "agent" not in st.session_state:
    st.session_state.agent = ScheduleAgent()
```

- **Documentation**: Xây dựng giao diện Streamlit (`app.py`) cho phép sinh viên tương tác với Agent qua chat UI. Tích hợp Claude API thông qua OpenRouter, xử lý lỗi tool schema format mismatch giữa OpenAI và Anthropic SDK. Implement `_convert_to_anthropic_tools()` để chuyển đổi TOOL_SCHEMAS từ OpenAI format sang Anthropic format trước khi gọi API.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Agent bị lỗi 401 `authentication_error: invalid x-api-key` khi sử dụng OpenRouter key (`sk-or-v1-...`) trực tiếp với Anthropic SDK. Sau đó fix base_url nhưng gặp lỗi 404 "Not Found" do trùng `/v1`. Tiếp theo lỗi 400 `Unknown server-tool shorthand` do TOOL_SCHEMAS dùng OpenAI format thay vì Anthropic format.

- **Log Source**:
```
Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}}
Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Invalid Anthropic Messages API request',
  'metadata': {'raw': '[{"code": "custom", "path": ["tools", 0, "type"], "message": "Unknown server-tool shorthand"}]'}}}
```

- **Diagnosis**:
  1. **401**: OpenRouter key không tương thích trực tiếp với Anthropic SDK — cần chỉ định `base_url` trỏ đến OpenRouter.
  2. **404**: Anthropic SDK tự động nối `/v1/messages` vào base_url,导致 `https://openrouter.ai/api/v1/v1/messages` bị trùng path.
  3. **400**: `TOOL_SCHEMAS` trong `tools.py` dùng OpenAI format (`"type": "function"`, `"function": {...}`), nhưng Anthropic API yêu cầu `"name"`, `"description"`, `"input_schema"`.

- **Solution**:
  1. Thêm `base_url="https://openrouter.ai/api"` vào `Anthropic()` constructor (bỏ `/v1` vì SDK tự thêm).
  2. Viết hàm `_convert_to_anthropic_tools()` chuyển đổi format tool schemas trước khi gửi request.
  3. Đổi model name từ `"claude-haiku-3"` sang `"anthropic/claude-3.5-haiku"` (đúng format OpenRouter).

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1. **Reasoning**: Khối `Thought` trong ReAct loop giúp Agent phân tích câu hỏi trước khi hành động. Ví dụ, khi người dùng hỏi "Thứ Ba học gì?", Agent suy luận cần chuyển "Thứ Ba" thành `2026-06-02` trước khi gọi `get_schedule_by_date`. Chatbot thông thường sẽ không có bước suy luận này — nó sẽ trả lời trực tiếp dựa trên pattern matching, dễ sai nếu câu hỏi phức tạp.

2. **Reliability**: Agent thực hiện *tốt hơn* Chatbot ở các câu hỏi cụ thể theo ngày hoặc buổi. Tuy nhiên, Agent có thể *kém hơn* Chatbot khi câu hỏi mơ hồ hoặc ngoài phạm vi — vì Agent phải gọi tool trước rồi mới từ chối, tốn thêm một bước API call. Chatbot có thể từ chối ngay lập tức.

3. **Observation**: Kết quả từ tool (Observation) đóng vai trò "ground truth" cho Agent. Khi `search_schedule_by_topic` trả về `{"results": []}`, Agent biết chắc chắn không có dữ liệu và trả lời "Không tìm thấy" thay vì đoán. Điều này giúp Agent đáng tin cậy hơn so với Chatbot tự sinh câu trả lời.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Sử dụng message queue (Redis/RabbitStack) để xử lý nhiều request đồng thời thay vì blocking I/O. Deploy Agent dưới dạng microservice với FastAPI, tách riêng phần tool execution ra service độc lập.

- **Safety**: Implement "Supervisor LLM" để audit câu trả lời của Agent trước khi gửi cho người dùng — kiểm tra hallucination và đảm bảo câu trả lời đúng với dữ liệu tool trả về. Thêm rate limiting per-user thay vì per-session.

- **Performance**: Cache kết quả tool calls cho các câu hỏi phổ biến (ví dụ: "Thứ Hai học gì?" được hỏi nhiều lần). Sử dụng Vector DB (ChromaDB) để tìm kiếm ngữ nghĩa thay vì exact match — cho phép người dùng hỏi tự nhiên hơn.

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_VU_QUOC_BAO.md` and placing it in this folder.
