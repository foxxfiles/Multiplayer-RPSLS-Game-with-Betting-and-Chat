# Multiplayer RPSLS Game with Betting and Chat

## Mission

Provide players and network administrators with a robust, interactive platform for engaging matches of Rock-Paper-Scissors-Lizard-Spock that ensures fair play through SSL/TLS encryption, secure credential handling, and transparent bet management while offering an intuitive GUI and seamless server-client communication.

## Vision

To become the go-to educational and entertainment tool for demonstrating real-time socket programming, secure communications, and game logic, fostering community engagement, encouraging experimentation with extensible asset sets, and promoting best practices in network application design.

## How to Use

1. Installation
    * Ensure prerequisites are installed: Python ≥3.8.
    * Clone repository and enter directory:
```bash 
git clone https://github.com/foxxfiles/Multiplayer-RPSLS-Game-with-Betting-and-Chat
cd Multiplayer-RPSLS-Game-with-Betting-and-Chat
```
    * Install dependencies:
```bash 
pip install -r requirements.txt
```
2. 
    * SSL certificates are auto-generated if missing.
    * Edit server_config.json to set host and port for the server.
    * Define asset sets and sounds in client/assets_config.json (see game-specs.md).

3. 
    * Start the Flask‑SocketIO server with SSL:
```bash 
python ./server/server.py
```
    * The server handles user registration/login, matchmaking, betting logic, and encrypted real-time events.
4. Running the Client

    * Launch the Tkinter client GUI:
```bash 
python main.py
```
    * Use the Login or Register screens to authenticate.

    * In the Lobby, click Find Match to join the queue.

5. Gameplay Workflow

    * Once matched, the initiator proposes a bet.

    * Both players confirm or decline the wager.

    * A random asset set (images for rock/paper/scissors/lizard/spock) is selected and synchronized.

    * Countdown sound plays, then players select their icon.

    * Results, credit updates, and chat messages are displayed instantly.

    * Players may choose to Play Again or Abandon to return to the lobby.

6. Data Persistence

    * ./server/usuarios.json stores user records with hashed & salted passwords, credit balances, and match statistics.

    * partidas.json and salas.json track completed games and active rooms respectively.

7. Advanced Features

    * Add or modify asset sets by editing game-specs.md configuration blocks.

    * Customize UI themes or controls via ui_components.py and ttkbootstrap.

    * Extend betting rules or add tournaments by enhancing server.py matchmaker and game state logic.