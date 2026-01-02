He investigado la documentación oficial de SimpliRoute y he extraído los puntos clave para que puedas integrar tu microservicio de forma profesional. La API se divide principalmente en dos "caminos" o casos de uso: integración de negocio y optimización inteligente.

Para tu proyecto **`simpliroute-performance-engine`**, estos son los endpoints esenciales:

### 1. Autenticación (Paso Obligatorio)

Antes de llamar a cualquier servicio, debés validar tu token.

* **Endpoint:** `GET https://api.simpliroute.com/v1/accounts/me/`
* **Header:** `Authorization: Token TU_API_KEY`
* **Tip:** Si no tenés cuenta, podés crear una de prueba por 14 días en su web para obtener esta Key.

---

### 2. El "Cerebro": API de Optimización

Este es el endpoint más importante para tu simulación, ya que es el que recibe los datos y devuelve las rutas calculadas.

* **Endpoint:** `POST http://optimizer.simpliroute.com/vrp/optimize/sync`
* **Uso:** Aquí enviás un JSON con dos listas principales:
* **`vehicles`**: Definís la capacidad, el inicio (`shift_start`) y fin de turno.
* **`nodes`**: Son las paradas (direcciones). Los campos obligatorios son `lat`, `lon`, y `ident` (nombre del punto).


* **Ejemplo de flujo:** Es ideal para tu lógica `async`, ya que podés enviar los nodos y esperar la respuesta estructurada con el orden de las visitas.

---

### 3. Gestión de Visitas (Si querés persistencia)

Si además de optimizar querés que las visitas queden guardadas en el panel de SimpliRoute:

* **Crear Visita:** `POST https://api.simpliroute.com/v1/routes/visits/`
* **Campos Obligatorios:**
* `title`: Nombre del cliente o local.
* `address`: Dirección (formato Google Maps).
* `planned_date`: Fecha de la visita (`YYYY-MM-DD`).



---

### 4. Seguimiento de Rutas y Planes

Una vez que la optimización termina, podés consultar o crear las rutas finales:

* **Listar vehículos con rutas:** `GET https://api.simpliroute.com/v1/plans/{planned_date}/vehicles/`
* **Crear un Plan:** `POST https://api.simpliroute.com/v1/plans/plans/` (Sirve para agrupar un conjunto de rutas bajo un mismo nombre, por ejemplo: "Reparto Lunes").

---

### Estrategia Técnica para tu Repo:

1. **En tu código:** Usá el endpoint de **Optimización Sync** (`/vrp/optimize/sync`). Es el más "limpio" para un desarrollador porque le pasás datos crudos y te devuelve la solución sin necesidad de haber creado objetos previos en su base de datos.
2. **Decorador de Performance:** Aplicá tu decorador `@monitor_performance` justamente en la función que llama a este endpoint. Así podés mostrar en tu Front: *"Llamada a SimpliRoute Optimizer exitosa en 0.8s"*.
3. **Manejo de Errores:** La documentación especifica que usan códigos HTTP estándar. Prepará tu código para manejar un `401` (Token inválido) o un `400` (Error en el formato del JSON).

**¿Qué te parece si empezamos armando el cliente de Python para pegarle al endpoint de Optimización?** Puedo darte la estructura del JSON que espera ese POST.