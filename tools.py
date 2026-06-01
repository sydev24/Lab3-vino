import json
from schedule_data import SCHEDULE

# ==========================================
# 1. CÁC HÀM XỬ LÝ LOGIC TOOL
# ==========================================


def get_schedule_by_date(date: str) -> dict:
	"""Tra cứu lịch học của cả ngày dựa vào ngày YYYY-MM-DD."""
	if date in SCHEDULE:
		data = SCHEDULE[date]
		return {
			"date": date,
			"weekday": data["weekday"],
			"morning": data["morning"],
			"afternoon": data["afternoon"],
		}
	return {"error": f"Không tìm thấy lịch học cho ngày {date}"}


def search_schedule_by_topic(keyword: str) -> dict:
	"""Tìm kiếm lịch học theo từ khóa, không phân biệt hoa thường."""
	keyword_lower = keyword.lower()
	results = []

	for date, data in SCHEDULE.items():
		# Kiểm tra buổi sáng
		if keyword_lower in data["morning"].lower():
			results.append(
				{
					"date": date,
					"weekday": data["weekday"],
					"session": "morning",
					"content": data["morning"],
				}
			)
		# Kiểm tra buổi chiều
		if keyword_lower in data["afternoon"].lower():
			results.append(
				{
					"date": date,
					"weekday": data["weekday"],
					"session": "afternoon",
					"content": data["afternoon"],
				}
			)

	if results:
		return {"results": results}
	return {
		"results": [],
		"message": f"Không tìm thấy nội dung liên quan đến '{keyword}'",
	}


def get_session_detail(date: str, session: str) -> dict:
	"""Tra cứu chi tiết một buổi học cụ thể (morning/afternoon) trong một ngày."""
	if session not in ["morning", "afternoon"]:
		return {"error": "Session không hợp lệ. Dùng 'morning' hoặc 'afternoon'."}

	if date not in SCHEDULE:
		return {"error": f"Không tìm thấy lịch học cho ngày {date}"}

	data = SCHEDULE[date]
	session_vi = "Buổi sáng" if session == "morning" else "Buổi chiều"

	return {
		"date": date,
		"weekday": data["weekday"],
		"session": session_vi,
		"content": data[session],
	}


# ==========================================
# 2. HÀM ĐIỀU PHỐI (DISPATCHER)
# ==========================================


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
		except Exception as exc:
			return json.dumps(
				{"error": f"Lỗi khi thực thi tool {tool_name}: {str(exc)}"},
				ensure_ascii=False,
			)

	return json.dumps(
		{"error": f"Không tìm thấy tool nào có tên là '{tool_name}'"},
		ensure_ascii=False,
	)


# ==========================================
# 3. DANH SÁCH TOOL SCHEMAS CHO CLAUDE API
# ==========================================


TOOL_SCHEMAS = [
	{
		"name": "get_schedule_by_date",
		"description": "Tra cứu thông tin lịch học của toàn bộ một ngày cụ thể (bao gồm cả sáng và chiều).",
		"input_schema": {
			"type": "object",
			"properties": {
				"date": {
					"type": "string",
					"description": "Ngày cần tra cứu theo định dạng YYYY-MM-DD (ví dụ: '2026-06-01').",
				}
			},
			"required": ["date"],
		},
	},
	{
		"name": "search_schedule_by_topic",
		"description": "Tìm kiếm các ngày học và buổi học dựa trên chủ đề hoặc từ khóa cụ thể.",
		"input_schema": {
			"type": "object",
			"properties": {
				"keyword": {
					"type": "string",
					"description": "Từ khóa hoặc chủ đề môn học cần tìm kiếm (ví dụ: 'Vector Store', 'ReAct', 'PRD').",
				}
			},
			"required": ["keyword"],
		},
	},
	{
		"name": "get_session_detail",
		"description": "Tra cứu chi tiết nội dung học của một buổi cụ thể (sáng hoặc chiều) trong một ngày.",
		"input_schema": {
			"type": "object",
			"properties": {
				"date": {
					"type": "string",
					"description": "Ngày cần tra cứu theo định dạng YYYY-MM-DD (ví dụ: '2026-06-01').",
				},
				"session": {
					"type": "string",
					"description": "Chỉ định buổi học. Chỉ chấp nhận một trong hai giá trị: 'morning' (buổi sáng) hoặc 'afternoon' (buổi chiều).",
					"enum": ["morning", "afternoon"],
				},
			},
			"required": ["date", "session"],
		},
	},
]