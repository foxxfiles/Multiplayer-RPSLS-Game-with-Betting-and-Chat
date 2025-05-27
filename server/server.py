import os
import json
import hashlib
import uuid
import datetime
import random

# Generación de certificados SSL con cryptography
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa

# Servidor Flask-SocketIO con eventlet y SSL
import eventlet
import eventlet.wsgi
import eventlet.green.ssl as ssl
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

############################################################
# 1. Generación de certificados SSL
############################################################

def check_or_create_certs(cert_file='cert.pem', key_file='key.pem'):
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("Certificados no encontrados, generando certificados autofirmados...")
        create_self_signed_cert(cert_file, key_file)

def create_self_signed_cert(cert_file, key_file):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Madrid"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Madrid"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MiEmpresa"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())
    with open(key_file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

############################################################
# 2. Manejo de usuarios, créditos y estadísticas
############################################################

USER_DB = 'usuarios.json'

def load_users():
    if not os.path.exists(USER_DB):
        data = {"usuarios": [], "next_id": 1}
        with open(USER_DB, 'w') as f:
            json.dump(data, f)
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USER_DB, 'w') as f:
        json.dump(data, f, indent=4)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def register_user(username, password):
    data = load_users()
    for user in data['usuarios']:
        if user['username'] == username:
            return False, "Usuario ya existe."
    salt = uuid.uuid4().hex
    password_hash = hash_password(password, salt)
    new_user = {
        "id": data['next_id'],
        "username": username,
        "password_hash": password_hash,
        "salt": salt,
        "creditos": 1000,  # Créditos iniciales
        "partidas_jugadas": 0,
        "partidas_ganadas": 0
    }
    data['usuarios'].append(new_user)
    data['next_id'] += 1
    save_users(data)
    return True, "Registro exitoso."

def login_user(username, password):
    data = load_users()
    for user in data['usuarios']:
        if user['username'] == username:
            # Si no tiene campo creditos, lo asignamos
            if user.get('creditos') is None:
                user['creditos'] = 1000
                save_users(data)
            salt = user['salt']
            if user['password_hash'] == hash_password(password, salt):
                return True, user
    return False, None

def get_user_credits(username):
    data = load_users()
    for user in data['usuarios']:
        if user['username'] == username:
            return user.get('creditos', 0)
    return 0

def update_stats(winner_username, loser_username, bet):
    data = load_users()
    for user in data['usuarios']:
        if user['username'] == winner_username:
            user['partidas_jugadas'] += 1
            user['partidas_ganadas'] += 1
            user['creditos'] += bet
        elif user['username'] == loser_username:
            user['partidas_jugadas'] += 1
            user['creditos'] -= bet
    save_users(data)

def update_stats_tie(username1, username2):
    data = load_users()
    for user in data['usuarios']:
        if user['username'] in [username1, username2]:
            user['partidas_jugadas'] += 1
    save_users(data)

############################################################
# 3. Lógica del juego (Piedra, Papel, Tijera, Lagarto, Spock)
############################################################

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return 0
    wins = {
        'tijera': ['papel', 'lagarto'],
        'papel': ['piedra', 'spock'],
        'piedra': ['lagarto', 'tijera'],
        'lagarto': ['spock', 'papel'],
        'spock': ['tijera', 'piedra']
    }
    return 1 if choice2 in wins.get(choice1, []) else 2

############################################################
# 4. Servidor Flask-SocketIO con dinámica de apuestas y chat
############################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

waiting_players = {}  # SID -> username
games = {}            # room -> dict con estado
connected_sids = set()
user_to_sid = {}      # username -> sid para encontrar fácilmente el sid de un usuario

@socketio.on('connect')
def on_connect():
    sid = request.sid
    connected_sids.add(sid)
    print(f"[SERVER] Cliente conectado con SID: {sid}")

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    # Eliminar el mapeo de username a sid
    usernames_to_remove = []
    for username, user_sid in user_to_sid.items():
        if user_sid == sid:
            usernames_to_remove.append(username)
    
    for username in usernames_to_remove:
        user_to_sid.pop(username, None)
        
    if sid in waiting_players:
        waiting_players.pop(sid, None)
    if sid in connected_sids:
        connected_sids.remove(sid)
    print(f"[SERVER] Cliente desconectado con SID: {sid}")

@socketio.on('register')
def handle_register(data):
    username = data.get('username')
    password = data.get('password')
    success, msg = register_user(username, password)
    if success:
        emit('register_success', {'message': msg})
    else:
        emit('register_error', {'message': msg})

@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    password = data.get('password')
    success, user = login_user(username, password)
    if success:
        user_to_sid[username] = request.sid  # Registrar el sid del usuario
        emit('login_success', user)
    else:
        emit('login_error', {'message': 'Credenciales inválidas'})

@socketio.on('find_match')
def handle_find_match(data):
    username = data.get('username')
    sid = request.sid
    if sid in connected_sids:
        waiting_players[sid] = username
    else:
        print(f"[SERVER] SID {sid} no está en conexiones activas.")
        return

    if len(waiting_players) >= 2:
        players = list(waiting_players.keys())[:2]
        if all(s in connected_sids for s in players):
            room = f"room_{players[0]}_{players[1]}"
            for s in players:
                join_room(room, sid=s)
            # Seleccionar aleatoriamente a un iniciador
            initiator_sid = random.choice(players)
            responder_sid = players[0] if players[0] != initiator_sid else players[1]
            initiator_username = waiting_players.get(initiator_sid, "Desconocido")
            responder_username = waiting_players.get(responder_sid, "Desconocido")
            # Eliminar de la lista de espera
            waiting_players.pop(players[0], None)
            waiting_players.pop(players[1], None)
            # Guardar estado de la partida
            games[room] = {
                'initiator': initiator_sid,
                'initiator_username': initiator_username,
                'responder': responder_sid,
                'responder_username': responder_username,
                'bet': None,
                'choices': {},
                'player_sets': {},  # Para almacenar qué set está usando cada jugador
                'chat_history': []  # Nueva lista para el historial de chat
            }
            # Notificar a ambos que se halló oponente
            emit('match_found', {
                'room': room,
                'opponent': responder_username if sid == initiator_sid else initiator_username
            }, room=room)
            # Solo el iniciador recibe bet_request
            emit('bet_request', {'message': 'Propon tu apuesta'}, room=initiator_sid)
        else:
            for s in players:
                if s not in connected_sids:
                    waiting_players.pop(s, None)
            print("[SERVER] Uno de los jugadores en espera ya no está conectado.")

@socketio.on('set_bet')
def handle_set_bet(data):
    room = data.get('room')
    username = data.get('username')
    bet = data.get('bet')
    print(f"[DEBUG] set_bet recibido de {username} con apuesta={bet} en room={room}")
    if room in games:
        # Solo el iniciador puede proponer la apuesta
        if request.sid == games[room].get('initiator'):
            initiator_credits = get_user_credits(username)
            responder_username = games[room].get('responder_username')
            responder_credits = get_user_credits(responder_username)
            if bet > initiator_credits or bet > responder_credits:
                emit('bet_error', {
                    'message': f"Apuesta demasiado alta. Tus créditos: {initiator_credits}, Oponente: {responder_credits}"
                }, room=request.sid)
                return
            games[room]['bet'] = bet
            responder_sid = games[room].get('responder')
            emit('bet_proposal', {
                'bet': bet,
                'message': f"El jugador {username} propone apostar {bet} créditos. ¿Aceptas?"
            }, room=responder_sid)
        else:
            print(f"[DEBUG] set_bet ignorado, {username} no es el iniciador en room={room}")

@socketio.on('accept_bet')
def handle_accept_bet(data):
    room = data.get('room')
    username = data.get('username')
    if room in games:
        bet = games[room].get('bet', 0)
        print(f"[DEBUG] Apuesta aceptada en room={room}, bet={bet}")
        emit('bet_confirmed', {
            'bet': bet,
            'message': f"Apuesta confirmada: {bet} créditos."
        }, room=room)

@socketio.on('decline_bet')
def handle_decline_bet(data):
    room = data.get('room')
    username = data.get('username')
    print(f"[DEBUG] Apuesta rechazada por {username} en room={room}")
    emit('bet_declined', {
        'message': f"El jugador {username} ha declinado la apuesta."
    }, room=room)
    if room in games:
        games.pop(room, None)

@socketio.on('make_choice')
def handle_make_choice(data):
    room = data.get('room')
    choice = data.get('choice')
    username = data.get('username')
    asset_set = data.get('asset_set')  # Set que está usando el jugador
    
    if room in games:
        games[room]['choices'][username] = choice
        # Guardar el set que está usando cada jugador
        games[room]['player_sets'][username] = asset_set
        
        if len(games[room]['choices']) == 2:
            players = list(games[room]['choices'].keys())
            c1 = games[room]['choices'][players[0]]
            c2 = games[room]['choices'][players[1]]
            result = determine_winner(c1, c2)
            bet = games[room].get('bet', 0)
            
            if result == 0:
                result_text = "Empate"
                update_stats_tie(players[0], players[1])
            elif result == 1:
                result_text = f"Ganador: {players[0]}"
                update_stats(players[0], players[1], bet)
            else:
                result_text = f"Ganador: {players[1]}"
                update_stats(players[1], players[0], bet)
                
            # Obtener créditos actualizados de cada jugador
            user_credits = {}
            for p in players:
                user_credits[p] = get_user_credits(p)
                
            # Incluir la información sobre los sets de cada jugador en la respuesta
            emit('game_result', {
                'result': result_text,
                'choices': games[room]['choices'],
                'bet': bet,
                'credits': user_credits,
                'player_sets': games[room]['player_sets']  # Enviar qué set está usando cada jugador
            }, room=room)
            
            # Se mantienen los datos de la sala para posible "play_again"
            # pero se limpian las choices y bet
            games[room]['choices'] = {}
            games[room]['bet'] = None
            # Mantener los player_sets para la próxima ronda

@socketio.on('play_again')
def handle_play_again(data):
    """Se prepara otra ronda en la misma sala, mismo iniciador."""
    room = data.get('room')
    username = data.get('username')
    if room in games:
        # El iniciador vuelve a proponer apuesta
        initiator_sid = games[room].get('initiator')
        emit('bet_request', {'message': 'Propon tu apuesta para la siguiente ronda'}, room=initiator_sid)

@socketio.on('abandon')
def handle_abandon(data):
    room = data.get('room')
    username = data.get('username')
    emit('abandon_confirm', {
        'message': f'El jugador {username} ha abandonado la partida.'
    }, room=room)
    if room in games:
        games.pop(room, None)
    print(f"[SERVER] El jugador {username} abandonó la sala {room}")

# Nuevas funciones para el sistema de chat
@socketio.on('send_chat')
def handle_chat_message(data):
    """Maneja mensajes de chat entre jugadores."""
    room = data.get('room')
    username = data.get('username')
    message = data.get('message')
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    if room in games and message:
        chat_entry = {
            'username': username,
            'message': message,
            'timestamp': timestamp
        }
        # Almacenar el mensaje en el historial
        games[room]['chat_history'].append(chat_entry)
        
        # Enviar el mensaje a todos en la sala
        emit('chat_message', chat_entry, room=room)
        print(f"[CHAT] {username} en sala {room}: {message}")

@socketio.on('get_chat_history')
def handle_get_chat_history(data):
    """Envía el historial de chat al cliente que lo solicita."""
    room = data.get('room')
    if room in games:
        emit('chat_history', {
            'history': games[room]['chat_history']
        })

@socketio.on('update_credits')
def handle_update_credits(data):
    """Envía los créditos actualizados al cliente que lo solicita."""
    username = data.get('username')
    credits = get_user_credits(username)
    emit('credits_updated', {'credits': credits})

if __name__ == '__main__':
    check_or_create_certs()
    listener = eventlet.listen(('0.0.0.0', 5000))
    ssl_sock = ssl.wrap_socket(listener, certfile='cert.pem', keyfile='key.pem', server_side=True)
    print("(SERVER) Iniciando en https://0.0.0.0:5000")
    eventlet.wsgi.server(ssl_sock, app)