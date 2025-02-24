import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

USERS = {
    "deine email": {
        "password": generate_password_hash("dein password!")
    }
}

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

# Windows-Dienstnamen der Bots
BOTS = {
    "Bot1 Name": "Bot1 Dienst Name",
    "Bot2 Name": "Bot2 Dienst Name"
}

def check_bot_status(service_name):
    """ Überprüft den Status eines Windows-Dienstes """
    try:
        result = subprocess.run(["sc", "query", service_name], capture_output=True, text=True)
        return "RUNNING" in result.stdout  # True, wenn der Dienst läuft
    except Exception as e:
        print(f"Fehler beim Abrufen des Status für {service_name}: {e}")
        return False

@app.route('/')
@login_required
def index():
    bot_status = {bot: check_bot_status(service) for bot, service in BOTS.items()}
    return render_template('index.html', bots=bot_status)

@app.route('/status')
@login_required
def bot_status():
    """ Gibt den aktuellen Status aller Bots zurück (für Live-Updates) """
    status = {bot: {"running": check_bot_status(service)} for bot, service in BOTS.items()}
    return jsonify(status)

@app.route('/start/<bot_name>', methods=['POST'])
@login_required
def start_bot(bot_name):
    if bot_name in BOTS:
        subprocess.run(["sc", "start", BOTS[bot_name]], capture_output=True, text=True)
        return jsonify({"status": f"{bot_name} gestartet"})
    return jsonify({"status": "Bot nicht gefunden"}), 404

@app.route('/stop/<bot_name>', methods=['POST'])
@login_required
def stop_bot(bot_name):
    if bot_name in BOTS:
        subprocess.run(["sc", "stop", BOTS[bot_name]], capture_output=True, text=True)
        return jsonify({"status": f"{bot_name} gestoppt"})
    return jsonify({"status": "Bot nicht gefunden"}), 404

@app.route('/restart/<bot_name>', methods=['POST'])
@login_required
def restart_bot(bot_name):
    """ Stoppt und startet den Bot neu """
    if bot_name in BOTS:
        service_name = BOTS[bot_name]
        subprocess.run(["sc", "stop", service_name], capture_output=True, text=True)
        subprocess.run(["sc", "start", service_name], capture_output=True, text=True)
        return jsonify({"status": f"{bot_name} neu gestartet"})
    return jsonify({"status": "Bot nicht gefunden"}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in USERS and check_password_hash(USERS[email]['password'], password):
            user = User(email)
            login_user(user)
            return redirect(url_for('index'))
        return "Falsche Anmeldedaten!"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
