import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import random  # Para la selección aleatoria de set de imágenes
import json
import os

# Importar las funciones auxiliares
from main_functions import (
    sio, connect_to_server, login, register, find_match, set_bet,
    accept_bet, decline_bet, make_choice, play_again, abandon,
    get_asset_sets, load_assets, load_all_assets, get_image_filename,
    update_credits
)

# Importar los componentes de chat
from chat_components import ChatFrame, UserInfoBar

# Importar componentes de UI
from ui_components import (
    LoginScreen, LobbyScreen, MatchSearchScreen, BetProposalScreen, 
    BetWaitScreen, BetResponseScreen, GameScreen, ChoiceWaitScreen,
    ResultScreen, AbandonScreen, create_server_config_dialog
)

# Configuración de servidor predeterminada y gestión de configuración
CONFIG_FILE = "server_config.json"

def load_server_config():
    """Carga la configuración del servidor desde un archivo JSON."""
    default_config = {"host": "localhost", "port": 5000}
    
    if not os.path.exists(CONFIG_FILE):
        # Si no existe el archivo, lo creamos con la configuración predeterminada
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except:
        # Si hay algún error, devolvemos la configuración predeterminada
        return default_config

def save_server_config(host, port):
    """Guarda la configuración del servidor en un archivo JSON."""
    config = {"host": host, "port": port}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Juego RPSLS con Apuestas")
        self.geometry("900x650")  # Aumentada la altura en 50 píxeles
        
        # Cargar configuración del servidor
        self.server_config = load_server_config()
        
        # Configurar estilos personalizados para una interfaz más elegante
        style = ttk.Style()
        
        # Estilos para botones más elegantes
        style.configure("rounded.TButton", borderwidth=0, relief="flat", font=("Segoe UI", 10))
        style.configure("rounded.success.TButton", background="#28a745", foreground="white")
        style.configure("rounded.danger.TButton", background="#dc3545", foreground="white")
        style.configure("rounded.warning.TButton", background="#ffc107", foreground="black")
        style.configure("rounded.info.TButton", background="#17a2b8", foreground="white")
        style.configure("rounded.primary.TButton", background="#007bff", foreground="white")
        
        # Estilos para marcos más elegantes
        style.configure("card.TFrame", relief="flat", borderwidth=0, background="#343a40")
        style.configure("transparent.TFrame", background="#212529")
        
        # Variables de estado
        self.username = None
        self.credits = 0    # Saldo del usuario
        self.room = None
        self.opponent = None
        self.bet_confirmed = False
        self.is_initiator = False
        self.is_connected = False
        self.images = {}    # Diccionario para almacenar imágenes del set actual
        self.all_assets = {} # Diccionario para almacenar todos los sets
        self.asset_set = None  # Set elegido para la partida
        self.button_images = []  # Para mantener referencias a las imágenes de los botones
        self.chat_frame = None  # Referencia al frame de chat
        
        # Crear marco principal con diseño fluido
        self.main_container = ttk.Frame(self, style="transparent.TFrame")
        self.main_container.pack(fill='both', expand=True)
        
        # Barra de información de usuario (siempre visible)
        self.user_info_bar = UserInfoBar(self.main_container)
        self.user_info_bar.pack(fill="x", side="top", pady=(0, 5))
        
        # Contenedor que tendrá el área de juego (arriba) y el chat (abajo)
        self.content_frame = ttk.Frame(self.main_container, style="transparent.TFrame")
        self.content_frame.pack(fill='both', expand=True)
        
        # Marco principal para el contenido del juego (arriba)
        self.main_frame = ttk.Frame(self.content_frame, style="transparent.TFrame")
        self.main_frame.pack(fill='both', expand=True, side="top")
        
        # Marco para el chat (abajo) - vacío inicialmente
        self.chat_container = ttk.Frame(self.content_frame, style="transparent.TFrame")
        # No hacemos pack todavía - será añadido después de emparejar
        
        # Barra de estado en la parte inferior (estilo sutil)
        self.status_label = ttk.Label(self, text="", anchor="center", 
                                    font=("Segoe UI", 9), foreground="#ffc107")
        self.status_label.pack(side="bottom", fill="x", pady=5)

        # Cargar todos los sets de assets
        self.all_assets = load_all_assets()
        if self.all_assets:
            print("Conjuntos cargados:", list(self.all_assets.keys()))
        else:
            print("No se pudieron cargar conjuntos de assets.")

        self.verify_assets()
        self.create_login_screen()

        # Configurar manejadores de eventos de socket.io
        sio.on('login_success', self.on_login_success)
        sio.on('login_error', self.on_login_error)
        sio.on('register_success', self.on_register_success)
        sio.on('register_error', self.on_register_error)
        sio.on('match_found', self.on_match_found)
        sio.on('bet_request', self.on_bet_request)      # Para el iniciador
        sio.on('bet_proposal', self.on_bet_proposal)    # Para el responder
        sio.on('bet_confirmed', self.on_bet_confirmed)
        sio.on('bet_declined', self.on_bet_declined)
        sio.on('game_result', self.on_game_result)
        sio.on('abandon_confirm', self.on_abandon_confirm)
        
        # Nuevos manejadores para chat y actualización de créditos
        sio.on('chat_message', self.on_chat_message)
        sio.on('chat_history', self.on_chat_history)
        sio.on('credits_updated', self.on_credits_updated)

    def verify_assets(self):
        # Verifica que al menos un conjunto se haya cargado correctamente
        if self.all_assets:
            # Tomamos el primer set para ver si faltan imágenes
            first_set = next(iter(self.all_assets.values()))
            missing = [option for option, img in first_set.items() if img is None]
            if missing:
                messagebox.showwarning("Advertencia de Assets", 
                    "Las siguientes imágenes faltan en al menos un set: " + ", ".join(missing))
        else:
            messagebox.showwarning("Advertencia de Assets", "No se encontraron conjuntos en el archivo de configuración.")

    def clear_main_frame(self):
        # Eliminar todos los widgets del main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def remove_chat(self):
        """Elimina el chat y su contenedor de la interfaz."""
        # Destruir el chat si existe
        if self.chat_frame:
            self.chat_frame.destroy()
            self.chat_frame = None
            
        # Ocultar el contenedor del chat
        self.chat_container.pack_forget()

    def update_status(self, message):
        self.status_label.config(text=message)

    def open_server_config_dialog(self):
        """Abre un diálogo para configurar el servidor."""
        def save_server_settings(host, port):
            save_server_config(host, port)
            self.server_config = {"host": host, "port": port}
            
        create_server_config_dialog(self, self.server_config, save_server_settings)

    def create_login_screen(self):
        # Eliminar chat si existe
        self.remove_chat()
        self.clear_main_frame()
        
        # Función de callback para iniciar sesión
        def handle_login_callback():
            self.handle_login()
            
        # Función de callback para registro
        def handle_register_callback():
            self.handle_register()
            
        # Crear pantalla de login con los callbacks necesarios
        login_screen = LoginScreen(
            self.main_frame,
            server_config=self.server_config,
            on_login=handle_login_callback,
            on_register=handle_register_callback,
            on_server_config=self.open_server_config_dialog
        )
        login_screen.pack(fill="both", expand=True)
        
        # Guardar referencias a los campos para poder acceder desde los manejadores
        self.entry_username = login_screen.entry_username
        self.entry_password = login_screen.entry_password
        
        # Limpiar mensaje de estado
        self.update_status("")

    def handle_connect_and_login(self):
        if not self.is_connected:
            try:
                # Usar la configuración guardada
                server_url = f"https://{self.server_config['host']}:{self.server_config['port']}"
                connect_to_server(server_url)
                self.is_connected = True
                self.update_status("Conectado al servidor.")
                # Una vez conectado, intenta hacer login automáticamente
                self.handle_login()
            except Exception as e:
                self.update_status(f"Error al conectar: {e}")
        else:
            self.handle_login()

    def handle_connect(self):
        try:
            # Usar la configuración guardada
            server_url = f"https://{self.server_config['host']}:{self.server_config['port']}"
            connect_to_server(server_url)
            self.is_connected = True
            self.update_status("Conectado al servidor.")
        except Exception as e:
            self.update_status(f"Error al conectar: {e}")

    def handle_login(self):
        if not self.is_connected:
            self.handle_connect()
            if not self.is_connected:
                return
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.username = username
        login(username, password)

    def handle_register(self):
        if not self.is_connected:
            self.handle_connect()
            if not self.is_connected:
                return
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.username = username
        register(username, password)

    def on_login_success(self, data):
        self.update_status("Inicio de sesión exitoso")
        self.credits = data.get('creditos', 0)
        # Actualizar barra de información de usuario
        self.user_info_bar.update_username(self.username)
        self.user_info_bar.update_credits(self.credits)
        self.create_lobby()

    def on_login_error(self, data):
        self.update_status(data.get('message', 'Error al iniciar sesión'))

    def on_register_success(self, data):
        self.update_status("Registro exitoso, inicie sesión")

    def on_register_error(self, data):
        self.update_status(data.get('message', 'Error en el registro'))

    def create_lobby(self):
        # Eliminar chat si existe
        self.remove_chat()
        self.clear_main_frame()
        
        # Crear componente de lobby con callback para búsqueda
        lobby_screen = LobbyScreen(
            self.main_frame,
            username=self.username,
            credits=self.credits,
            on_search_match=self.search_match
        )
        lobby_screen.pack(fill="both", expand=True)
        
        self.update_status("")

    def search_match(self):
        if not self.is_connected:
            self.update_status("Primero conecte al servidor.")
            return
        find_match(self.username)
        self.clear_main_frame()
        
        # Crear pantalla de búsqueda
        search_screen = MatchSearchScreen(self.main_frame)
        search_screen.pack(fill="both", expand=True)
        
        self.update_status("Conectando con el servidor de emparejamiento...")
        
    def create_chat(self):
        """Crea el componente de chat y lo añade a la interfaz."""
        # Limpiar cualquier chat existente
        if self.chat_frame:
            self.chat_frame.destroy()
            
        # Crear nuevo chat
        self.chat_frame = ChatFrame(self.chat_container, self.room, self.username, max_height=150)
        self.chat_frame.pack(fill="x", expand=True)
        
        # Mostrar el contenedor de chat si no está visible
        if not self.chat_container.winfo_ismapped():
            self.chat_container.pack(fill="x", side="bottom", padx=10, pady=5)

    def on_match_found(self, data):
        self.room = data.get('room')
        self.opponent = data.get('opponent')
        # Usar nuestro nuevo método para cargar y seleccionar un set de assets
        self.reload_asset_sets()
        
        # Limpiar y preparar la pantalla
        self.clear_main_frame()
        
        # Crear y añadir el chat SOLO UNA VEZ aquí
        self.create_chat()
        
        # Marco elegante para la información de la partida
        info_frame = ttk.Frame(self.main_frame, style="card.TFrame", padding=15)
        info_frame.pack(expand=True, pady=30)
        
        # Notificación de oponente con estilo moderno
        ttk.Label(
            info_frame, 
            text="¡Oponente encontrado!", 
            font=("Segoe UI", 14), 
            foreground="#17a2b8"
        ).pack(pady=5)
        
        ttk.Label(
            info_frame, 
            text=f"{self.opponent}", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#fd7e14"
        ).pack(pady=10)
        
        # Mensaje indicando el siguiente paso
        ttk.Label(
            info_frame, 
            text="Preparando la partida...", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).pack(pady=10)
        
        self.update_status("Esperando dinámica de apuesta...")

    def reload_asset_sets(self):
        """Recarga la lista de sets disponibles y selecciona uno aleatoriamente."""
        # Recargar todos los assets para asegurar que tenemos la última versión
        self.all_assets = load_all_assets()
        
        # Seleccionar un set aleatorio para la nueva partida
        available_sets = list(self.all_assets.keys())
        if available_sets:
            # Seleccionar un set diferente al actual si es posible
            if len(available_sets) > 1 and self.asset_set in available_sets:
                current_set = self.asset_set
                available_sets.remove(current_set)
                self.asset_set = random.choice(available_sets)
                print(f"Cambiando de set {current_set} a {self.asset_set}")
            else:
                self.asset_set = random.choice(available_sets)
                print(f"Seleccionado set {self.asset_set}")
        else:
            # Usar el set por defecto si no hay disponibles
            self.asset_set = "set1"
            print("No hay sets disponibles, usando set1 por defecto")
            
    def on_bet_request(self, data):
        self.is_initiator = True
        # Recargar assets antes de iniciar una nueva ronda
        self.reload_asset_sets()
        self.create_bet_proposal_screen()

    def create_bet_proposal_screen(self):
        self.bet_confirmed = False
        
        # Limpiar la pantalla manteniendo el chat
        self.clear_main_frame()
        
        # Función para manejar la confirmación de apuesta
        def on_confirm_bet():
            self.send_bet_proposal()
            
        # Crear componente de propuesta de apuesta
        bet_proposal = BetProposalScreen(
            self.main_frame,
            on_confirm_bet=on_confirm_bet
        )
        bet_proposal.pack(fill="both", expand=True)
        
        # Guardar referencia al campo de entrada
        self.bet_entry = bet_proposal.bet_entry
        
        self.update_status("")

    def send_bet_proposal(self):
        bet_amount = None
        try:
            bet_amount = int(self.bet_entry.get())
        except ValueError:
            self.update_status("Ingrese un número válido.")
            return
            
        if bet_amount is not None:
            set_bet(self.room, self.username, bet_amount)
            
            # Limpiar la pantalla manteniendo el chat
            self.clear_main_frame()
            
            # Crear pantalla de espera de apuesta
            bet_wait = BetWaitScreen(self.main_frame)
            bet_wait.pack(fill="both", expand=True)
            
            self.update_status("Esperando respuesta del oponente...")

    def on_bet_proposal(self, data):
        self.is_initiator = False
        bet = data.get('bet')
        
        # Limpiar la pantalla manteniendo el chat
        self.clear_main_frame()
        
        # Funciones de callback para aceptar/rechazar apuesta
        def on_accept_callback():
            self.send_accept_bet()
            
        def on_decline_callback():
            self.send_decline_bet()
            
        # Crear componente de respuesta a apuesta
        bet_response = BetResponseScreen(
            self.main_frame,
            bet_amount=bet,
            opponent=self.opponent,
            on_accept=on_accept_callback,
            on_decline=on_decline_callback
        )
        bet_response.pack(fill="both", expand=True)
        
        self.update_status("")

    def send_accept_bet(self):
        accept_bet(self.room, self.username)

    def send_decline_bet(self):
        decline_bet(self.room, self.username)
        
        # Eliminar chat
        self.remove_chat()
        
        # Limpiar pantalla
        self.clear_main_frame()
        
        # Crear componente de abandono
        abandon_screen = AbandonScreen(
            self.main_frame,
            message="Regresando al lobby...",
            on_return_lobby=self.create_lobby
        )
        abandon_screen.pack(fill="both", expand=True)
        
        self.after(2000, self.create_lobby)
        self.update_status("Volviendo al lobby...")

    def on_bet_confirmed(self, data):
        bet = data.get('bet')
        msg = data.get('message', f"Apuesta confirmada: {bet} créditos.")
        self.bet_confirmed = True
        self.update_status(msg)
        self.create_game_screen()

    def on_bet_declined(self, data):
        msg = data.get('message', "La apuesta ha sido rechazada.")
        self.update_status(msg)
        
        # Eliminar chat
        self.remove_chat()
            
        self.clear_main_frame()
        
        # Crear componente de abandono
        abandon_screen = AbandonScreen(
            self.main_frame,
            message=msg,
            on_return_lobby=self.create_lobby
        )
        abandon_screen.pack(fill="both", expand=True)

    def create_game_screen(self):
        self.images = load_assets(self.asset_set)
        self.button_images = []  # Mantener referencias para evitar recolección de basura
        
        # Limpiar la pantalla manteniendo el chat
        self.clear_main_frame()
        
        # Función para manejar la selección
        def on_choice_callback(option):
            self.send_choice(option)
            
        # Crear pantalla de juego
        game_screen = GameScreen(
            self.main_frame,
            room=self.room,
            opponent=self.opponent,
            images=self.images,
            on_choice=on_choice_callback
        )
        game_screen.pack(fill="both", expand=True)
        
        # Mantener referencias a las imágenes
        self.button_images = game_screen.button_images
        
        self.update_status("")

    def send_choice(self, option):
        make_choice(self.room, self.username, option, self.asset_set)
        
        # Limpiar la pantalla manteniendo el chat
        self.clear_main_frame()
        
        # Crear pantalla de espera de elección
        choice_wait = ChoiceWaitScreen(
            self.main_frame,
            choice=option
        )
        choice_wait.pack(fill="both", expand=True)
        
        self.update_status("Esperando la elección del oponente...")

    def on_game_result(self, data):
        result = data.get('result')
        bet = data.get('bet')
        choices = data.get('choices', {})
        credits_info = data.get('credits', {})
        user_credits = credits_info.get(self.username, 0)
        # Obtener los sets y imágenes de cada jugador
        player_sets = data.get('player_sets', {})
        
        # Actualizar créditos en la barra de información
        self.credits = user_credits
        self.user_info_bar.update_credits(user_credits)
        
        # Limpiar la pantalla manteniendo el chat
        self.clear_main_frame()
        
        # Funciones para jugar de nuevo o abandonar
        def on_play_again_callback():
            self.send_play_again()
            
        def on_abandon_callback():
            self.send_abandon()
        
        # Crear pantalla de resultados
        result_screen = ResultScreen(
            self.main_frame,
            result=result,
            bet=bet,
            choices=choices,
            images=self.images,
            player_sets=player_sets,
            all_assets=self.all_assets,
            username=self.username,
            on_play_again=on_play_again_callback,
            on_abandon=on_abandon_callback
        )
        result_screen.pack(fill="both", expand=True)
        
        self.update_status("")

    def send_play_again(self):
        play_again(self.room, self.username)
        self.update_status("Esperando confirmación para jugar de nuevo...")

    def send_abandon(self):
        abandon(self.room, self.username)
        
        # Eliminar chat
        self.remove_chat()
            
        self.clear_main_frame()
        
        # Crear componente de abandono
        abandon_screen = AbandonScreen(
            self.main_frame,
            message="Has abandonado la partida",
            on_return_lobby=self.create_lobby
        )
        abandon_screen.pack(fill="both", expand=True)
        
        self.update_status("Partida finalizada.")

    def on_abandon_confirm(self, data):
        msg = data.get('message', 'La partida ha finalizado.')
        
        # Eliminar chat
        self.remove_chat()
            
        self.clear_main_frame()
        
        # Crear componente de abandono
        abandon_screen = AbandonScreen(
            self.main_frame,
            message=msg,
            on_return_lobby=self.create_lobby
        )
        abandon_screen.pack(fill="both", expand=True)
        
        self.update_status("Regresando al lobby...")
    
    # Manejadores para chat y actualización de créditos
    def on_chat_message(self, data):
        """Maneja la recepción de un mensaje de chat."""
        if self.chat_frame:
            self.chat_frame.receive_message(data)
    
    def on_chat_history(self, data):
        """Carga el historial de chat recibido del servidor."""
        if self.chat_frame:
            history = data.get('history', [])
            self.chat_frame.load_chat_history(history)
    
    def on_credits_updated(self, data):
        """Actualiza los créditos mostrados en la barra de información."""
        new_credits = data.get('credits', self.credits)
        self.credits = new_credits
        self.user_info_bar.update_credits(new_credits)

if __name__ == '__main__':
    app = App()
    app.mainloop()