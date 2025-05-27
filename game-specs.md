# Especificaciones: Juego Multijugador de Piedra, Papel, Tijera, Lagarto, Spock

## Arquitectura del Sistema

### Servidor
- **Tecnología**: Python con Socket.IO para comunicación en tiempo real
- **Base de datos**: JSON para almacenar usuarios, partidas y puntuaciones
- **Seguridad**: Comunicación cifrada mediante SSL/TLS
- **Gestión de certificados**: Generación automática de certificados autofirmados si no existen

### Cliente
- **Interfaz**: tkinter con tema oscuro estilo Bootstrap
- **Audio**: Reproducción de sonidos WAV para inicio de partida
- **Gráficos**: Sistema de carga de assets desde directorio local definido en JSON
- **Conectividad**: Conexión cifrada con el servidor

## Módulos del Servidor

### 1. Sistema de Autenticación
- Registro de nuevos usuarios con nombre y contraseña
- Login de usuarios existentes
- Almacenamiento seguro de contraseñas (hash + salt)
- Gestión de acceso a archivos JSON de usuarios

### 2. Sistema de Emparejamiento
- Cola de espera para jugadores
- Emparejamiento aleatorio entre jugadores disponibles
- Creación de salas de juego independientes

### 3. Gestor de Partidas
- Control del estado de cada partida activa
- Sincronización de acciones entre jugadores
- Temporizador para límite de selección
- Validación de jugadas y determinación del ganador
- **Rotación de assets**: Selección aleatoria del conjunto de imágenes para cada partida

### 4. Sistema de Apuestas
- Gestión de créditos por usuario
- Procesamiento de propuestas de apuesta
- Transferencia de créditos al ganador

### 5. Tabla de Clasificación
- Registro de victorias/derrotas
- Cálculo de puntuaciones
- Ranking de los mejores jugadores

### 6. Seguridad
- Generación y gestión de certificados SSL
- Cifrado de comunicaciones
- Protección contra trampas y manipulaciones

## Módulos del Cliente

### 1. Interfaz Gráfica (tkinter)
- Tema oscuro estilo Bootstrap
- Pantallas: login, lobby, partida, historial, ranking
- Animaciones para revelación de selecciones

### 2. Gestor de Assets
- Carga de múltiples variantes de imágenes desde directorio local
- Parseo de archivo JSON de configuración
- **Selección aleatoria de conjunto de imágenes para cada partida**
- Presentación aleatoria de miniaturas para selección del jugador

### 3. Sistema de Audio
- Reproducción de sonido WAV al inicio de cada ronda
- Efectos sonoros para victoria/derrota/empate

### 4. Comunicación con Servidor
- Conexión segura mediante SSL
- Manejo de eventos en tiempo real
- Sincronización de estado de juego y assets seleccionados

### 5. Lógica de Juego
- Implementación de reglas de Piedra, Papel, Tijera, Lagarto, Spock
- Manejo de selecciones del usuario
- Cálculo de resultados

### 6. Sistema de Apuestas
- Interfaz para proponer/aceptar apuestas
- Visualización de créditos disponibles
- Historial de apuestas

## Reglas del Juego

Las reglas de Piedra, Papel, Tijera, Lagarto, Spock son:

- Tijera corta Papel
- Papel cubre Piedra
- Piedra aplasta Lagarto
- Lagarto envenena Spock
- Spock rompe Tijera
- Tijera decapita Lagarto
- Lagarto come Papel
- Papel desautoriza Spock
- Spock vaporiza Piedra
- Piedra aplasta Tijera

## Flujo de Juego

1. El usuario se registra/inicia sesión
2. El sistema empareja al usuario con un oponente aleatorio
3. El ganador del último juego propone la apuesta
4. El retador decide si acepta
5. **El servidor selecciona aleatoriamente un conjunto de imágenes para la partida**
6. Comienza la partida con reproducción de sonido
7. Al finalizar el sonido, ambos jugadores ven opciones con las imágenes seleccionadas
8. Cada jugador selecciona su opción (oculta para el oponente)
9. Una vez que ambos seleccionan, se revelan las elecciones
10. Se determina el ganador y se transfieren los créditos
11. Se actualiza la tabla de clasificación

## Estructura de Datos

### Base de Datos JSON (Server)

```json
// Estructura de usuarios.json
{
  "usuarios": [
    {
      "id": 1,
      "username": "usuario1",
      "password_hash": "hash_de_la_contraseña",
      "creditos": 1000,
      "partidas_jugadas": 0,
      "partidas_ganadas": 0,
      "fecha_registro": "2025-03-09T10:30:00"
    },
    {
      "id": 2,
      "username": "usuario2",
      "password_hash": "hash_de_la_contraseña",
      "creditos": 1000,
      "partidas_jugadas": 0,
      "partidas_ganadas": 0,
      "fecha_registro": "2025-03-09T11:15:00"
    }
  ],
  "next_id": 3
}

// Estructura de partidas.json
{
  "partidas": [
    {
      "id": 1,
      "jugador1_id": 1,
      "jugador2_id": 2,
      "seleccion_jugador1": "piedra",
      "seleccion_jugador2": "papel",
      "ganador_id": 2,
      "cantidad_apuesta": 50,
      "set_imagenes_id": "set2",
      "fecha_partida": "2025-03-09T12:45:00"
    }
  ],
  "next_id": 2
}

// Estructura de salas.json
{
  "salas": [
    {
      "id": 1,
      "jugador1_id": 3,
      "jugador2_id": 4,
      "estado": "en_progreso",
      "set_imagenes_id": "set3",
      "apuesta_propuesta": 75,
      "apuesta_aceptada": true,
      "fecha_creacion": "2025-03-09T13:20:00"
    }
  ],
  "next_id": 2
}
```

### JSON de Configuración de Assets (Cliente)

```json
{
  "sets": {
    "set1": {
      "piedra": {
        "imagen": "piedra_clasica.png",
        "descripcion": "Piedra aplasta Tijera y Lagarto"
      },
      "papel": {
        "imagen": "papel_clasico.png",
        "descripcion": "Papel cubre Piedra y desautoriza Spock"
      },
      "tijera": {
        "imagen": "tijera_clasica.png",
        "descripcion": "Tijera corta Papel y decapita Lagarto"
      },
      "lagarto": {
        "imagen": "lagarto_clasico.png",
        "descripcion": "Lagarto come Papel y envenena Spock"
      },
      "spock": {
        "imagen": "spock_clasico.png",
        "descripcion": "Spock rompe Tijera y vaporiza Piedra"
      }
    },
    "set2": {
      "piedra": {
        "imagen": "piedra_futurista.png",
        "descripcion": "Piedra aplasta Tijera y Lagarto"
      },
      "papel": {
        "imagen": "papel_futurista.png",
        "descripcion": "Papel cubre Piedra y desautoriza Spock"
      },
      "tijera": {
        "imagen": "tijera_futurista.png",
        "descripcion": "Tijera corta Papel y decapita Lagarto"
      },
      "lagarto": {
        "imagen": "lagarto_futurista.png",
        "descripcion": "Lagarto come Papel y envenena Spock"
      },
      "spock": {
        "imagen": "spock_futurista.png",
        "descripcion": "Spock rompe Tijera y vaporiza Piedra"
      }
    },
    "set3": {
      "piedra": {
        "imagen": "piedra_medieval.png",
        "descripcion": "Piedra aplasta Tijera y Lagarto"
      },
      "papel": {
        "imagen": "papel_medieval.png",
        "descripcion": "Papel cubre Piedra y desautoriza Spock"
      },
      "tijera": {
        "imagen": "tijera_medieval.png",
        "descripcion": "Tijera corta Papel y decapita Lagarto"
      },
      "lagarto": {
        "imagen": "lagarto_medieval.png",
        "descripcion": "Lagarto come Papel y envenena Spock"
      },
      "spock": {
        "imagen": "spock_medieval.png",
        "descripcion": "Spock rompe Tijera y vaporiza Piedra"
      }
    }
  },
  "sonidos": {
    "inicio_partida": "countdown.wav",
    "victoria": "win.wav",
    "derrota": "lose.wav",
    "empate": "draw.wav"
  }
}
```

## Protocolos de Comunicación

### Eventos del Servidor al Cliente:
- `login_success`: Confirmación de inicio de sesión
- `match_found`: Emparejamiento encontrado
- `game_start`: Inicio de partida
- `set_assets`: Envío del conjunto de imágenes seleccionado para la partida
- `bet_proposed`: Propuesta de apuesta
- `reveal_choices`: Revelar selecciones
- `game_result`: Resultado de la partida
- `credits_update`: Actualización de créditos
- `leaderboard_update`: Actualización de clasificación

### Eventos del Cliente al Servidor:
- `register`: Registro de nuevo usuario
- `login`: Inicio de sesión
- `find_match`: Buscar partida
- `propose_bet`: Proponer apuesta
- `accept_bet`: Aceptar apuesta
- `decline_bet`: Rechazar apuesta
- `make_choice`: Realizar selección
- `disconnect`: Desconexión del usuario

## Implementación de Rotación de Assets

1. **Selección aleatoria**: Al crear una nueva partida, el servidor selecciona aleatoriamente uno de los conjuntos de imágenes disponibles.

2. **Sincronización**: El servidor envía el identificador del conjunto seleccionado a ambos clientes mediante el evento `set_assets`.

3. **Carga de imágenes**: Cada cliente carga las imágenes correspondientes al conjunto indicado desde su directorio local.

4. **Presentación**: Las miniaturas de selección se muestran utilizando este conjunto específico para toda la duración de la partida.

5. **Almacenamiento**: El conjunto utilizado se almacena en la base de datos junto con los detalles de la partida para referencia futura.

Esta implementación garantiza que los jugadores tengan una experiencia visual variada en cada partida, manteniendo el interés y la frescura del juego.