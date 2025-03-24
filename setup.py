#!/usr/bin/env python
import os
import sys
import subprocess
import builtins
import contextlib
import io
import traceback

# ---------------------------
# Hilfsfunktion: Konsolenausgabe unterdrücken
# ---------------------------
@contextlib.contextmanager
def suppress_stdout():
    """Unterdrückt temporär die Standardausgabe."""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# ---------------------------
# Hilfsfunktion: Paketinstallation
# ---------------------------
def install_package(package):
    """Versucht ein Paket über mehrere Wege zu installieren."""
    commands = [
        [sys.executable, "-m", "pip", "install", package],
        ["pip", "install", package],
        ["pip3", "install", package]
    ]
    
    for cmd in commands:
        try:
            # Ausgabe der Installation unterdrücken
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                if "Requirement already satisfied" in result.stdout:
                    print(f"Paket {package} ist bereits installiert.")
                else:
                    print(f"Paket {package} wurde erfolgreich installiert.")
                return True
        except Exception:
            continue
    
    print(f"Fehler: {package} konnte nicht installiert werden.")
    return False

# ---------------------------
# Funktion: Installation aller Pakete aus requirements.txt
# ---------------------------
def install_requirements():
    """Liest requirements.txt, prüft die Existenz jedes Pakets und installiert es ggf."""
    if not os.path.exists("requirements.txt"):
        print("Fehler: requirements.txt wurde nicht gefunden.")
        sys.exit(1)
    
    with open("requirements.txt", "r") as req_file:
        lines = req_file.readlines()
    
    # Filtere leere Zeilen und Kommentare
    packages = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    
    print(f"Prüfe {len(packages)} Pakete aus requirements.txt...")
    
    for package in packages:
        # Extrahiere den Paketnamen (bei Versionsangaben z. B. "numpy==1.21.0")
        pkg_name = package.split("==")[0].strip()
        try:
            # Versuche Import ohne Ausgabe
            with suppress_stdout():
                __import__(pkg_name)
            print(f"{pkg_name} ist bereits installiert.")
        except ImportError:
            print(f"{pkg_name} wird installiert...")
            if not install_package(package):
                print(f"Fehler: {package} konnte nicht installiert werden.")

# ---------------------------
# Custom Import-Hook: Installiert fehlende Module während der Laufzeit
# ---------------------------
real_import = builtins.__import__

def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Erweiterte __import__, die bei einem ImportError automatisch versucht, das Modul zu installieren."""
    try:
        return real_import(name, globals, locals, fromlist, level)
    except ImportError:
        # Prüfe, ob es sich um ein Windows-spezifisches Modul handelt
        windows_modules = ['_winapi', 'msvcrt', 'nt']
        if name in windows_modules and sys.platform != 'win32':
            print(f"Modul '{name}' ist nur unter Windows verfügbar und wird übersprungen.")
            raise
        
        # Falls es sich um ein Untermodul handelt, versuche das Hauptmodul zu installieren
        if '.' in name:
            main_module = name.split('.')[0]
            package_name = main_module
        else:
            package_name = name
        
        # Bekannte Mappings (z. B. "fitz" wird zu "PyMuPDF")
        known_mappings = {
            "fitz": "PyMuPDF",
            # Weitere Mappings hier hinzufügen, falls nötig
        }
        
        package_name = known_mappings.get(package_name, package_name)
        print(f"Modul '{name}' nicht gefunden. Versuche, '{package_name}' zu installieren...")
        
        if install_package(package_name):
            return real_import(name, globals, locals, fromlist, level)
        else:
            print(f"Automatische Installation von '{package_name}' fehlgeschlagen.")
            raise

# Überschreibe die eingebaute __import__ Funktion
builtins.__import__ = custom_import

# ---------------------------
# Main-Bereich: Installation und Start der Anwendung
# ---------------------------
if __name__ == "__main__":
    print("Installiere alle Pakete aus requirements.txt...")
    install_requirements()
    print("Alle Abhängigkeiten wurden überprüft.")
    
    # Hier können weitere systembezogene Schritte ergänzt werden.
    # Beispiel: Systempakete (Ubuntu) installieren, falls notwendig:
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "libxcb-xinerama0"], check=True)
            print("Systempaket libxcb-xinerama0 wurde installiert oder ist bereits vorhanden.")
        except Exception as e:
            print(f"Warnung: Konnte libxcb-xinerama0 nicht installieren: {e}")
    
    # Starte die Hauptanwendung
    # Hier wird angenommen, dass dein Hauptmodul "main.py" mit einer main()-Funktion vorhanden ist.
    try:
        from main import main
        main()
    except ImportError:
        print("Hauptmodul 'main' konnte nicht importiert werden.")
    except Exception as e:
        print(f"Fehler beim Starten der Hauptanwendung: {e}")
        traceback.print_exc()
