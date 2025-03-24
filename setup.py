#!/usr/bin/env python
import os
import sys
import subprocess
import builtins
import contextlib
import logging
import traceback

# ---------------------------
# Logging konfigurieren
# ---------------------------
logging.basicConfig(
    filename="installer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log(msg):
    print(msg)
    logging.info(msg)

# ---------------------------
# Hilfsfunktion: Konsolenausgabe unterdrücken
# ---------------------------
@contextlib.contextmanager
def suppress_stdout():
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
    commands = [[sys.executable, "-m", "pip", "install", package]]
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                log(f"Paket {package} wurde erfolgreich installiert.")
                return True
        except Exception as e:
            logging.error(f"Fehler bei der Installation von {package}: {e}")
    log(f"Fehler: {package} konnte nicht installiert werden.")
    return False

# ---------------------------
# Funktion: Installation aller Pakete aus requirements.txt
# ---------------------------
def install_requirements():
    if not os.path.exists("requirements.txt"):
        log("Fehler: requirements.txt wurde nicht gefunden.")
        sys.exit(1)
    
    with open("requirements.txt", "r") as req_file:
        packages = [line.strip() for line in req_file if line.strip() and not line.startswith("#")]
    
    log(f"Prüfe {len(packages)} Pakete aus requirements.txt...")
    
    for package in packages:
        pkg_name = package.split("==")[0].strip()
        try:
            with suppress_stdout():
                __import__(pkg_name)
            log(f"{pkg_name} ist bereits installiert.")
        except ImportError:
            log(f"{pkg_name} wird installiert...")
            install_package(package)

# ---------------------------
# Custom Import-Hook
# ---------------------------
real_import = builtins.__import__
imported_packages = set()

def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in imported_packages:
        return real_import(name, globals, locals, fromlist, level)
    
    try:
        module = real_import(name, globals, locals, fromlist, level)
        imported_packages.add(name)
        return module
    except ImportError:
        log(f"Modul '{name}' nicht gefunden. Versuche, es zu installieren...")
        if install_package(name):
            return real_import(name, globals, locals, fromlist, level)
        log(f"Installation von '{name}' fehlgeschlagen.")
        raise

builtins.__import__ = custom_import

# ---------------------------
# Main-Bereich
# ---------------------------
if __name__ == "__main__":
    log("Installiere alle Pakete aus requirements.txt...")
    install_requirements()
    log("Alle Abhängigkeiten wurden überprüft.")
    
    if sys.platform.startswith("linux"):
        if os.geteuid() != 0:
            log("Warnung: Systempakete erfordern Root-Rechte.")
        else:
            try:
                subprocess.run(["apt-get", "update"], check=True)
                subprocess.run(["apt-get", "install", "-y", "libxcb-xinerama0"], check=True)
                log("Systempaket libxcb-xinerama0 installiert.")
            except Exception as e:
                log(f"Fehler bei der Installation von Systempaketen: {e}")
    
    try:
        from main import main
        main()
    except ImportError:
        log("Hauptmodul 'main' konnte nicht importiert werden.")
    except Exception as e:
        log(f"Fehler beim Starten der Anwendung: {e}")
        traceback.print_exc()
