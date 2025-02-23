# Nexus Gaming Bot Interface

Ein einfaches Web-Dashboard zur Verwaltung von Discord-Bots, die als Windows-Dienste mit NSSM laufen.

## Voraussetzungen

### 1. Installiere Python
Lade [Python 3.11+](https://www.python.org/downloads/) herunter und installiere es. Stelle sicher, dass die Option **"Add Python to PATH"** während der Installation aktiviert ist.

### 2. Installiere Flask und weitere Abhängigkeiten
Öffne eine **Eingabeaufforderung (cmd)** und installiere die benötigten Python-Pakete:
```bash
pip install flask flask-login werkzeug
```

### 3. Installiere NSSM
NSSM (Non-Sucking Service Manager) wird benötigt, um die Bots als Windows-Dienste zu verwalten. 
- Lade NSSM von [https://nssm.cc/download](https://nssm.cc/download) herunter
- Entpacke es nach `C:\nssm`
- Füge den Pfad `C:\nssm` zur Windows-Umgebungsvariable `PATH` hinzu (Systemsteuerung → System → Erweiterte Systemeinstellungen → Umgebungsvariablen)

## Einrichtung

### 1. Bots als Windows-Dienste hinzufügen
Ersetze `BOT1` mit dem Namen deines Bots und `C:\Pfad\zum\bot.py` mit dem tatsächlichen Pfad:
```bash
nssm install BOT1 "C:\Pfad\zu\python.exe" "C:\Pfad\zum\bot.py"
```
Starte den Dienst mit:
```bash
sc start BOT1
```
Stoppe den Dienst mit:
```bash
sc stop BOT1
```

### 2. `dashboard.py` anpassen
Bearbeite die Datei `dashboard.py` und passe die **Windows-Dienstnamen** in der Variable `BOTS` an:
```python
BOTS = {
    "Bot1": "NSSM_Bot1",
    "Bot2": "NSSM_Bot2"
}
```

## Start des Dashboards
Starte das Web-Interface mit:
```bash
python dashboard.py
```
Dann öffne [http://localhost:5000](http://localhost:5000) in deinem Browser.

## Funktionen
✅ **Anzeigen des Bot-Status** (Läuft/Gestoppt)  
✅ **Starten und Stoppen von Bots**  
✅ **Neustarten von Bots**  
✅ **Login mit Benutzername und Passwort**  

## Login-Daten ändern
Standardmäßig ist der Benutzer in `dashboard.py` definiert:
```python
USERS = {
    "admin@example.com": {
        "password": generate_password_hash("passwort123")
    }
}
```
Ändere `admin@example.com` und das Passwort nach deinen Wünschen.

## FAQ
**1. Mein Bot wird als gestoppt angezeigt, obwohl er läuft.**  
→ Stelle sicher, dass der Dienstname in `dashboard.py` korrekt ist.

**2. Ich bekomme eine Fehlermeldung `TemplateNotFound: index.html`.**  
→ Stelle sicher, dass sich `index.html` im Ordner `templates/` befindet.

**3. Wie entferne ich einen Bot-Dienst?**  
```bash
nssm remove BOT1 confirm
```

**4. Wie kann ich das Dashboard auf einem Server hosten?**  
Starte Flask so, dass es von anderen PCs im Netzwerk erreichbar ist:
```bash
python dashboard.py --host=0.0.0.0 --port=5000
```

## Lizenz
MIT-Lizenz – Verwende es frei für deine Projekte!
 
