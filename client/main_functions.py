import os
import json
import random
from PIL import Image, ImageTk
import socketio

# Configuración de SocketIO para el cliente
sio = socketio.Client(ssl_verify=False)

def connect_to_server(url):
    """Establece conexión con el servidor Socket.IO."""
    sio.connect(url, transports=['websocket'])

def login(username, password):
    """Envía solicitud de login al servidor."""
    sio.emit('login', {'username': username, 'password': password})

def register(username, password):
    """Envía solicitud de registro al servidor."""
    sio.emit('register', {'username': username, 'password': password})

def find_match(username):
    """Solicita buscar una partida al servidor."""
    sio.emit('find_match', {'username': username})

def set_bet(room, username, bet):
    """Envía una propuesta de apuesta al servidor."""
    sio.emit('set_bet', {'room': room, 'username': username, 'bet': bet})

def accept_bet(room, username):
    """Acepta una apuesta propuesta."""
    sio.emit('accept_bet', {'room': room, 'username': username})

def decline_bet(room, username):
    """Rechaza una apuesta propuesta."""
    sio.emit('decline_bet', {'room': room, 'username': username})

def make_choice(room, username, choice, asset_set):
    """Envía la elección del jugador al servidor junto con el set de assets usado."""
    sio.emit('make_choice', {'room': room, 'username': username, 'choice': choice, 'asset_set': asset_set})

def play_again(room, username):
    """Solicita jugar otra partida en la misma sala."""
    sio.emit('play_again', {'room': room, 'username': username})

def abandon(room, username):
    """Abandona la partida actual."""
    sio.emit('abandon', {'room': room, 'username': username})

def update_credits(username):
    """Solicita una actualización de los créditos del usuario."""
    sio.emit('update_credits', {'username': username})

def get_asset_sets(config_file="assets_config.json"):
    """
    Retorna una lista de nombres de conjuntos definidos en el archivo de configuración.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, config_file)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return list(config.get("sets", {}).keys())
    except Exception as e:
        print(f"Error leyendo {config_path}: {e}")
        return []

def load_assets(asset_set="set1", assets_folder="assets", config_file="assets_config.json", size=(120,128)):
    """
    Lee el archivo de configuración y carga las imágenes del conjunto de assets indicado.
    Redimensiona cada imagen al tamaño especificado (por defecto 120x128).
    Utiliza rutas absolutas basadas en la ubicación del script.
    Imprime en consola el nombre de archivo esperado para cada opción.
    Retorna un diccionario con objetos PhotoImage para cada opción.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, config_file)
    if not os.path.exists(config_path):
        print(f"Archivo de configuración {config_path} no encontrado.")
        return {}
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error leyendo {config_path}: {e}")
        return {}
    
    images = {}
    set_config = config.get("sets", {}).get(asset_set, {})
    assets_path = os.path.join(base_path, assets_folder)
    for option, data in set_config.items():
        image_filename = data.get("imagen")
        print(f"Opción '{option}': se espera imagen '{image_filename}'")
        image_path = os.path.join(assets_path, image_filename)
        if os.path.exists(image_path):
            try:
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
                images[option] = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print(f"Error cargando la imagen {image_path}: {e}")
                images[option] = None
        else:
            print(f"Imagen {image_path} no encontrada.")
            images[option] = None
    return images

def load_all_assets(assets_folder="assets", config_file="assets_config.json", size=(120,128)):
    """
    Carga todos los conjuntos de assets definidos en el archivo de configuración.
    Retorna un diccionario donde la clave es el nombre del set y el valor es el diccionario de imágenes.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, config_file)
    all_assets = {}
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        sets = config.get("sets", {})
        for set_name in sets.keys():
            all_assets[set_name] = load_assets(set_name, assets_folder, config_file, size)
    except Exception as e:
        print(f"Error cargando todos los assets: {e}")
    return all_assets

def get_image_filename(asset_set, choice, config_file="assets_config.json"):
    """
    Retorna el nombre de archivo de imagen para un set y opción específicos.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, config_file)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get("sets", {}).get(asset_set, {}).get(choice, {}).get("imagen", "")
    except Exception as e:
        print(f"Error leyendo {config_path}: {e}")
        return ""

# Funciones para el sistema de chat
def send_chat_message(room, username, message):
    """Envía un mensaje de chat al servidor."""
    if message and message.strip():  # Solo enviar si el mensaje no está vacío
        sio.emit('send_chat', {
            'room': room,
            'username': username,
            'message': message.strip()
        })

def get_chat_history(room):
    """Solicita el historial de chat al servidor."""
    sio.emit('get_chat_history', {'room': room})