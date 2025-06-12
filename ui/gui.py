import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import PyQt6
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QHBoxLayout,
)
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap
from PyQt6.QtCore import QSize
from pathlib import Path

# No QT_QPA_PLATFORM_PLUGIN_PATH set here

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)

class CertGeneratorUI(QWidget):
    def __init__(self, main_func):
        """
        Initialize the UI.
        """
        super().__init__()
        self.setWindowTitle("Certificate Generator")
        self.main = main_func
        # Do not override background color here; let QSS handle it

        self.csv_path = None
        self.template_path = None

        # Asset paths
        assets_path = Path(resource_path("ui/assets"))
        og_path = assets_path / "OG-CUHK-840.png"
        cuhk_path = assets_path / "faculty-logo.png"
        zoom_path = assets_path / "zoom.png"

        # OG Logo
        self.og_label = QLabel()
        if og_path.exists():
            self.og_label.setPixmap(QPixmap(str(og_path)))
        else:
            self.og_label.setText("OG Logo")
            self.og_label.setProperty("class", "text-label")
        self.og_label.setScaledContents(True)
        self.og_label.setFixedSize(QSize(50, 50))

        # CUHK Logo
        self.cuhk_label = QLabel()
        if cuhk_path.exists():
            self.cuhk_label.setPixmap(QPixmap(str(cuhk_path)))
        else:
            self.cuhk_label.setText("CUHK Logo")
            self.cuhk_label.setProperty("class", "text-label")
        self.cuhk_label.setScaledContents(True)
        self.cuhk_label.setFixedSize(QSize(55, 50))

        # Zoom logo
        self.zoom_label = QLabel()
        if zoom_path.exists():
            self.zoom_label.setPixmap(QPixmap(str(zoom_path)))
        else:
            self.zoom_label.setText("Zoom Logo")
            self.zoom_label.setProperty("class", "text-label")
        self.zoom_label.setScaledContents(True)
        self.zoom_label.setFixedSize(QSize(90, 70))

        # Create the layout
        main_layout = QVBoxLayout()

        # Logo layout
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.og_label)
        logo_layout.addWidget(self.cuhk_label)
        logo_layout.addStretch()
        logo_layout.addWidget(self.zoom_label)
        main_layout.addLayout(logo_layout)

        # CSV row
        self.csv_label = QLabel("CSV File: Not selected")
        self.csv_label.setProperty("class", "text-label")
        self.btn_csv = QPushButton("Upload")
        self.btn_csv.clicked.connect(self.select_csv)
        csv_layout = QHBoxLayout()
        csv_layout.addWidget(self.csv_label)
        csv_layout.addStretch()
        csv_layout.addWidget(self.btn_csv)
        main_layout.addLayout(csv_layout)

        # Template row
        self.template_label = QLabel("Word Template: Not selected")
        self.template_label.setProperty("class", "text-label")
        self.btn_template = QPushButton("Upload")
        self.btn_template.clicked.connect(self.select_template)
        template_layout = QHBoxLayout()
        template_layout.addWidget(self.template_label)
        template_layout.addStretch()
        template_layout.addWidget(self.btn_template)
        main_layout.addLayout(template_layout)

        # Generate row
        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setObjectName("btn_generate")
        self.btn_generate.clicked.connect(self.generate_certificates)
        generate_layout = QHBoxLayout()
        generate_layout.addStretch()
        generate_layout.addWidget(self.btn_generate)
        generate_layout.addStretch()
        main_layout.addLayout(generate_layout)

        # Status label
        self.status_label = QLabel("Status: Waiting for input")
        self.status_label.setProperty("class", "text-label")
        main_layout.addWidget(self.status_label)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        self.setLayout(main_layout)

    def select_csv(self):
        """
        Select the CSV file.
        """
        
        csv_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if csv_path:
            self.csv_path = csv_path
            self.csv_label.setText(f"CSV File: {csv_path}")

    def select_template(self):
        """
        Select the Word template.
        """
        template_path, _ = QFileDialog.getOpenFileName(self, "Select Word Template", "", "Word Documents (*.docx)")
        if template_path:
            self.template_path = template_path
            self.template_label.setText(f"Word Template: {template_path}")

    def generate_certificates(self):
        """
        Generate the certificates.
        """
        if not self.csv_path or not self.template_path:
            self.status_label.setText("❌ Please select both a CSV file and a Word template.")
            return

        try:
            self.status_label.setText("⚙️ Processing, please wait...")
            QApplication.processEvents()

            saved_files = self.main(self.csv_path, self.template_path)

            self.log_output.clear()
            self.log_output.append("✅ Certificates generated successfully:")
            for path in saved_files:
                self.log_output.append(f"✅ Saved: 📄 {path}")

            self.status_label.setText("✅ All certificates generated!")
        except Exception as e:
            self.status_label.setText(f"❌ Error: {e}")


if __name__ == "__main__":
    from main import main
    app = QApplication(sys.argv)

    font_path = Path(resource_path("ui/assets/noto-sans.ttf"))
    font_id = QFontDatabase.addApplicationFont(str(font_path))
    
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))
    else:
        print("Warning: Custom font failed to load")

    # Load QSS style before creating the window
    try:
        style_path = resource_path("ui/style.qss")
        print(f"[DEBUG] Loading QSS from: {style_path}")
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    except Exception as e:
        print(f"Warning: Failed to load style.qss - {e}")

    # Show main window
    window = CertGeneratorUI(main)
    window.show()

    sys.exit(app.exec())
