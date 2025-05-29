from excel_reader import read_attendee_data, filter_eligible_attendees, save_to_excel
from cert_generator import generate_certificates
from pathlib import Path

def main(csv_path, template_path):

    # Read the attendee data
    attendee_data = read_attendee_data(csv_path)
    if not attendee_data:
        raise Exception("No attendee data found")

    # Filter the eligible attendees
    eligible_attendees = filter_eligible_attendees(attendee_data)
    if not eligible_attendees:
        raise Exception("No eligible attendees found")

    # Save the eligible attendees to an Excel file
    output_excel_path = Path.home() / "Downloads" / "certs" / "eligible_attendees.xlsx"
    save_to_excel(eligible_attendees, output_excel_path)

    # Generate the certificates
    saved_cert = generate_certificates(template_path, eligible_attendees)
    return saved_cert

if __name__ == "__main__":
    from ui.gui import CertGeneratorUI
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = CertGeneratorUI()
    window.show()
    sys.exit(app.exec())
