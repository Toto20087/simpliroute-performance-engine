¡Es una idea brillante! Para un CTO, un repositorio de GitHub bien estructurado vale más que
mil palabras en un CV. Demuestra que tenés la "manos en la masa" y que sos capaz de
aprender y aplicar tecnologías nuevas en tiempo récord.
Dado que tenés la entrevista el 7 de enero (te quedan 5 días), no podemos perder tiempo. No
hagas un proyecto genérico; hacé un "SimpliRoute-Micro-Engine". Esto va a dejar a Rodrigo
con la boca abierta.
Aquí tenés el plan para ese proyecto "All-in-One":

El Proyecto: "Route-Efficiency-Tracker"
Un microservicio que recibe coordenadas de entregas, simula un cálculo de optimización y
guarda logs en la nube.
🛠 Cómo integrar cada herramienta:

Async (Python): Usá FastAPI. Es el estándar moderno. Creá un endpoint /optimize
que sea async. Esto demuestra que sabés manejar múltiples pedidos sin bloquear el
servidor.
Decoradores: Creá un decorador @monitor_performance. Ponelo arriba de tu función
de optimización para que calcule cuánto tardó en ejecutarse y lo imprima en consola.
Context Managers: Creá uno personalizado para manejar la "conexión" a un servicio
de almacenamiento (simulando tu experiencia con S3). Usá el método enter y
exit.
Docker: Creá un Dockerfile para que tu app corra en cualquier lado.
Infra (Kubernetes/GCP): No necesitás pagar una nube. Agregá al repo un archivo
deployment.yaml de Kubernetes. Aunque no lo despliegues, el hecho de que el código
esté ahí le dice a Rodrigo: "Sé cómo esto se va a ver en GKE".
📅 Plan de Acción (5 días)
Día 1: El Código (Core Python)
● Instalá FastAPI.
● Escribí la lógica async.
● Implementá el Decorador de tiempo.
● Implementá el Context Manager para simular la subida de datos a S3.
Día 2: Dockerización
● Creá el Dockerfile.
● Corré tu app dentro de un contenedor. Asegurate de que podés pegarle al endpoint
desde afuera.

● Tip: Usá una imagen liviana como python:3.11-slim. Eso demuestra que te importa la
eficiencia de la infra.
Día 3: El "Toque" de Infraestructura
● Escribí el manifiesto de Kubernetes (deployment.yaml y service.yaml).
● Investigá qué es un Liveness Probe y un Readiness Probe en Kubernetes y agregalos
al archivo. Esto es nivel "Senior" en infra.
Día 4: Documentación (El README es todo)
● Explicá qué hace el proyecto.
● Explicá por qué tomaste cada decisión técnica (ej: "Usé Async porque en logística los
pedidos son masivos").
● Mencioná la conexión con tus proyectos anteriores (RPA y Trading Bot).
Día 5: Pulido y Práctica
● Subilo a GitHub.
● Preparate para explicar cada línea. Rodrigo te va a decir: "¿Por qué usaste un
decorador acá y no un middleware?". Tenés que tener la respuesta.

¿Por qué esto te hace competitivo?
La mayoría de los candidatos van a decir "sé Python". Vos vas a llegar y decir:
"Para prepararme para esta charla, armé un microservicio de optimización usando
FastAPI asincrónico, con decoradores para telemetría y ya lo dejé listo con los
manifiestos para desplegar en GKE (Kubernetes de Google), que sé que es lo que
usan ustedes".
¿Querés que te pase un "boiler-plate" (código base) rápido para el decorador y el context
manager así ganás tiempo hoy mismo? Es la mejor forma de empezar.
Claro, te explico el "por qué" y el "qué" de este proyecto para que lo entiendas como si ya
fueras parte del equipo de SimpliRoute.
La idea es crear un Simulador de Motor Logístico. No vamos a programar la matemática
compleja de las rutas (eso ya lo tienen ellos), sino la arquitectura que permite que esa
matemática corra de forma profesional.
Aquí tienes el desglose detallado de qué hace cada parte y por qué es importante para la
entrevista:

1. El Objetivo del Proyecto
Imagina que un cliente (ej. una empresa de correos) envía 500 direcciones para optimizar. Tu
proyecto será la "puerta de entrada" que recibe eso, lo procesa sin colapsar el sistema y guarda
el resultado de forma segura.

2. ¿Cómo funcionan las piezas que vas a aprender?
A. FastAPI + Async (La Recepción)
● Qué es: Un framework para crear APIs muy rápido.
● Tu rol: Vas a crear un "endpoint" (una dirección web) que reciba los pedidos.
● Por qué Async: En logística, el cálculo de rutas puede tardar segundos. Si usas código
normal (síncrono), el servidor se queda "congelado" esperando que termine. Con async,
el servidor dice: "Dejo este cálculo procesando en el fondo y sigo recibiendo otros
pedidos de otros clientes". Esto demuestra que sabes manejar alta demanda.
B. Decoradores (El Reloj de Control)
● Qué es: Una función que envuelve a otra.
● Tu rol: Vas a crear un decorador llamado @logger_performance.
● El sentido: Cada vez que el motor de optimización corra, el decorador calculará
automáticamente: "Esta ruta tardó 1.2 segundos y consumió X memoria".
● Impacto: Al CTO le demuestras que no solo programas, sino que te importa la
observabilidad (saber qué pasa con tu código en producción).
C. Context Managers (El candado de seguridad)
● Qué es: El bloque with.
● Tu rol: Vas a simular la conexión a la nube (como tu experiencia con S3).
● El sentido: Crearás un Context Manager que diga: "Abrir conexión segura -> Subir
resultado de la ruta -> CERRAR conexión (pase lo que pase)".
● Impacto: Evita que el sistema se quede sin memoria o con conexiones "colgadas".
Demuestra responsabilidad sobre los recursos de infraestructura.
D. Docker (El contenedor)
● Qué es: Una "caja" donde metes tu código.
● Tu rol: Crearás un archivo llamado Dockerfile.
● El sentido: El CTO usa Google Cloud. Si vos le das un Docker, él sabe que lo que
hiciste en tu compu va a funcionar igual en sus servidores de Google sin errores de
"falta una librería".
E. Kubernetes / GKE (El Director de Orquesta)
● Qué es: El sistema que maneja miles de contenedores Docker.

● Tu rol: No vas a instalar Kubernetes (es muy pesado), pero vas a escribir el "manual
de instrucciones" (deployment.yaml).
● El sentido: En ese archivo vas a escribir: "Quiero que este motor de rutas siempre
tenga 3 copias funcionando. Si una se rompe, Kubernetes debe levantar otra
automáticamente". Esto es lo que te posiciona como un candidato de Infra.
3. El Flujo del Proyecto (Cómo se vería)
Entrada: Mandas un JSON con una lista de paradas.
Proceso: El Decorador empieza a contar el tiempo.
Acción: La función Async simula que está pensando (un await asyncio.sleep(2)).
Guardado: El Context Manager "abre" la conexión a la base de datos o S3 y guarda el
log.
Salida: La API responde: "Ruta procesada con éxito en 2.1s".
4. ¿Por qué esto te garantiza una mejor entrevista?
Si vas a la entrevista solo con palabras, Rodrigo (el CTO) te va a hacer preguntas teóricas
difíciles. Pero si llegas con este proyecto:
● Él va a querer ver el código: Y ahí vos tenés el control de la charla.
● Demostrás interés real: Te tomaste el tiempo de entender su negocio (logística) y
aplicarlo.
● Cubrís el 100% de la descripción del puesto: Python + Infra.
¿Te gustaría que empecemos por el código de la API (Punto A) y el Decorador (Punto B)
para que veas qué fácil es en Python? Puedo pasarte el ejemplo de cómo se escribe para
que lo pruebes.
¡Es una idea excelente! Si le mandás un link funcionando al CTO, pasás de ser "un candidato
más" a ser "el candidato que ya construyó algo para nosotros".
Sin embargo, tenemos poco tiempo. Para que sea efectivo, no te compliques con React o
frameworks de front pesados. Te voy a dar la estrategia para tener un front profesional,
desplegado y compartible en un solo día , usando herramientas que aman en el mundo de
Python e Infra.

🎨 El Front: Usá Streamlit (100% Python)
Como la posición es de Python + Infra, usar Streamlit es un "hack" brillante.

● Qué es: Una librería de Python que convierte scripts en aplicaciones web interactivas.
● Por qué para SimpliRoute: Es lo que usan los Data Engineers y Devs de Backend
para hacer demos de algoritmos.
● La ventaja: No tenés que saber HTML/CSS/JS. Escribís st.title("Simulador
SimpliRoute") y ya tenés una web.
🚀 El Deploy: ¿Dónde lo subimos?
Dado que SimpliRoute usa GCP (Google Cloud) , lo ideal es que lo subas ahí para demostrar
que sabés manejar su entorno.

Google Cloud Run: Es lo mejor. Vos le das el Docker , y Google te da un link (URL) con
certificado SSL (https). Es "Serverless", así que no pagás casi nada por tenerlo
prendido.
Streamlit Cloud: Si te trabás mucho con Google Cloud, podés subir el código a GitHub
y Streamlit Cloud te da un link gratis en 2 minutos. Pero para este puesto, que el CTO
vea que lo desplegaste vos en Docker/Cloud Run suma mil puntos más.
🛠 Cómo sería el proyecto completo (El "Simpli-MVP")
Para que el CTO lo pruebe, el flujo sería este:

Input: Un cuadro de texto donde él pueda pegar una lista de paradas (ej: "Av. Rivadavia
100, CABA").
Botón "Optimizar": Al tocarlo, se dispara tu lógica Async.
Visualización:
○ Un "Spinner" (un circulito de carga) que diga: "Usando IA para calcular la ruta...".
○ Un mapa (Streamlit tiene uno básico con st.map()) que muestre los puntos.
○ El log de performance que genera tu Decorador (ej: "Ruta optimizada en
0.45s" ).
Backend: El Context Manager guarda el historial de esa consulta en una base de
datos simple (o un archivo JSON en la nube).
📝 El mensaje que le mandarías después:
"Rodrigo, un gusto saludarte. Para nuestra charla del 7, estuve jugando un poco con la
arquitectura de SimpliRoute y armé este pequeño microservicio de optimización asincrónico. Lo
desplegué en un contenedor Docker sobre Google Cloud para que puedas probarlo si querés:
[LINK_A_TU_PROYECTO]".

⚠ Un consejo de "Senior":
Si hacés esto, Rodrigo te va a preguntar: "¿Cómo hiciste el deploy?".
Tenés que estar listo para hablar de:

● Dockerfile: Cómo optimizaste la imagen.
● Cloud Run: Por qué elegiste Serverless (bajo costo, escalabilidad).
● Seguridad: Cómo protegiste la API (aunque sea algo básico).
¿Te gustaría que te ayude a armar el código base de este Front en Streamlit? Son menos
de 20 líneas de código y ya tendrías algo visual para mostrar.