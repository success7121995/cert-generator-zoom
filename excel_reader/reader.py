import csv
from collections import defaultdict
import pandas as pd
from pathlib import Path

def read_attendee_data(file_path):
    target_section = '觀眾詳細資訊'
    section_found = False
    headers = []
    attendee_data = []

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if not row:
                continue  # skip empty rows

            if target_section in row[0]:
                section_found = True
                continue

            if section_found and '已出席' in row[0] and '使用者名稱（原始名稱）' in row[1]:
                headers = row
                continue

            if section_found and headers:
                if len(row) >= len(headers):  # skip malformed rows
                    attendee_data.append(dict(zip(headers, row)))
                else:
                    print(f"[WARN] Skipping incomplete row: {row}")

    return attendee_data
    

def filter_eligible_attendees(attendee_list):
    target_specialty = "Nurse/Midwife"
    target_country = "香港特別行政區"
    min_duration = 30

    attendee_summary = defaultdict(lambda: {
        "名字": "",
        "姓氏": "",
        "電子郵件地址": "",
        "出席時間（分鐘）": 0,
        "Specialty": "",
        "國家/地區名稱": ""
    })

    for row in attendee_list:
        email = row.get("電子郵件地址", "").strip()
        specialty = row.get("Specialty", "").strip()
        country = row.get("國家/地區名稱", "").strip()
        duration_str = row.get("出席時間（分鐘）", "").strip()

        if not email or not duration_str.isdigit():
            continue

        duration = int(duration_str)

        # Check if the email is already in the summary
        if email in attendee_summary:
            attendee_summary[email]["出席時間（分鐘）"] += duration
        else:
            if specialty == target_specialty and country == target_country:
                attendee_summary[email] = {
                    "名字": row.get("名字", "").strip(),
                    "姓氏": row.get("姓氏", "").strip(),
                    "電子郵件地址": email,
                    "出席時間（分鐘）": duration,
                    "Specialty": specialty,
                    "國家/地區名稱": country
                }

    eligible_attendees = [
        data for data in attendee_summary.values()
        if data["出席時間（分鐘）"] >= min_duration
    ]

    # Add sequential ref to each eligible attendee
    for idx, data in enumerate(eligible_attendees, 1):
        data["ref"] = idx

    return eligible_attendees

def save_to_excel(eligible_attendees, output_path):
    """
    Save the eligible attendees to an Excel file.
    """
    # Create the output directory if it doesn't exist
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the eligible attendees to an Excel file
    df = pd.DataFrame(eligible_attendees)
    df.to_excel(str(output_path), index=False)