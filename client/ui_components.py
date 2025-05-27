import tkinter as tk
from tkinter import ttk, messagebox

class LoginScreen(ttk.Frame):
    """
    Pantalla de inicio de sesión y registro de usuarios.
    """
    def __init__(self, parent, server_config, on_login, on_register, on_server_config, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.server_config = server_config
        self.on_login = on_login
        self.on_register = on_register
        self.on_server_config = on_server_config
        
        # Variables para los campos de entrada
        self.entry_username = None
        self.entry_password = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pantalla de login."""
        # Crear un marco con efecto de tarjeta para el login
        frame = ttk.Frame(self, style="card.TFrame", padding=20)
        frame.pack(expand=True, pady=50)
        
        # Título elegante y centrado
        title_label = ttk.Label(
            frame, 
            text="Iniciar Sesión", 
            font=("Segoe UI", 16, "bold"), 
            foreground="#17a2b8"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos de entrada con diseño más limpio
        ttk.Label(
            frame, 
            text="Usuario:", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.entry_username = ttk.Entry(frame, width=25, font=("Segoe UI", 11))
        self.entry_username.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(
            frame, 
            text="Contraseña:", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.entry_password = ttk.Entry(frame, show="•", width=25, font=("Segoe UI", 11))
        self.entry_password.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.entry_password.bind("<Return>", lambda e: self.on_login())
        
        # Botones con estilo moderno y espaciado elegante
        btn_frame = ttk.Frame(frame, style="transparent.TFrame")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame, 
            text="Iniciar sesión", 
            command=self.on_login, 
            style="info.TButton", 
            width=15
        ).pack(side="left", padx=10)
        
        ttk.Button(
            btn_frame, 
            text="Registrarse", 
            command=self.on_register, 
            style="success.TButton", 
            width=15
        ).pack(side="left", padx=10)
        
        # Información del servidor conectado y botón para cambiar
        server_frame = ttk.Frame(frame, style="transparent.TFrame")
        server_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        server_label = ttk.Label(
            server_frame,
            text=f"Servidor: {self.server_config['host']}:{self.server_config['port']}",
            font=("Segoe UI", 9),
            foreground="#adb5bd"
        )
        server_label.pack(side="left", padx=5)
        
        ttk.Button(
            server_frame,
            text="Cambiar",
            command=self.on_server_config,
            style="secondary.TButton",
            width=8
        ).pack(side="left", padx=5)
    
    def get_credentials(self):
        """Retorna el nombre de usuario y contraseña ingresados."""
        return self.entry_username.get(), self.entry_password.get()
    
    def focus_username(self):
        """Da foco al campo de nombre de usuario."""
        self.entry_username.focus_set()


class LobbyScreen(ttk.Frame):
    """
    Pantalla del lobby principal del juego.
    """
    def __init__(self, parent, username, credits, on_search_match, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.username = username
        self.credits = credits
        self.on_search_match = on_search_match
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario del lobby."""
        # Marco elegante para el lobby con efecto de tarjeta
        frame = ttk.Frame(self, style="card.TFrame", padding=20)
        frame.pack(expand=True, pady=50)
        
        # Bienvenida personalizada con formato atractivo
        ttk.Label(
            frame, 
            text=f"Bienvenido, {self.username}", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#17a2b8"
        ).pack(pady=15)
        
        # Saldo con formato distintivo
        saldo_frame = ttk.Frame(frame, style="transparent.TFrame")
        saldo_frame.pack(pady=15)
        
        ttk.Label(
            saldo_frame, 
            text=f"Tu saldo actual:", 
            font=("Segoe UI", 12), 
            foreground="#adb5bd"
        ).pack(side="left")
        
        ttk.Label(
            saldo_frame, 
            text=f"{self.credits} créditos", 
            font=("Segoe UI", 12, "bold"), 
            foreground="#ffc107"
        ).pack(side="left", padx=5)
        
        # Botón de búsqueda con estilo llamativo pero elegante
        ttk.Button(
            frame, 
            text="Buscar partida", 
            command=self.on_search_match, 
            style="warning.TButton", 
            width=20
        ).pack(pady=20)
    
    def update_credits(self, new_credits):
        """Actualiza el saldo mostrado en el lobby."""
        self.credits = new_credits
        # Actualizar la etiqueta de créditos
        # Tendríamos que mantener una referencia a la etiqueta para actualizarla


class MatchSearchScreen(ttk.Frame):
    """
    Pantalla de búsqueda de partida.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pantalla de búsqueda."""
        # Marco para la búsqueda con animación de carga
        frame = ttk.Frame(self, style="card.TFrame", padding=20)
        frame.pack(expand=True, pady=50)
        
        # Mensaje de búsqueda con formato elegante
        ttk.Label(
            frame, 
            text="Buscando oponente...", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#fd7e14"
        ).pack(pady=15)
        
        # Mensaje secundario con instrucciones
        ttk.Label(
            frame, 
            text="Espere mientras se conecta con otro jugador", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).pack(pady=10)


class BetProposalScreen(ttk.Frame):
    """
    Pantalla para proponer una apuesta.
    """
    def __init__(self, parent, on_confirm_bet, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.on_confirm_bet = on_confirm_bet
        
        self.bet_entry = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario para proponer apuesta."""
        # Marco elegante para la propuesta de apuesta
        bet_frame = ttk.Frame(self, style="card.TFrame", padding=20)
        bet_frame.pack(expand=True, pady=30)
        
        # Título y mensaje con estilo moderno
        ttk.Label(
            bet_frame, 
            text="Propón tu apuesta", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#17a2b8"
        ).pack(pady=10)
        
        ttk.Label(
            bet_frame, 
            text="¿Cuántos créditos quieres apostar?", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).pack(pady=5)
        
        # Campo de entrada con estilo elegante
        self.bet_entry = ttk.Entry(bet_frame, width=10, font=("Segoe UI", 16), justify="center")
        self.bet_entry.pack(pady=15)
        self.bet_entry.focus_set()  # Dar foco al campo de apuesta
        self.bet_entry.bind("<Return>", lambda e: self.on_confirm_bet())
        
        # Botón de confirmación llamativo pero elegante
        ttk.Button(
            bet_frame, 
            text="Confirmar apuesta", 
            command=self.on_confirm_bet, 
            style="warning.TButton", 
            width=20
        ).pack(pady=15)
    
    def get_bet_amount(self):
        """Retorna el monto de la apuesta ingresado."""
        try:
            return int(self.bet_entry.get())
        except ValueError:
            return None


class BetWaitScreen(ttk.Frame):
    """
    Pantalla de espera después de proponer una apuesta.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de espera de apuesta."""
        # Marco para mensaje de espera con estilo elegante
        wait_frame = ttk.Frame(self, style="card.TFrame", padding=20)
        wait_frame.pack(expand=True, pady=30)
        
        # Mensaje con formato atractivo
        ttk.Label(
            wait_frame, 
            text="Apuesta propuesta", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#17a2b8"
        ).pack(pady=10)
        
        ttk.Label(
            wait_frame, 
            text="Esperando respuesta del oponente...", 
            font=("Segoe UI", 12), 
            foreground="#fd7e14"
        ).pack(pady=10)


class BetResponseScreen(ttk.Frame):
    """
    Pantalla para responder a una propuesta de apuesta.
    """
    def __init__(self, parent, bet_amount, opponent, on_accept, on_decline, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.bet_amount = bet_amount
        self.opponent = opponent
        self.on_accept = on_accept
        self.on_decline = on_decline
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario para responder a apuesta."""
        # Marco para la propuesta de apuesta con estilo elegante
        bet_frame = ttk.Frame(self, style="card.TFrame", padding=20)
        bet_frame.pack(expand=True, pady=30)
        
        # Mensaje principal con formato atractivo
        ttk.Label(
            bet_frame, 
            text="Propuesta de apuesta", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#17a2b8"
        ).pack(pady=10)
        
        msg = f"El jugador propone apostar {self.bet_amount} créditos"
        ttk.Label(
            bet_frame, 
            text=msg, 
            font=("Segoe UI", 14), 
            foreground="#fd7e14"
        ).pack(pady=10)
        
        ttk.Label(
            bet_frame, 
            text="¿Aceptas la apuesta?", 
            font=("Segoe UI", 12), 
            foreground="#adb5bd"
        ).pack(pady=10)
        
        # Botones con estilo moderno y espaciado elegante
        btn_frame = ttk.Frame(bet_frame, style="transparent.TFrame")
        btn_frame.pack(pady=15)
        
        ttk.Button(
            btn_frame, 
            text="Aceptar", 
            command=self.on_accept, 
            style="success.TButton", 
            width=15
        ).pack(side="left", padx=10)
        
        ttk.Button(
            btn_frame, 
            text="Rechazar", 
            command=self.on_decline, 
            style="danger.TButton", 
            width=15
        ).pack(side="left", padx=10)


class GameScreen(ttk.Frame):
    """
    Pantalla principal del juego.
    """
    def __init__(self, parent, room, opponent, images, on_choice, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.room = room
        self.opponent = opponent
        self.images = images
        self.on_choice = on_choice
        self.button_images = []  # Mantener referencias a las imágenes
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pantalla de juego."""
        # Marco para el juego con estilo elegante
        play_frame = ttk.Frame(self, style="card.TFrame", padding=15)
        play_frame.pack(expand=True, pady=20)
        
        # Información de la partida con formato atractivo
        info_container = ttk.Frame(play_frame, style="transparent.TFrame")
        info_container.pack(fill="x", pady=5)
        
        ttk.Label(
            info_container, 
            text=f"Partida en sala:", 
            font=("Segoe UI", 10), 
            foreground="#adb5bd"
        ).pack(side="left")
        
        room_id = self.room.split("_")[-1][:8] + "..." if len(self.room) > 20 else self.room
        ttk.Label(
            info_container, 
            text=room_id, 
            font=("Segoe UI", 10), 
            foreground="#17a2b8"
        ).pack(side="left", padx=5)
        
        # Nombre del oponente destacado
        ttk.Label(
            play_frame, 
            text=f"VS {self.opponent}", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#fd7e14"
        ).pack(pady=10)
        
        # Indicación para seleccionar opción
        ttk.Label(
            play_frame, 
            text="Seleccione su opción:", 
            font=("Segoe UI", 12), 
            foreground="#e9ecef"
        ).pack(pady=10)
        
        # Contenedor para las opciones con diseño más atractivo
        options_container = ttk.Frame(play_frame, style="transparent.TFrame")
        options_container.pack(pady=10)
        
        # Estilos y colores para cada opción
        option_styles = {
            'piedra': {"style": "warning.TButton", "color": "#ffc107"},   # Amarillo
            'papel': {"style": "info.TButton", "color": "#17a2b8"},       # Azul claro
            'tijera': {"style": "danger.TButton", "color": "#dc3545"},    # Rojo
            'lagarto': {"style": "success.TButton", "color": "#28a745"},  # Verde
            'spock': {"style": "primary.TButton", "color": "#007bff"}     # Azul oscuro
        }
        
        # Crear cada botón de opción con estilo elegante
        for option in ['piedra', 'papel', 'tijera', 'lagarto', 'spock']:
            # Marco para contener cada opción
            option_frame = ttk.Frame(options_container, style="transparent.TFrame")
            option_frame.pack(side="left", padx=10, pady=5)
            
            # Botón con imagen
            btn = ttk.Button(
                option_frame, 
                text=option.capitalize(), 
                command=lambda opt=option: self.on_choice(opt),
                style=option_styles[option]["style"]
            )
            
            if self.images.get(option):
                btn.config(image=self.images[option], compound=tk.TOP)
                self.button_images.append(self.images[option])  # Mantener referencia
            btn.pack(side="top", pady=2)
            
            # Etiqueta con el nombre de la opción
            ttk.Label(
                option_frame, 
                text=option.capitalize(), 
                font=("Segoe UI", 9, "bold"), 
                foreground=option_styles[option]["color"]
            ).pack(side="top")


class ChoiceWaitScreen(ttk.Frame):
    """
    Pantalla de espera después de hacer una selección.
    """
    def __init__(self, parent, choice, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.choice = choice
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de espera de selección."""
        # Marco para mensaje de espera con estilo elegante
        wait_frame = ttk.Frame(self, style="card.TFrame", padding=20)
        wait_frame.pack(expand=True, pady=30)
        
        # Mensajes con formato atractivo
        ttk.Label(
            wait_frame, 
            text="¡Selección realizada!", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#17a2b8"
        ).pack(pady=10)
        
        ttk.Label(
            wait_frame, 
            text=f"Has seleccionado: {self.choice.capitalize()}", 
            font=("Segoe UI", 14), 
            foreground="#fd7e14"
        ).pack(pady=10)
        
        ttk.Label(
            wait_frame, 
            text="Esperando la elección del oponente...", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).pack(pady=10)


class ResultScreen(ttk.Frame):
    """
    Pantalla de resultados de la partida.
    """
    def __init__(self, parent, result, bet, choices, images, player_sets, all_assets, 
                 username, on_play_again, on_abandon, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.result = result
        self.bet = bet
        self.choices = choices
        self.images = images
        self.player_sets = player_sets
        self.all_assets = all_assets
        self.username = username
        self.on_play_again = on_play_again
        self.on_abandon = on_abandon
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pantalla de resultados."""
        # Determinar estilo basado en el resultado
        result_style = "card.TFrame"
        result_color = "#adb5bd"  # Gris para empate
        
        if "Ganador" in self.result:
            if self.result.endswith(self.username):
                result_color = "#28a745"  # Verde para victoria
            else:
                result_color = "#dc3545"  # Rojo para derrota
        
        # Marco para mostrar resultados con estilo elegante pero más compacto
        result_frame = ttk.Frame(self, style=result_style, padding=15)
        result_frame.pack(expand=True, pady=10)  # Reducido el padding
        
        # Resultado principal con formato atractivo
        ttk.Label(
            result_frame, 
            text="Resultado", 
            font=("Segoe UI", 14), 
            foreground="#e9ecef"
        ).pack(pady=3)  # Reducido el padding
        
        ttk.Label(
            result_frame, 
            text=self.result, 
            font=("Segoe UI", 16, "bold"),  # Reducido el tamaño de fuente
            foreground=result_color
        ).pack(pady=3)  # Reducido el padding
        
        # Información de la apuesta
        bet_frame = ttk.Frame(result_frame, style="transparent.TFrame")
        bet_frame.pack(pady=5)  # Reducido el padding
        
        ttk.Label(
            bet_frame, 
            text="Apuesta:", 
            font=("Segoe UI", 11), 
            foreground="#adb5bd"
        ).pack(side="left")
        
        ttk.Label(
            bet_frame, 
            text=f"{self.bet} créditos", 
            font=("Segoe UI", 11, "bold"), 
            foreground="#ffc107"
        ).pack(side="left", padx=5)
        
        # Contenedor para mostrar las elecciones con separador
        choices_title = ttk.Label(
            result_frame, 
            text="Elecciones", 
            font=("Segoe UI", 12, "bold"), 
            foreground="#e9ecef"
        )
        choices_title.pack(pady=(8, 5))  # Reducido el padding
        
        # Línea separadora
        separator = ttk.Separator(result_frame, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=3)  # Reducido el padding
        
        # Marco para las elecciones con diseño elegante
        choices_frame = ttk.Frame(result_frame, style="transparent.TFrame")
        choices_frame.pack(pady=5)  # Reducido el padding
        
        # Mostrar cada elección con su imagen
        for player, choice in self.choices.items():
            # Marco para cada jugador
            player_frame = ttk.Frame(choices_frame, style="transparent.TFrame", padding=3)
            player_frame.pack(side="left", padx=15)
            
            # Color basado en si es el jugador actual o el oponente
            player_color = "#17a2b8" if player == self.username else "#fd7e14"
            
            # Nombre del jugador
            ttk.Label(
                player_frame, 
                text=player, 
                font=("Segoe UI", 11, "bold"), 
                foreground=player_color
            ).pack(pady=2)
            
            # Elección del jugador
            choice_display = ttk.Frame(player_frame, style="transparent.TFrame")
            choice_display.pack(pady=3)  # Reducido el padding
            
            # Si es el jugador local, usar su propia imagen
            if player == self.username and self.images.get(choice):
                lbl = ttk.Label(choice_display, image=self.images[choice])
                lbl.image = self.images[choice]  # Mantener referencia
                lbl.pack()
                
                ttk.Label(
                    choice_display, 
                    text=choice.capitalize(), 
                    font=("Segoe UI", 9), 
                    foreground="#e9ecef"
                ).pack(pady=2)
                
            # Si es el oponente, intentar usar el set que está usando el oponente
            elif player != self.username:
                opponent_set = self.player_sets.get(player, '')
                
                # Intentar cargar la imagen del conjunto del oponente
                opponent_images = self.all_assets.get(opponent_set, {})
                if opponent_images and opponent_images.get(choice):
                    lbl = ttk.Label(choice_display, image=opponent_images[choice])
                    lbl.image = opponent_images[choice]  # Mantener referencia
                    lbl.pack()
                # Si no está disponible, usar la imagen del mismo set que estamos usando
                elif self.images.get(choice):
                    lbl = ttk.Label(choice_display, image=self.images[choice])
                    lbl.image = self.images[choice]  # Mantener referencia
                    lbl.pack()
                
                ttk.Label(
                    choice_display, 
                    text=choice.capitalize(), 
                    font=("Segoe UI", 9), 
                    foreground="#e9ecef"
                ).pack(pady=2)
                
            else:
                ttk.Label(
                    choice_display, 
                    text=choice.capitalize(), 
                    font=("Segoe UI", 11, "bold"), 
                    foreground="#e9ecef"
                ).pack(pady=3)
        
        # Separador antes de los botones
        separator2 = ttk.Separator(result_frame, orient="horizontal")
        separator2.pack(fill="x", padx=20, pady=8)
        
        # Botones para acciones post-partida con estilo elegante
        btn_frame = ttk.Frame(result_frame, style="transparent.TFrame")
        btn_frame.pack(pady=8)  # Reducido el padding
        
        ttk.Button(
            btn_frame, 
            text="Jugar de nuevo", 
            command=self.on_play_again, 
            style="success.TButton", 
            width=15
        ).pack(side="left", padx=10)
        
        ttk.Button(
            btn_frame, 
            text="Abandonar", 
            command=self.on_abandon, 
            style="danger.TButton", 
            width=15
        ).pack(side="left", padx=10)


class AbandonScreen(ttk.Frame):
    """
    Pantalla mostrada cuando un jugador abandona la partida.
    """
    def __init__(self, parent, message, on_return_lobby, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.message = message
        self.on_return_lobby = on_return_lobby
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pantalla de abandono."""
        # Marco para mensaje de abandono con estilo elegante
        frame = ttk.Frame(self, style="card.TFrame", padding=20)
        frame.pack(expand=True, pady=30)
        
        # Mensaje con formato atractivo
        ttk.Label(
            frame, 
            text="Partida finalizada", 
            font=("Segoe UI", 18, "bold"), 
            foreground="#fd7e14"
        ).pack(pady=10)
        
        ttk.Label(
            frame, 
            text=self.message, 
            font=("Segoe UI", 12), 
            foreground="#adb5bd"
        ).pack(pady=10)
        
        # Botón para volver al lobby con estilo elegante
        ttk.Button(
            frame, 
            text="Volver al Lobby", 
            command=self.on_return_lobby, 
            style="info.TButton", 
            width=15
        ).pack(pady=15)


def create_server_config_dialog(parent, current_config, on_save):
    """
    Crea un diálogo para configurar la conexión al servidor.
    """
    dialog = tk.Toplevel(parent)
    dialog.title("Configuración del Servidor")
    dialog.geometry("300x150")
    dialog.transient(parent)
    dialog.grab_set()
    
    frame = ttk.Frame(dialog, padding=10)
    frame.pack(fill="both", expand=True)
    
    # Campos para host y puerto
    ttk.Label(frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    host_entry = ttk.Entry(frame, width=20)
    host_entry.grid(row=0, column=1, padx=5, pady=5)
    host_entry.insert(0, current_config["host"])
    
    ttk.Label(frame, text="Puerto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    port_entry = ttk.Entry(frame, width=20)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    port_entry.insert(0, str(current_config["port"]))
    
    def save_config():
        try:
            host = host_entry.get().strip()
            port = int(port_entry.get().strip())
            on_save(host, port)
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número entero")
    
    # Botones de guardar y cancelar
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Button(btn_frame, text="Guardar", command=save_config).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side="left", padx=5)
    
    return dialog