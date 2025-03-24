# PDF zu Markdown Konverter - Detaillierte Anleitung für Linux/Ubuntu

## Inhaltsverzeichnis

1.  **Einleitung**

2.  **Funktionen**
    
3.  **Systemanforderungen**
    
4.  **Installation**
    
5.  **Nutzung**
    
6.  **Leistung und Genauigkeit**
    
7.  **Einschränkungen**
    
8.  **Verwendung in nachgelagerten Aufgaben**
    
9.  **Mitwirkung**
    
10.  **Lizenz**
    

## 1. Einleitung

Dieses Projekt dient der Extraktion von Markdown-formatierten Inhalten aus PDF-Dateien. Es wurde speziell für nachgelagerte Aufgaben wie Retrieval Augmented Generation (RAG) entwickelt. Die Umwandlung bewahrt verschiedene Markdown-Elemente wie Tabellen, Bilder, Links, Fett- und Kursivtext, Blockzitate und Codeblöcke. Die Umsetzung erfolgt mit Python-Bibliotheken wie PyMuPDF (fitz), pdfplumber, pytesseract und anderen.

## 2. Funktionen

*   Extrahiert Text, Bilder, Tabellen und Codeblöcke aus PDFs
    
*   Konvertiert PDF-Inhalte in Markdown-Format, optimiert für RAG und NLP-Aufgaben
    
*   Bewahrt Formatierungen wie Fett/Kursiv, Tabellen, Bilder, Links, Listen und Codeblöcke
    
*   Handhabt komplexe Layouts inklusive mehrspaltigem Text
    
*   Führt OCR auf Bildern durch, um Text zu extrahieren
    
*   Generiert Bildunterschriften mit einem vortrainierten Modell
    
*   Gibt sauberes, strukturiertes Markdown für Information Retrieval und Textgenerierung aus
    

## 3. Systemanforderungen

*   **Betriebssystem:** Ubuntu 20.04 oder neuer
    
*   **Python-Version:** 3.8 oder höher | Aktuell Verwendet 3.12
    
*   **Benötigte Python-Bibliotheken:**
    ```
    PyMuPDF
    tk
    PyQt5
    opencv-python-headless
    pdfplumber
    pytesseract
    opencv-python
    transformers
    torch
    Pillow
    ```

## 4. Installation

- 4.1 Repository klonen:

    ```
    git clone https://gitlab.com/Spooner2000pdf-to-markdown-converter-python3.xx.git
    ```

- 4.2 Virtuelle Umgebung erstellen (optional, aber empfohlen) mit python
    ```
    python -m venv venv
    source venv/bin/activate

    (Letzte Version von Python-PIP installieren)
    python -m pip install --upgrade pip
    ```

    oder mit python3

    ```
    python3 -m venv venv
    source venv/bin/activate

    (Letzte Version von Python-PIP installieren)
    python3 -m pip install --upgrade pip
    ```

- 4.3 Benötigte Pakete installieren mit python
     ```
    python setup.py
    ```

    oder mit python3

    ```
    python3 setup.py
    ```

- 4.4 Tesseract OCR installieren(manuel falls nicht automatisch installiert)

    ```
    sudo apt-get install tesseract-ocr tesseract-ocr-deu 
    ```

    Für Windows: [Windows Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

## 5. Nutzung

Das Skript mit der PDF-Datei als Argument ausführen:

- Das extrahierte Markdown wird im outputs-Verzeichnis gespeichert und erhält denselben Namen wie die Eingabe-PDF, jedoch mit der Endung .md.

## 6. Leistung und Genauigkeit

*   **Genauigkeit:** Hohe Präzision bei der Bewahrung der Dokumentstruktur. Gut geeignet für Texte, Tabellen, Bilder, Links und Codeblöcke. Sehr komplexe Layouts können eine manuelle Nachbearbeitung erfordern.
    
*   **Geschwindigkeit:** Die Verarbeitungszeit hängt von der PDF-Größe und -Komplexität ab. Ein 10-seitiges PDF mit gemischten Inhalten benötigt in der Regel 30-60 Sekunden.
    
*   **Optimierung für RAG:** Klare Trennung zwischen Abschnitten und Inhaltstypen, um einfache Verarbeitung für RAG-Systeme zu ermöglichen.
    

## 7. Einschränkungen

*   Nur für die Konvertierung von PDFs in Markdown vorgesehen.
    
*   Sehr große PDFs (100+ Seiten) können längere Verarbeitungszeiten benötigen.
    
*   Komplexe mathematische Formeln oder spezielle Symbole werden nicht immer perfekt konvertiert.
    
*   Gescannte PDFs ohne eingebetteten Text sind auf OCR angewiesen, das nicht 100% exakt sein kann.
    

## 8. Verwendung in nachgelagerten Aufgaben

Die generierte Markdown-Datei eignet sich besonders für:

*   **Retrieval Augmented Generation (RAG):** Ermöglicht leichtes Indexieren und Abrufen von Kontext für Sprachmodelle.
    
*   **Textzusammenfassung:** Saubere Markdown-Formatierung verbessert die Qualität automatischer Zusammenfassungen.
    
*   **Informationsextraktion:** Klare Struktur erleichtert das Auffinden spezifischer Informationen.
    

## 9. Mitwirkung

Beiträge zur Verbesserung der Genauigkeit, Geschwindigkeit oder Funktionalität sind willkommen. Vorschläge und Pull Requests können im GitHub-Repository eingereicht werden.

## 10. Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details befinden sich in der LICENSE-Datei.