import tkinter as tk
from tkinter import ttk, scrolledtext
import datetime
from main_functions import send_chat_message

class ChatFrame(ttk.Frame):
    """
    Componente para mostrar y gestionar el chat entre jugadores.
    Incluye área de visualización de mensajes y campo de entrada.
    """
    def __init__(self, parent, room, username, max_height=150, **kwargs):
        super().__init__(parent, **kwargs)
        self.room = room
        self.username = username
        self.max_height = max_height
        self.setup_ui()
        
    def setup_ui(self):
        """Configura los elementos de la interfaz del chat."""
        # Frame principal con borde sutil y redondeado
        self.config(padding=5, relief="flat", borderwidth=0)
        
        # Top bar con título y estilo minimalista
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 5))
        
        # Título del chat con estilo moderno
        title_label = ttk.Label(
            top_frame, 
            text="Chat de Partida", 
            font=("Segoe UI", 10, "bold"), 
            foreground="#28a745"  # Verde Bootstrap
        )
        title_label.pack(side="left")
        
        # Dividimos el chat con un diseño más moderno
        chat_container = ttk.Frame(self)
        chat_container.pack(fill="both", expand=True)
        
        # Marco para el área de mensajes con bordes suaves
        msg_frame = ttk.Frame(chat_container, relief="flat")
        msg_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Área de mensajes con fondo claro, más elegante
        self.chat_display = scrolledtext.ScrolledText(
            msg_frame, 
            wrap="word", 
            height=6,
            state="disabled",
            font=("Segoe UI", 9),
            bg="#212529",  # Fondo oscuro Bootstrap
            fg="#e9ecef",  # Texto claro Bootstrap
            padx=10,
            pady=5,
            relief="flat",
            borderwidth=1,
            highlightbackground="#343a40",  # Borde sutil
            highlightthickness=1
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Frame para entrada de mensaje con diseño integrado
        input_frame = ttk.Frame(chat_container)
        input_frame.pack(side="right", fill="y", padx=0, pady=0)
        
        # Entrada elegante que ocupa la altura
        self.message_input = ttk.Entry(
            input_frame,
            font=("Segoe UI", 9),
            width=20
        )
        self.message_input.pack(fill="both", expand=True, padx=0, pady=(0, 5))
        self.message_input.bind("<Return>", self.send_message)  # Enviar al presionar Enter
        
        # Botón de enviar moderno y simple
        send_button = ttk.Button(
            input_frame, 
            text="Enviar", 
            command=self.send_message,
            style="success.TButton",
            width=10
        )
        send_button.pack(fill="x")
        
        # Dar foco al campo de entrada
        self.message_input.focus_set()
    
    def send_message(self, event=None):
        """Envía el mensaje escrito al servidor."""
        message = self.message_input.get()
        if message.strip():
            send_chat_message(self.room, self.username, message)
            self.message_input.delete(0, tk.END)  # Limpiar después de enviar
    
    def receive_message(self, message_data):
        """
        Muestra un mensaje recibido en el área de chat.
        
        Args:
            message_data: Diccionario con username, message y timestamp.
        """
        # Guardar la posición actual del scroll
        self.chat_display.config(state="normal")
        
        # Formato para mensajes
        username = message_data.get('username', 'Desconocido')
        message = message_data.get('message', '')
        timestamp = message_data.get('timestamp', 
                                    datetime.datetime.now().strftime("%H:%M:%S"))
        
        # Estilo moderno de chat inspirado en aplicaciones profesionales
        if username == self.username:
            # Formato para mensajes propios más sutil
            self.chat_display.insert(tk.END, f"Tú ({timestamp}): ", "own_user")
            self.chat_display.insert(tk.END, f"{message}\n", "own_message")
        else:
            # Formato para mensajes de otros usuarios
            self.chat_display.insert(tk.END, f"{username} ({timestamp}): ", "other_user")
            self.chat_display.insert(tk.END, f"{message}\n", "other_message")
        
        # Colores sutiles y elegantes para los mensajes
        self.chat_display.tag_config("own_user", foreground="#17a2b8", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_config("own_message", foreground="#e9ecef")
        self.chat_display.tag_config("other_user", foreground="#fd7e14", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_config("other_message", foreground="#e9ecef")
        
        # Desplazar hacia abajo para mostrar el último mensaje
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")
    
    def load_chat_history(self, history):
        """
        Carga el historial de chat en el área de visualización.
        
        Args:
            history: Lista de mensajes, cada uno como un diccionario.
        """
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0, tk.END)  # Limpiar área primero
        
        for message_data in history:
            self.receive_message(message_data)
        
        self.chat_display.config(state="disabled")
    
    def clear(self):
        """Limpia el área de chat."""
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state="disabled")

class UserInfoBar(ttk.Frame):
    """
    Barra superior que muestra el nombre del usuario y su saldo actual.
    Se actualiza cuando cambia el saldo.
    """
    def __init__(self, parent, username="Jugador", credits=0, **kwargs):
        super().__init__(parent, **kwargs)
        self.username = username
        self.credits = credits
        self.setup_ui()
    
    def setup_ui(self):
        """Configura los elementos visuales de la barra de información."""
        # Marco principal con diseño refinado y unificado
        self.config(padding=(10, 8), relief="flat", borderwidth=0)
        
        # Fondo unificado
        self.configure(style="primary.TFrame")
        
        # Contenedor para mantener todo en una línea
        content_frame = ttk.Frame(self, style="primary.TFrame")
        content_frame.pack(fill="x", expand=True)
        
        # Etiqueta para el nombre de usuario (integrada en el diseño)
        self.username_label = ttk.Label(
            content_frame, 
            text=f"Usuario: {self.username}", 
            font=("Segoe UI", 10, "bold"),
            foreground="white",
            background="#6f42c1",  # Color morado de bootstrap theme
            padding=(10, 2)
        )
        self.username_label.pack(side="left")
        
        # Etiqueta para los créditos (integrada en el mismo diseño)
        self.credits_label = ttk.Label(
            content_frame, 
            text=f"Saldo: {self.credits} créditos", 
            font=("Segoe UI", 10),
            foreground="white",
            background="#6f42c1",  # Mismo color para continuidad
            padding=(10, 2)
        )
        self.credits_label.pack(side="right", padx=(0, 10))
    
    def update_credits(self, new_credits):
        """Actualiza el saldo mostrado."""
        self.credits = new_credits
        self.credits_label.config(text=f"Saldo: {self.credits} créditos")
    
    def update_username(self, new_username):
        """Actualiza el nombre de usuario mostrado."""
        self.username = new_username
        self.username_label.config(text=f"Usuario: {self.username}")