# Historias de Usuario - Juego Multijugador de Piedra, Papel, Tijera, Lagarto, Spock

## Módulo de Autenticación

### HU-01: Registro de Nuevo Usuario
**Como** usuario nuevo del sistema  
**Quiero** poder registrarme con un nombre de usuario y contraseña  
**Para** tener acceso personalizado al juego y que se guarde mi progreso

#### Criterios de Aceptación:
- El sistema permite registrar un nombre de usuario único
- La contraseña se almacena de forma segura (hash + salt)
- Recibo confirmación cuando el registro es exitoso
- Recibo un mensaje de error si el nombre de usuario ya existe

### HU-02: Inicio de Sesión
**Como** usuario registrado  
**Quiero** iniciar sesión con mis credenciales  
**Para** acceder a mi cuenta y continuar jugando

#### Criterios de Aceptación:
- Puedo ingresar mi nombre de usuario y contraseña
- Accedo al lobby después de iniciar sesión correctamente
- Recibo un mensaje de error si las credenciales son incorrectas
- Puedo ver mis créditos y estadísticas después de iniciar sesión

## Módulo de Emparejamiento

### HU-03: Buscar Partida
**Como** jugador en el lobby  
**Quiero** poder buscar una partida contra otro jugador  
**Para** jugar al Piedra, Papel, Tijera, Lagarto, Spock

#### Criterios de Aceptación:
- Existe un botón para buscar partida
- Puedo ver el estado de búsqueda (buscando oponente)
- Recibo una notificación cuando se encuentra un oponente
- Puedo cancelar la búsqueda de partida

### HU-04: Emparejamiento con Oponente
**Como** jugador en búsqueda de partida  
**Quiero** ser emparejado con otro jugador disponible  
**Para** comenzar una partida

#### Criterios de Aceptación:
- El sistema me empareja con otro jugador que también está en búsqueda
- Recibo información sobre mi oponente (nombre de usuario)
- La partida comienza automáticamente después del emparejamiento
- Se me asigna un conjunto aleatorio de imágenes para la partida

## Módulo de Apuestas

### HU-05: Proponer Apuesta
**Como** ganador de la última partida  
**Quiero** proponer una cantidad para apostar  
**Para** aumentar la emoción del juego

#### Criterios de Aceptación:
- Puedo ver mis créditos disponibles
- Puedo especificar una cantidad para apostar
- No puedo apostar más créditos de los que tengo
- Mi propuesta se envía al oponente

### HU-06: Responder a Propuesta de Apuesta
**Como** jugador retador  
**Quiero** poder aceptar o rechazar una propuesta de apuesta  
**Para** decidir si quiero arriesgar mis créditos

#### Criterios de Aceptación:
- Puedo ver la cantidad propuesta para apostar
- Tengo botones para aceptar o rechazar la apuesta
- Si acepto, la partida comienza con la apuesta establecida
- Si rechazo, la partida comienza sin apuesta

## Módulo de Partida

### HU-07: Iniciar Partida
**Como** jugador emparejado  
**Quiero** que la partida comience con un sonido de cuenta regresiva  
**Para** prepararme para hacer mi selección

#### Criterios de Aceptación:
- Escucho un sonido de cuenta regresiva al iniciar la partida
- Veo una animación o indicador visual de la cuenta regresiva
- Las opciones de selección aparecen cuando termina la cuenta regresiva
- Puedo ver el conjunto específico de imágenes asignado a esta partida

### HU-08: Seleccionar Jugada
**Como** jugador en una partida activa  
**Quiero** seleccionar entre piedra, papel, tijera, lagarto o Spock  
**Para** intentar ganar a mi oponente

#### Criterios de Aceptación:
- Veo las cinco opciones disponibles con sus respectivas imágenes
- Puedo seleccionar una opción haciendo clic en ella
- Mi selección queda marcada visualmente
- Mi selección no es visible para mi oponente hasta que ambos hayamos elegido

### HU-09: Ver Resultados de la Partida
**Como** jugador que ha realizado su selección  
**Quiero** ver el resultado de la partida  
**Para** saber si he ganado, perdido o empatado

#### Criterios de Aceptación:
- Después de que ambos jugadores seleccionan, se revelan las elecciones
- Veo mi selección y la de mi oponente
- Se muestra claramente el resultado (victoria, derrota o empate)
- Escucho un sonido correspondiente al resultado
- Se muestra la regla aplicada (ej. "Papel cubre Piedra")

### HU-10: Transferencia de Créditos
**Como** ganador de una partida con apuesta  
**Quiero** recibir los créditos apostados  
**Para** aumentar mi balance de créditos

#### Criterios de Aceptación:
- Si gano, veo cómo aumentan mis créditos
- Si pierdo, veo cómo disminuyen mis créditos
- El cambio en los créditos se muestra claramente
- Se actualiza mi balance total

## Módulo de Ranking y Estadísticas

### HU-11: Consultar Historial de Partidas
**Como** usuario registrado  
**Quiero** poder ver mi historial de partidas  
**Para** conocer mi desempeño

#### Criterios de Aceptación:
- Puedo acceder a una pantalla de historial desde el menú principal
- Veo la lista de mis partidas con fecha, oponente y resultado
- Puedo ver las apuestas realizadas en cada partida
- La información se muestra en orden cronológico inverso

### HU-12: Consultar Tabla de Clasificación
**Como** usuario registrado  
**Quiero** ver la tabla de clasificación  
**Para** conocer mi posición respecto a otros jugadores

#### Criterios de Aceptación:
- Puedo acceder a la tabla de clasificación desde el menú principal
- La tabla muestra los jugadores ordenados por victorias o créditos
- Puedo ver mi posición resaltada en la tabla
- Se muestran estadísticas relevantes (victorias, partidas jugadas, etc.)

## Módulo de Configuración y Preferencias

### HU-13: Gestionar Sonidos del Juego
**Como** usuario del juego  
**Quiero** poder activar o desactivar los sonidos  
**Para** personalizar mi experiencia de juego

#### Criterios de Aceptación:
- Existe una sección de configuración accesible
- Puedo activar/desactivar todos los sonidos
- Los cambios se aplican inmediatamente
- La configuración se mantiene entre sesiones

### HU-14: Visualizar Conjuntos de Imágenes
**Como** usuario del juego  
**Quiero** poder ver los diferentes conjuntos de imágenes disponibles  
**Para** conocer las variantes visuales del juego

#### Criterios de Aceptación:
- Puedo acceder a una galería de conjuntos de imágenes
- Veo miniaturas de cada conjunto (clásico, futurista, medieval)
- Cada conjunto muestra las cinco opciones (piedra, papel, tijera, lagarto, Spock)
- Se muestra una descripción o nombre para cada conjunto

## Módulo de Assets Visuales

### HU-15: Disfrutar de Variedad Visual
**Como** jugador frecuente  
**Quiero** experimentar diferentes conjuntos de imágenes en cada partida  
**Para** mantener el juego fresco y visualmente interesante

#### Criterios de Aceptación:
- Cada nueva partida presenta un conjunto de imágenes aleatorio (clásico, futurista o medieval)
- Las imágenes son consistentes dentro de una misma partida
- Puedo distinguir claramente las diferentes opciones independientemente del conjunto usado
- La descripción de cada opción permanece visible para entender sus reglas

### HU-16: Visualizar Animaciones de Resultado
**Como** jugador de una partida  
**Quiero** ver animaciones que ilustren el resultado de la partida  
**Para** entender visualmente por qué gané o perdí

#### Criterios de Aceptación:
- Hay una animación visual que ilustra la regla aplicada (ej. tijeras cortando papel)
- La animación es coherente con el conjunto de imágenes de la partida
- La animación es breve pero clara
- Hay un texto explicativo junto con la animación

### HU-17: Personalizar la Interfaz
**Como** usuario del juego  
**Quiero** personalizar aspectos visuales de la interfaz  
**Para** adaptar la experiencia a mis preferencias

#### Criterios de Aceptación:
- Puedo ajustar el tamaño de las imágenes en la selección
- Puedo cambiar entre tema claro y oscuro
- Mis preferencias se guardan para futuras sesiones
- Los cambios se aplican inmediatamente

## Módulo de Seguridad

### HU-18: Conexión Segura con el Servidor
**Como** usuario del juego  
**Quiero** que mi conexión con el servidor sea segura  
**Para** proteger mis datos y evitar trampas

#### Criterios de Aceptación:
- La comunicación con el servidor está cifrada mediante SSL/TLS
- Recibo una notificación si la conexión no es segura
- Puedo ver un indicador de conexión segura en la interfaz
- Mis credenciales se transmiten de forma segura

### HU-19: Protección contra Desconexiones
**Como** jugador en una partida activa  
**Quiero** que el sistema maneje adecuadamente las desconexiones  
**Para** no perder créditos injustamente

#### Criterios de Aceptación:
- Si mi oponente se desconecta, se me notifica
- La partida se cancela sin pérdida de créditos si no había apuesta
- Si había apuesta y estábamos en la fase de selección, se devuelven los créditos
- Tengo la opción de buscar una nueva partida

### HU-20: Prevención de Trampas
**Como** jugador honesto  
**Quiero** que el sistema prevenga formas de hacer trampa  
**Para** garantizar la integridad del juego

#### Criterios de Aceptación:
- Las selecciones de los jugadores se procesan en el servidor, no en el cliente
- El servidor valida el tiempo de respuesta para evitar ventajas injustas
- No es posible conocer la selección del oponente antes de hacer la propia
- Se implementan medidas contra bots o scripts automatizados

## Módulo de Interacción Social

### HU-21: Chat Básico en Partida
**Como** jugador en una partida activa  
**Quiero** poder enviar mensajes predefinidos a mi oponente  
**Para** añadir un elemento social a la experiencia

#### Criterios de Aceptación:
- Puedo seleccionar mensajes predefinidos amistosos durante la partida
- Veo los mensajes enviados por mi oponente
- Los mensajes no interfieren con la jugabilidad
- Puedo desactivar los mensajes si lo deseo

### HU-22: Añadir Jugadores como Amigos
**Como** usuario del juego  
**Quiero** poder añadir a otros jugadores como amigos  
**Para** jugar con ellos en el futuro

#### Criterios de Aceptación:
- Después de una partida, tengo la opción de añadir al oponente como amigo
- Puedo ver una lista de mis amigos en el lobby
- Puedo invitar directamente a mis amigos a jugar
- Puedo eliminar amigos de mi lista

### HU-23: Desafío Directo
**Como** usuario con amigos en el juego  
**Quiero** poder desafiar directamente a un amigo  
**Para** jugar específicamente con esa persona

#### Criterios de Aceptación:
- Puedo seleccionar a un amigo conectado y enviarle un desafío
- El amigo recibe una notificación del desafío
- El amigo puede aceptar o rechazar el desafío
- Si acepta, comenzamos una partida privada

## Módulo de Características Avanzadas

### HU-24: Torneos Automáticos
**Como** jugador competitivo  
**Quiero** participar en torneos automáticos  
**Para** competir con múltiples jugadores

#### Criterios de Aceptación:
- Recibo notificaciones cuando hay torneos programados
- Puedo inscribirme en torneos con una cantidad específica de créditos
- El sistema organiza automáticamente las rondas y emparejamientos
- Recibo premios basados en mi posición final en el torneo

### HU-25: Misiones Diarias
**Como** jugador regular  
**Quiero** tener misiones diarias  
**Para** obtener recompensas adicionales y tener objetivos

#### Criterios de Aceptación:
- Cada día se generan nuevas misiones aleatorias (ej. "Gana 3 partidas con Piedra")
- Puedo ver mi progreso en cada misión
- Al completar misiones, recibo créditos adicionales
- Las misiones incentivan a usar diferentes estrategias o elementos

### HU-26: Sistema de Niveles
**Como** usuario del juego  
**Quiero** subir de nivel al ganar partidas  
**Para** tener una sensación de progresión

#### Criterios de Aceptación:
- Gano puntos de experiencia al jugar partidas
- Los puntos acumulados determinan mi nivel
- Mi nivel se muestra junto a mi nombre de usuario
- Desbloqueo nuevos elementos visuales al subir de nivel

### HU-27: Estadísticas Detalladas
**Como** jugador analítico  
**Quiero** acceder a estadísticas detalladas de mi desempeño  
**Para** mejorar mi estrategia

#### Criterios de Aceptación:
- Puedo ver porcentajes de victoria con cada elemento (piedra, papel, etc.)
- Veo estadísticas por oponente o globales
- Las estadísticas incluyen gráficos visuales
- Puedo filtrar estadísticas por período de tiempo

## Módulo de Experiencia Responsiva

### HU-28: Interfaz Adaptativa
**Como** usuario del juego  
**Quiero** que la interfaz se adapte a diferentes tamaños de pantalla  
**Para** poder jugar cómodamente desde cualquier dispositivo

#### Criterios de Aceptación:
- La interfaz se reorganiza automáticamente en pantallas pequeñas
- Los elementos táctiles son suficientemente grandes en dispositivos móviles
- La experiencia es consistente independientemente del dispositivo
- No se pierde funcionalidad en pantallas pequeñas

### HU-29: Modo Offline para Práctica
**Como** usuario con conectividad inestable  
**Quiero** poder practicar contra la IA cuando estoy offline  
**Para** mejorar mis habilidades sin necesidad de conexión

#### Criterios de Aceptación:
- Puedo seleccionar un modo de práctica contra la IA
- La IA tiene diferentes niveles de dificultad
- Puedo practicar sin gastar o ganar créditos reales
- El juego me notifica cuando recupero conexión

## Módulo de Accesibilidad

### HU-30: Opciones de Accesibilidad
**Como** usuario con necesidades especiales  
**Quiero** configurar opciones de accesibilidad  
**Para** poder disfrutar del juego a pesar de mis limitaciones

#### Criterios de Aceptación:
- Puedo activar un modo de alto contraste
- Hay opciones para aumentar el tamaño del texto
- Las señales visuales están acompañadas de señales sonoras
- El juego es compatible con lectores de pantalla

### HU-31: Tutorial Interactivo
**Como** nuevo usuario  
**Quiero** un tutorial que explique las reglas y la interfaz  
**Para** aprender a jugar rápidamente

#### Criterios de Aceptación:
- El tutorial se muestra automáticamente en el primer inicio de sesión
- Explica paso a paso las reglas del juego
- Incluye ejemplos interactivos de cada combinación ganadora
- Puedo saltar o repetir el tutorial cuando quiera

## Módulo de Administración

### HU-32: Panel de Administrador
**Como** administrador del sistema  
**Quiero** un panel de control  
**Para** gestionar usuarios, partidas y configuraciones

#### Criterios de Aceptación:
- Puedo ver la lista de todos los usuarios registrados
- Puedo suspender cuentas que violen las normas
- Tengo acceso a estadísticas generales del sistema
- Puedo ajustar parámetros como cantidades iniciales de crédito

### HU-33: Gestión de Conjuntos de Imágenes
**Como** administrador del sistema  
**Quiero** poder añadir nuevos conjuntos de imágenes  
**Para** mantener el juego actualizado y atractivo

#### Criterios de Aceptación:
- Existe una interfaz para cargar nuevas imágenes
- Puedo asignar cada imagen a su categoría correspondiente
- Puedo activar o desactivar conjuntos de imágenes
- Los cambios se reflejan en la configuración de assets del cliente

### HU-34: Monitoreo del Sistema
**Como** administrador del sistema  
**Quiero** monitorear el rendimiento y actividad del servidor  
**Para** garantizar una experiencia fluida para los usuarios

#### Criterios de Aceptación:
- Puedo ver métricas en tiempo real (usuarios conectados, partidas activas)
- Recibo alertas sobre problemas potenciales
- Tengo acceso a logs detallados
- Puedo reiniciar servicios específicos sin afectar todo el sistema

### HU-35: Respaldo y Recuperación
**Como** administrador del sistema  
**Quiero** programar respaldos automáticos  
**Para** proteger los datos contra pérdidas

#### Criterios de Aceptación:
- El sistema realiza respaldos automáticos de las bases de datos JSON
- Puedo restaurar desde un respaldo en caso de problemas
- Los respaldos incluyen historial de partidas y cuentas de usuario
- Recibo confirmación por correo electrónico cuando se completa un respaldo
