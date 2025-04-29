from flask import Flask, request, jsonify
import json, os
import bcrypt

app = Flask(__name__)
DATA_FILE = 'data/users.json'

# Hilfsfunktion: Lade Benutzerdaten
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Hilfsfunktion: Speichere Benutzerdaten
def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username').lower()
    password = data.get('password')

    print(f"🔐 Registrierung angefragt: {username}")

    users = load_users()

    if username in users:
        print(f"❌ Benutzer '{username}' existiert bereits!")
        return jsonify({'status': 'error', 'message': 'Benutzer existiert bereits!'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = {"password": hashed.decode('utf-8'), "points": 1000}
    save_users(users)

    print(f"✅ Benutzer '{username}' erfolgreich registriert.")

    return jsonify({'status': 'success', 'message': 'Registrierung erfolgreich!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username').lower()
    password = data.get('password')

    print(f"🔑 Login-Versuch: {username}")

    users = load_users()

    if username not in users:
        print(f"❌ Benutzer '{username}' nicht gefunden.")
        return jsonify({'status': 'error', 'message': 'Benutzer nicht gefunden!'}), 404

    hashed = users[username]['password'].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), hashed):
        print(f"✅ Login erfolgreich für Benutzer: {username}")
        return jsonify({'status': 'success', 'points': users[username]['points']})
    else:
        print(f"❌ Falsches Passwort für Benutzer: {username}")
        return jsonify({'status': 'error', 'message': 'Falsches Passwort!'}), 401

@app.route('/update_points', methods=['POST'])
def update_points():
    data = request.get_json()
    username = data.get('username').lower()
    points = data.get('points')

    print(f"🔄 Punkte-Update angefragt für '{username}' auf {points} Punkte.")

    users = load_users()

    if username not in users:
        print(f"❌ Benutzer '{username}' nicht gefunden beim Punkte-Update.")
        return jsonify({'status': 'error', 'message': 'Benutzer nicht gefunden!'}), 404

    users[username]['points'] = points
    save_users(users)

    print(f"✅ Punkte erfolgreich aktualisiert für '{username}'.")

    return jsonify({'status': 'success', 'message': 'Punkte aktualisiert'})

@app.route('/get_users', methods=['GET'])
def get_users():
    print("👀 Benutzerliste wurde abgerufen.")
    users = load_users()
    return jsonify({'users': users})

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    print("🚀 Server startet auf Port 5000...")
    app.run(host='0.0.0.0', port=5000)
