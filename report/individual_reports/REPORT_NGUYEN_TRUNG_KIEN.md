# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyen Trung Kien
- **Student ID**: 2A202600696
- **Date**: 2026-06-01

## I. Technical Contribution (15 Points)
*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: `tools.py`
- **Code Highlights**: Xay dung 3 ham logic chinh: `get_schedule_by_date` (truy xuat theo ngay), `search_schedule_by_topic` (tim kiem theo tu khoa noi dung), va `get_session_detail` (chi tiet buoi sang/chieu).
- Thiet lap ham dieu phoi `execute_tool` de boc tach tham so va goi ham tuong ung thong qua `TOOL_HANDLERS`.
- Dinh nghia `TOOL_SCHEMAS` theo chuan Claude API (su dung `input_schema`) de Agent co the hieu duoc chuc nang va cau truc du lieu dau vao cua tung tool.

- **Documentation**: Module `tools.py` dong vai tro la "canh tay" cua Agent. Khi Agent (Nguoi 3) nhan yeu cau, no se phan tich y dinh, doi chieu voi `TOOL_SCHEMAS` de chon tool phu hop, sau do goi `execute_tool`. Ket qua tra ve tu tool duoi dang JSON string se duoc dua vao khoi `Observation` cua ReAct loop de Agent tong hop cau tra loi cuoi cung.

## II. Debugging Case Study (10 Points)
*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Loi mo hinh khong goi duoc tool do sai cau truc Schema (Mismatching Tool Spec).
- **Log Source**: `Output: "Error: Unexpected key 'parameters' in tool definition. Expected 'input_schema' for Claude API."`
- **Diagnosis**: Trong qua trinh phat trien, ban dau toi da nham lan giua dinh dang cua Gemini API (su dung `parameters`) va Claude API (su dung `input_schema`). Dieu nay dan den viec LLM nhan dien duoc ten tool nhung khong the khoi tao loi goi ham do sai dinh dang JSON Schema cua tham so dau vao.
- **Solution**: Cap nhat lai toan bo `TOOL_SCHEMAS` trong file `tools.py`, chuyen doi tu khoa `parameters` sang `input_schema` theo dung tai lieu ky thuat cua Anthropic danh cho `tool_use`.

## III. Personal Insights: Chatbot vs ReAct (10 Points)
*Reflect on the reasoning capability difference.*

1. **Reasoning**: Khoi `Thought` giup Agent co thoi gian "suy nghi" de chia nho nhiem vu. Thay vi tra loi bua khi khong co du lieu, `Thought` cho phep Agent nhan ra: "Toi can biet lich ngay Thu Ba, toi se goi tool `get_schedule_by_date`". Dieu nay Chatbot thong thuong khong lam duoc vi no chi co gang du doan tu tiep theo dua tren xac suat.
2. **Reliability**: Agent thuc hien te hon Chatbot khi cau hoi qua don gian hoac mang tinh chat giao tiep xa hoi (Small talk). Viec ep mot Agent ReAct phai thuc hien day du cac buoc Thought-Action-Observation cho mot cau "Chao ban" se gay ton Token va lam tang do tre (latency) khong can thiet.
3. **Observation**: Phan hoi tu moi truong (Observations) dong vai tro la bang chung thuc te. Neu tool tra ve "Khong tim thay lich hoc", Agent se dua vao do de dieu chinh hanh vi trong buoc `Thought` tiep theo (vi du: tim kiem bang tu khoa khac thay vi tim theo ngay) thay vi tra loi sai lech thong tin.

## IV. Future Improvements (5 Points)
*How would you scale this for a production-level AI agent system?*

- **Scalability**: Xay dung co che **Tool Retrieval**. Khi so luong tool len den hang tram, viec day tat ca vao System Prompt se lam day ngu canh (Context window). Can mot Vector DB de tim kiem va chi cung cap cac tool lien quan nhat cho moi cau hoi.
- **Safety**: Trien khai lop **Pydantic Validation** ngay tai dau vao cua cac ham trong `tools.py` de dam bao du lieu nguoi dung truyen vao khong chua ma doc hoac sai dinh dang truoc khi xu ly sau hon.
- **Performance**: Ap dung **Caching** cho cac ket qua truy van lich hoc pho bien. Neu nhieu sinh vien cung hoi ve lich ngay 01/06, Agent co the lay ket qua tu cache thay vi thuc hien lai toan bo luong logic/API call.