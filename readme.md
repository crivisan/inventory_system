# Land-Lieben Inventar System

Eine leichte, lokal ausführbare Desktop-Anwendung zur Verwaltung projektbezogener Anschaffungen im Rahmen von **Land-Lieben / Smart City Kusel**.

## 🖥️ Übersicht
Das Inventar-System ermöglicht Teammitgliedern:
- Produkte, Lieferanten und Kosten zu erfassen und zu verwalten  
- Barcode-Etiketten zu generieren und zu drucken  
- Barcodes mit einem Scanner zu lesen  
- Inventardaten nach CSV zu exportieren  
- Alle Einträge in einer Tabellenansicht anzuzeigen und zu bearbeiten  

Das Tool wurde mit **Python (PyQt6)** entwickelt und verwendet eine lokale **SQLite-Datenbank** (`data/inventory.db`).

## ⚙️ Installation (Windows)

1. **Repository klonen oder herunterladen**  
   ```bash
   git clone https://github.com/crivisan/inventory_system
   cd inventory_system


2. Virtuelle Umgebung erstellen und Abhängigkeiten installieren

    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Anwendung starten

    ```bash
    python main.py
    ```

## 💾 Datenhaltung

Alle Daten werden standardmäßig lokal gespeichert unter:

`data/inventory.db`


Falls mehrere Nutzer gleichzeitig mit demselben Inventar arbeiten sollen, kann diese Datei auf ein gemeinsames Netzlaufwerk verschoben werden.
(Bei parallelem Zugriff empfiehlt sich zukünftig eine zentrale PostgreSQL-Datenbank.)

## 🧠 Zukünftige Erweiterungen

- Mehrbenutzer-Unterstützung (PostgreSQL / zentraler Server)
- Berichte und Auswertungen (z. B. Ausgaben pro Gemeinde)
- Automatische Versionsaktualisierung
- Erweiterte Such- und Filterfunktionen


---
---
© 2025 – Land-Lieben / Landkreis Kusel – Smart City Projekt

