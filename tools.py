import json
from schedule_data import SCHEDULE

def get_schedule_by_date(date: str) -> dict:
    if date in SCHEDULE:
        data = SCHEDULE[date]
        return {
            "date": date,
            "weekday": data["weekday"],
            "morning": data["morning"],
            "afternoon": data["afternoon"]
        }
    return {"error": f"Không tìm thấy lịch học cho ngày {date}"}

def search_schedule_by_topic(keyword: str) -> dict:
    results = []
    keyword_lower = keyword.lower()
    for date, data in SCHEDULE.items():
        for session in ["morning", "afternoon"]:
            if keyword_lower in data[session].lower():
                results.append({
                    "date": date,
                    "weekday": data["weekday"],
                    "session": "Buổi sáng" if session == "morning" else "Buổi chiều",
                    "content": data[session]
                })
    if results:
        return {"results": results}
    return {"results": [], "message": f"Không tìm thấy nội dung liên quan đến '{keyword}'"}

def get_session_detail(date: str, session: str) -> dict:
    if session not in ["morning", "afternoon"]:
        return {"error": "Session không hợp lệ. Dùng 'morning' hoặc 'afternoon'."}
    if date in SCHEDULE:
        data = SCHEDULE[date]
        return {
            "date": date,
            "weekday": data["weekday"],
            "session": "Buổi sáng" if session == "morning" else "Buổi chiều",
            "content": data[session]
        }
    return {"error": f"Không tìm thấy lịch học cho ngày {date}"}

TOOL_HANDLERS = {
    "get_schedule_by_date": lambda params: get_schedule_by_date(**params),
    "search_schedule_by_topic": lambda params: search_schedule_by_topic(**params),
    "get_session_detail": lambda params: get_session_detail(**params),
}

def execute_tool(tool_name: str, parameters: dict) -> str:
    """Gọi tool theo tên, trả về JSON string."""
    if tool_name in TOOL_HANDLERS:
        try:
            result = TOOL_HANDLERS[tool_name](parameters)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)

# Chuyển Schema sang chuẩn OpenAI để tương thích tốt nhất với OpenRouter
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_schedule_by_date",
            "description": "Lấy thông tin lịch học đầy đủ (sáng và chiều) của một ngày cụ thể.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Ngày cần tra cứu theo định dạng YYYY-MM-DD, ví dụ: '2026-06-01'"
                    }
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_schedule_by_topic",
            "description": "Tìm kiếm các buổi học có chứa từ khóa hoặc chủ đề nhất định.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Từ khóa tìm kiếm, ví dụ: 'Vector Store', 'ReAct'"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_session_detail",
            "description": "Lấy thông tin chi tiết lịch học của một buổi cụ thể (sáng hoặc chiều) trong một ngày.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Ngày cần tra cứu theo định dạng YYYY-MM-DD, ví dụ: '2026-06-01'"
                    },
                    "session": {
                        "type": "string",
                        "description": "Buổi học cần tra cứu. Chỉ chấp nhận 'morning' hoặc 'afternoon'"
                    }
                },
                "required": ["date", "session"]
            }
        }
    }
]
