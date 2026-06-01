# schedule_data.py
import csv
import logging
from pathlib import Path


# Đường dẫn tới file CSV
DATA_FILE = Path(__file__).parent / "data" / "schedule.csv"

# Các cột bắt buộc trong CSV
REQUIRED_COLUMNS = ["date", "weekday", "morning", "afternoon"]

# Cấu hình log
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    force=True
)

logger = logging.getLogger(__name__)


def validate_row(row: dict, row_number: int) -> bool:
    """
    Kiểm tra một dòng dữ liệu trong CSV có hợp lệ không.
    Trả về True nếu hợp lệ, False nếu không hợp lệ.
    """
    for column in REQUIRED_COLUMNS:
        value = row.get(column)

        if value is None:
            logger.error("Dòng %s bị thiếu cột '%s'", row_number, column)
            return False

        if value.strip() == "":
            logger.error("Dòng %s có dữ liệu rỗng ở cột '%s'", row_number, column)
            return False

    return True


def load_schedule() -> dict:
    """
    Đọc dữ liệu lịch học từ file CSV và chuyển thành dictionary SCHEDULE.

    Output:
    {
        "2026-06-01": {
            "weekday": "Thứ Hai",
            "morning": "...",
            "afternoon": "..."
        }
    }
    """
    schedule = {}

    logger.info("Bắt đầu đọc dữ liệu từ file: %s", DATA_FILE)

    if not DATA_FILE.exists():
        logger.error("Không tìm thấy file dữ liệu: %s", DATA_FILE)
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {DATA_FILE}")

    with open(DATA_FILE, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            logger.error("File CSV không có header")
            raise ValueError("File CSV không có header")

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            logger.error("File CSV thiếu cột bắt buộc: %s", missing_columns)
            raise ValueError(f"File CSV thiếu cột bắt buộc: {missing_columns}")

        for row_number, row in enumerate(reader, start=2):
            if not validate_row(row, row_number):
                logger.warning("Bỏ qua dòng không hợp lệ: %s", row_number)
                continue

            date = row["date"].strip()

            if date in schedule:
                logger.warning("Ngày %s bị trùng, dữ liệu mới sẽ ghi đè dữ liệu cũ", date)

            schedule[date] = {
                "weekday": row["weekday"].strip(),
                "morning": row["morning"].strip(),
                "afternoon": row["afternoon"].strip(),
            }

            logger.info("Đã load dữ liệu ngày %s", date)

    if not schedule:
        logger.error("Không có dữ liệu lịch học hợp lệ nào được load")
        raise ValueError("Không có dữ liệu lịch học hợp lệ nào được load")

    logger.info("Hoàn tất load dữ liệu. Tổng số ngày: %s", len(schedule))

    return schedule


SCHEDULE = load_schedule()


if __name__ == "__main__":
    print("Kiểm tra dữ liệu lịch học")
    print("Số ngày:", len(SCHEDULE))
    print("Ngày 2026-06-02:", SCHEDULE.get("2026-06-02"))