# Individual Report: Lab 3 - Chatbot vs ReAct Agent

* **Student Name**: Vũ Văn Huy
* **Student ID**: 2A202600750
* **Date**: 01/06/2026

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase.*

* **Modules Implementated**:

  * `schedule_data.py`
  * `data/schedule.csv`

* **Code Highlights**:
  Tôi phụ trách phần **module dữ liệu** cho Agent tra cứu lịch học. Module `schedule_data.py` có nhiệm vụ đọc dữ liệu từ file CSV và chuyển thành dictionary `SCHEDULE`.

```python
DATA_FILE = Path(__file__).parent / "data" / "schedule.csv"
REQUIRED_COLUMNS = ["date", "weekday", "morning", "afternoon"]
```

Tôi sử dụng `csv.DictReader` để đọc file và kiểm tra các cột bắt buộc. Nếu thiếu cột hoặc dữ liệu trong dòng bị rỗng, chương trình sẽ ghi log lỗi.

```python
def validate_row(row: dict, row_number: int) -> bool:
    for column in REQUIRED_COLUMNS:
        value = row.get(column)

        if value is None:
            logger.error("Dòng %s bị thiếu cột '%s'", row_number, column)
            return False

        if value.strip() == "":
            logger.error("Dòng %s có dữ liệu rỗng ở cột '%s'", row_number, column)
            return False

    return True
```

Dữ liệu hợp lệ sẽ được thêm vào dictionary `schedule`:

```python
schedule[date] = {
    "weekday": row["weekday"].strip(),
    "morning": row["morning"].strip(),
    "afternoon": row["afternoon"].strip(),
}
```

* **Documentation**:
  Module này là tầng dữ liệu của hệ thống. Các tool trong ReAct Agent sẽ truy xuất biến `SCHEDULE` để trả lời câu hỏi của người dùng về lịch học theo ngày, theo thứ hoặc theo nội dung buổi học.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

* **Problem Description**:
  Khi kiểm thử, tôi thử xoá giá trị `"Thứ Ba"` trong cột `weekday` của file `schedule.csv`. Khi đó dòng dữ liệu này bị xem là không hợp lệ.

* **Log Source**:

```text
ERROR - Dòng 3 có dữ liệu rỗng ở cột 'weekday'
WARNING - Bỏ qua dòng không hợp lệ: 3
```

* **Diagnosis**:
  Lỗi này đến từ dữ liệu đầu vào, không phải từ LLM hay ReAct loop. Vì file CSV là nguồn dữ liệu chính, nếu một dòng bị thiếu thông tin thì Agent có thể không tra cứu được lịch học chính xác.

* **Solution**:
  Tôi dùng hàm `validate_row()` để kiểm tra từng dòng trước khi đưa vào `SCHEDULE`. Nếu dòng lỗi, chương trình ghi log rõ dòng nào và cột nào bị lỗi, sau đó bỏ qua dòng đó bằng `continue`.

```python
if not validate_row(row, row_number):
    logger.warning("Bỏ qua dòng không hợp lệ: %s", row_number)
    continue
```

Cách này giúp dễ phát hiện lỗi trong file CSV và tránh đưa dữ liệu sai vào hệ thống.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1. **Reasoning**:
   ReAct Agent tốt hơn chatbot thường vì nó có thể phân tích câu hỏi, chọn tool phù hợp, gọi tool lấy dữ liệu rồi mới trả lời. Nhờ vậy câu trả lời bám sát dữ liệu thật hơn.

2. **Reliability**:
   Agent có thể hoạt động kém hơn chatbot khi tool, API key hoặc dữ liệu đầu vào bị lỗi. Ví dụ, nếu file CSV thiếu dữ liệu hoặc tool schema sai, Agent có thể không trả lời được dù câu hỏi đơn giản.

3. **Observation**:
   Observation giúp Agent biết kết quả sau khi gọi tool. Nếu tool trả về dữ liệu đúng, Agent dùng dữ liệu đó để trả lời. Nếu tool không tìm thấy dữ liệu, Agent cần thông báo rõ cho người dùng.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

* **Scalability**:
  Có thể thay file CSV bằng database để lưu nhiều lịch học, nhiều khóa học và nhiều tuần học hơn.

* **Safety**:
  Nên kiểm tra dữ liệu chặt hơn. Nếu thiếu dữ liệu quan trọng, chương trình nên dừng lại thay vì bỏ qua dòng lỗi để tránh Agent trả lời thiếu thông tin.

* **Performance**:
  Với dữ liệu nhỏ, dictionary là đủ. Nếu dữ liệu lớn hơn, có thể dùng database hoặc search index để tra cứu nhanh hơn. Log cũng nên được lưu theo từng phiên để dễ debug.

---

