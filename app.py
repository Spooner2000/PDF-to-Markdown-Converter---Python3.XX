import os
os.environ["QT_QPA_PLATFORM"] = "wayland"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/x86_64-linux-gnu/qt5/plugins"
os.environ.pop("QT_PLUGIN_PATH", None)

os.environ["QT_DEBUG_PLUGINS"] = "1"

import sys
import re
import traceback
import logging
import warnings
from pathlib import Path
from abc import ABC, abstractmethod

# Wichtig: Verwende opencv-python-headless (stelle sicher, dass es installiert ist)
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
import cv2
import numpy as np
from PIL import Image

import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

from PyQt5 import QtCore, QtGui, QtWidgets

warnings.filterwarnings("ignore")

# --- Konfiguration ---
output_dir = os.path.join(Path.home(), "Documents", "PDF-Markdown_Output")
config = {
    "OUTPUT_DIR": output_dir,
    "PAGE_DELIMITER": "\n\n---\n\n"
}

# --- PDF-Extraktions-Klassen (wie zuvor) ---

class PDFExtractor(ABC):
    """Abstrakte Basisklasse zur PDF-Extraktion."""
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.setup_logging()

    def setup_logging(self):
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{Path(__file__).stem}.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def extract(self):
        pass

class MarkdownPDFExtractor(PDFExtractor):
    """Extrahiert Markdown-formatierten Inhalt aus PDF."""
    BULLET_POINTS = "•◦▪▫●○"

    def __init__(self, pdf_path):
        super().__init__(pdf_path)
        self.pdf_filename = Path(pdf_path).stem
        Path(config["OUTPUT_DIR"]).mkdir(parents=True, exist_ok=True)
        self.setup_image_captioning()

    def setup_image_captioning(self):
        try:
            self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.logger.info("Image-Captioning-Modell eingerichtet.")
        except Exception as e:
            self.logger.error(f"Fehler beim Einrichten des Captioning-Modells: {e}")
            self.logger.exception(traceback.format_exc())

    def extract(self):
        try:
            markdown_content, _ = self.extract_markdown()
            self.save_markdown(markdown_content)
            self.logger.info(f"Markdown gespeichert: {Path(config['OUTPUT_DIR'])}/{self.pdf_filename}.md")
            return markdown_content
        except Exception as e:
            self.logger.error(f"Fehler bei der PDF-Verarbeitung: {e}")
            self.logger.exception(traceback.format_exc())
            return ""

    def extract_markdown(self):
        try:
            doc = fitz.open(self.pdf_path)
            markdown_content = ""
            markdown_pages = []
            tables = self.extract_tables()
            table_index = 0
            for page_num, page in enumerate(doc):
                self.logger.info(f"Verarbeite Seite {page_num + 1}")
                page_content = ""
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if block["type"] == 0:
                        page_content += self.process_text_block(block)
                    elif block["type"] == 1:
                        page_content += self.process_image_block(page, block)
                while table_index < len(tables) and tables[table_index]["page"] == page.number:
                    page_content += "\n\n" + self.table_to_markdown(tables[table_index]["content"]) + "\n\n"
                    table_index += 1
                markdown_pages.append(page_content)
                markdown_content += page_content + config["PAGE_DELIMITER"]
            return markdown_content, markdown_pages
        except Exception as e:
            self.logger.error(f"Fehler bei der Markdown-Extraktion: {e}")
            self.logger.exception(traceback.format_exc())
            return "", []

    def extract_tables(self):
        tables = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_number, page in enumerate(pdf.pages):
                    for table in page.extract_tables():
                        tables.append({"page": page_number, "content": table})
            self.logger.info(f"Extrahiert {len(tables)} Tabellen.")
        except Exception as e:
            self.logger.error(f"Fehler beim Tabellen-Extrahieren: {e}")
            self.logger.exception(traceback.format_exc())
        return tables

    def table_to_markdown(self, table):
        try:
            table = [[("" if cell is None else str(cell).strip()) for cell in row] for row in table]
            col_widths = [max(len(cell) for cell in col) for col in zip(*table)]
            md = ""
            for i, row in enumerate(table):
                formatted_row = [cell.ljust(col_widths[j]) for j, cell in enumerate(row)]
                md += "| " + " | ".join(formatted_row) + " |\n"
                if i == 0:
                    md += "|" + "|".join(["-" * (width + 2) for width in col_widths]) + "|\n"
            return md
        except Exception as e:
            self.logger.error(f"Fehler beim Konvertieren der Tabelle: {e}")
            self.logger.exception(traceback.format_exc())
            return ""

    def perform_ocr(self, image):
        try:
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            ocr_result = pytesseract.image_to_data(opencv_image, output_type=pytesseract.Output.DICT)
            result = ""
            for word in ocr_result["text"]:
                if word.strip():
                    result += word + " "
                if len(result) > 30:
                    break
            return result.strip()
        except Exception as e:
            self.logger.error(f"OCR-Fehler: {e}")
            self.logger.exception(traceback.format_exc())
            return ""

    def caption_image(self, image):
        try:
            ocr_text = self.perform_ocr(image)
            if ocr_text:
                return ocr_text
            if image.mode != "RGB":
                image = image.convert("RGB")
            image = np.array(image).transpose(2, 0, 1)
            inputs = self.feature_extractor(images=image, return_tensors="pt").to(self.device)
            generated_ids = self.model.generate(inputs.pixel_values, max_length=30)
            caption = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return caption.strip()
        except Exception as e:
            self.logger.error(f"Captioning-Fehler: {e}")
            self.logger.exception(traceback.format_exc())
            return ""

    def process_text_block(self, block):
        try:
            block_text = ""
            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]])
                block_text += line_text + "\n"
            return block_text
        except Exception as e:
            self.logger.error(f"Fehler beim Textblock: {e}")
            self.logger.exception(traceback.format_exc())
            return ""

    def process_image_block(self, page, block):
        try:
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat, clip=block["bbox"], alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image_filename = f"{self.pdf_filename}_image_{page.number+1}_{block.get('number',0)}.png"
            image_path = Path(config["OUTPUT_DIR"]) / image_filename
            image.save(image_path, "PNG", optimize=True, quality=95)
            caption = self.caption_image(image)
            if not caption:
                caption = image_filename
            return f"![{caption}]({image_path})\n\n"
        except Exception as e:
            self.logger.error(f"Fehler beim Bildblock: {e}")
            self.logger.exception(traceback.format_exc())
            return ""

    def save_markdown(self, markdown_content):
        try:
            os.makedirs(Path(config["OUTPUT_DIR"]), exist_ok=True)
            output_file = Path(config["OUTPUT_DIR"]) / f"{self.pdf_filename}.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            self.logger.info("Markdown erfolgreich gespeichert.")
        except Exception as e:
            self.logger.error(f"Speicherfehler: {e}")
            self.logger.exception(traceback.format_exc())

# --- Worker via QRunnable und QThreadPool (statt QThread) ---

class ConversionTask(QtCore.QRunnable):
    def __init__(self, pdf_files, callback):
        super().__init__()
        self.pdf_files = pdf_files
        self.callback = callback  # Callback-Funktion zur Status-Aktualisierung

    def run(self):
        total = len(self.pdf_files)
        for idx, pdf_file in enumerate(self.pdf_files, start=1):
            try:
                msg = f"Verarbeite ({idx}/{total}): {Path(pdf_file).name}"
                self.callback(msg)
                extractor = MarkdownPDFExtractor(pdf_file)
                extractor.extract()
            except Exception as e:
                self.callback(f"Fehler bei {pdf_file}: {e}")
        self.callback("Konvertierung abgeschlossen!")

# --- PyQt5 GUI mit Drag & Drop ---

class DraggableListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(DraggableListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event: QtGui.QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(".pdf"):
                    if not self.findItems(file_path, QtCore.Qt.MatchExactly):
                        self.addItem(file_path)
            event.acceptProposedAction()

class PDFConverterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PDFConverterWindow, self).__init__()
        self.setWindowTitle("PDF zu Markdown Konverter")
        self.resize(600, 400)
        self.init_ui()
        self.pool = QtCore.QThreadPool()

    def init_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        self.list_widget = DraggableListWidget()
        layout.addWidget(self.list_widget)
        
        self.status_label = QtWidgets.QLabel("Ziehe PDF-Dateien in das Feld oder wähle sie über den Button aus.")
        layout.addWidget(self.status_label)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        select_btn = QtWidgets.QPushButton("Dateien auswählen")
        select_btn.clicked.connect(self.select_files)
        button_layout.addWidget(select_btn)
        
        self.convert_btn = QtWidgets.QPushButton("Konvertieren")
        self.convert_btn.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.convert_btn)
        
        layout.addLayout(button_layout)
    
    def select_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "PDF-Dateien auswählen", "", "PDF-Dateien (*.pdf)")
        if files:
            for file in files:
                if not self.list_widget.findItems(file, QtCore.Qt.MatchExactly):
                    self.list_widget.addItem(file)
            self.status_label.setText(f"{self.list_widget.count()} PDF(s) ausgewählt.")
    
    def start_conversion(self):
        if self.list_widget.count() == 0:
            QtWidgets.QMessageBox.warning(self, "Keine Dateien", "Bitte füge PDF-Dateien hinzu!")
            return
        
        pdf_files = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        self.status_label.setText("Konvertierung gestartet...")
        self.convert_btn.setEnabled(False)
        
        def update_status(msg):
            # Da wir aus einem anderen Thread kommen, nutzen wir signal-slot-Mechanismus
            QtCore.QMetaObject.invokeMethod(self.status_label, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, msg))
        
        task = ConversionTask(pdf_files, update_status)
        self.pool.start(task)
        # Nach Abschluss des Tasks (hier über das letzte Status-Update) wird der Button wieder aktiviert
        # Du kannst auch einen Timer oder Signal verwenden, um den Abschluss genauer zu erkennen.
        # Hier simulieren wir das: Nach 5 Sekunden wird der Button wieder aktiviert.
        QtCore.QTimer.singleShot(5000, self.finish_conversion)
    
    def finish_conversion(self):
        self.convert_btn.setEnabled(True)
        self.list_widget.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PDFConverterWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
