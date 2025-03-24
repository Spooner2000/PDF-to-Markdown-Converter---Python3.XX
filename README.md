# PDF zu Markdown Konverter - Detaillierte Anleitung für Linux/Ubuntu

## Inhaltsverzeichnis

1.  **Beschreibung**

2.  **Funktionen**
    
3.  **Systemanforderungen**
    
4.  **Installation**
    
5.  **Lizenz**

## 1. Beschreibung

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
    pdfplumber
    pytesseract
    OpenCV (cv2)
    numpy
    pillow
    transformers
    torch
    ```

## 4. Installation

- 4.1 Repository klonen

- 4.2 Virtuelle Umgebung erstellen (optional, aber empfohlen)

- 4.3 Benötigte Pakete installieren
    - Starte das Setup welches alle Abhängigkeiten installiert um das Tool zu starten.

- 4.4 Tesseract OCR installieren

## 5. Nutzung

Das Skript kann nach dem ersten mal ausführen immer mit folgendem befehl ausgeführt werden:

```
python app.py
```

oder mit 

```
python3 app.py
```

- Das extrahierte Markdown wird in **"/Documents/PDF-Markdown_Output"** gespeichert und erhält denselben Namen wie die Eingabe-PDF, jedoch mit der Endung .md.

## Hinweis
Die Abhängigkeiten werden installiert um das Tool starten zu können, jedoch wird ein Model beim ersten mal Konvertieren einer datei, im hintergrund heruntergeladen und verwendet, wodurch die Wartezeit bis zum ersten umgewandelten Dokument etwas länger dauern kann **(ca. 2-5 min)**.

- **Bei längeren Wartezeiten, beenden und das Tool nochmals starten!**

## 6. Leistung und Genauigkeit

*   **Genauigkeit:** Hohe Präzision bei der Bewahrung der Dokumentstruktur. Gut geeignet für Texte, Tabellen, Bilder, Links und Codeblöcke. Sehr komplexe Layouts können eine manuelle Nachbearbeitung erfordern.
    
*   **Geschwindigkeit:** Die Verarbeitungszeit hängt von der PDF-Größe und -Komplexität ab. 
    - Ein 10-seitiges PDF mit gemischten Inhalten benötigt in der Regel 10-30 Sekunden.
    - Ein 30-seitiges **(oder mehr)** PDF mit gemischten Inhalten benötigt in der Regel 30-120 Sekunden.
    
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