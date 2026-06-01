import os
import json
import datetime
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOL_SCHEMAS, execute_tool

load_dotenv()

SYSTEM_PROMPT = """Bạn là trợ lý học tập hỗ trợ sinh viên tra cứu lịch học và nội dung khóa học.
Lịch học diễn ra từ ngày 01/06/2026 (Thứ Hai) đến 05/06/2026 (Thứ Sáu).
Bạn có các tool để tra cứu dữ liệu. Hãy sử dụng chúng để trả lời câu hỏi.
Khi người dùng hỏi theo ngày trong tuần, suy ra ngày rồi gọi tool.
Trả lời bằng tiếng Việt, ngắn gọn, rõ ràng."""

class ScheduleAgent:
    def __init__(self):
        # Dùng thư viện OpenAI để tương thích hoàn toàn với OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.model = "anthropic/claude-3-haiku"
        
        # Setup logging
        if not os.path.exists('logs'):
            os.makedirs('logs')

    def _log_telemetry(self, action_type: str, data: dict):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": action_type,
            "data": data
        }
        with open("logs/agent_telemetry.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def chat(self, user_input: str) -> str:
        """
        Gửi user_input → chạy ReAct loop → trả final answer.
        In ra terminal: 💭 Thought, ⚡ Action, 👁️ Observation
        """
        self.messages.append({"role": "user", "content": user_input})
        self._log_telemetry("USER_INPUT", {"input": user_input})
        
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # Ghi nhận Thought nếu có
            if message.content:
                print(f"\n💭 Thought: {message.content}")
                self._log_telemetry("THOUGHT", {"thought": message.content})
                
            # Lưu lại message của trợ lý
            self.messages.append(message)
            
            # Nếu KHÔNG gọi tool -> Đây là final answer
            if not message.tool_calls:
                final_answer = message.content or ""
                self._log_telemetry("FINAL_ANSWER", {"answer": final_answer})
                return final_answer
                
            # Nếu CÓ gọi tool -> Thực thi tool
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = tool_call.function.arguments
                
                print(f"⚡ Action: Calling {func_name} with params: {func_args}")
                self._log_telemetry("ACTION", {"tool": func_name, "params": func_args})
                
                # Parse arguments từ chuỗi JSON
                try:
                    args_dict = json.loads(func_args)
                except json.JSONDecodeError:
                    args_dict = {}
                
                result = execute_tool(func_name, args_dict)
                print(f"👁️ Observation: {result}")
                self._log_telemetry("OBSERVATION", {"result": result})
                
                # Trả kết quả của tool lại cho hệ thống
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": result
                })

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Lỗi: Chưa cấu hình ANTHROPIC_API_KEY trong file .env")
        return
        
    print("🤖 Schedule Agent (OpenRouter Edition) đã sẵn sàng! (Gõ 'quit' hoặc 'exit' để thoát)")
    agent = ScheduleAgent()
    
    while True:
        try:
            user_input = input("\nBạn: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Tạm biệt!")
                break
                
            if not user_input.strip():
                continue
                
            response = agent.chat(user_input)
            print(f"\n🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()
