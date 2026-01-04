# 🚀 El Viaje del Proyecto: SimpliRoute Performance Engine

## ⏱️ Resumen de Inversión de Tiempo
**Esfuerzo Total Estimado**: ~3 Días de Trabajo Full-Time (Comprimido en un Sprint Intensivo)

| Fase | Duración | Descripción |
| :--- | :--- | :--- |
| **Arquitectura del Sistema** | 4 Horas | Diseño del patrón de Microservicios, contenedorización con Docker y estrategia de despliegue en Kubernetes. |
| **Desarrollo Backend** | 8 Horas | Construcción de la aplicación FastAPI, modelos Pydantic y el patrón "Estrategia" modular para el solucionador. |
| **Implementación del Algoritmo** | 6 Horas | Implementación del solucionador **Google OR-Tools**, matemática de distancia Haversine y lógica VRP (N-Node TSP). |
| **Visualización Frontend** | 4 Horas | Creación del dashboard en Streamlit e integración del **Mapa 3D PyDeck** para visualización de rutas. |
| **DevOps y Testing** | 4 Horas | Optimización de Dockerfile, manifiestos de Kubernetes y pruebas de integración. |

---

## 🧠 Tópicos y Tecnologías Dominadas

### 1. Ingeniería Python Avanzada
*   **FastAPI & AsyncIO**: Implementación de endpoints asíncronos de alto rendimiento.
*   **Pydantic V2**: Validación estricta de datos y definición de esquemas.
*   **Type Hinting**: Tipado de nivel profesional para mantenibilidad.

### 2. Optimización Combinatoria ("Matemática Dura")
*   **Problema de Enrutamiento de Vehículos (VRP)**: Comprensión de la complejidad para encontrar caminos óptimos con restricciones (Capacidad, Ventanas de Tiempo).
*   **Google OR-Tools**: Implementación del solucionador de Programación con Restricciones utilizado por gigantes de la industria.
*   **Fórmula Haversine**: Cálculo de distancias de "Círculo Máximo" en una esfera (Tierra) para estimaciones de viaje precisas.

### 3. Visualización Frontend Moderna
*   **Streamlit**: Construcción rápida de dashboards de datos interactivos.
*   **PyDeck (deck.gl)**: Renderizado de capas de datos geoespaciales 3D complejas (PathLayer, ScatterplotLayer) para mapas profesionales.

### 4. Infraestructura Cloud-Native
*   **Docker**: Contenedorización de la aplicación para un contexto de ejecución consistente.
*   **Kubernetes (K8s)**: Definición de Infraestructura Declarativa (Deployments, Services) para capacidades escalables.

### 5. Diseño de Sistemas Resilientes
*   **Estrategias de Fallback**: Diseño de un sistema que se degrada elegantemente de una API Cloud a un Solucionador Local si la red falla.
*   **Observabilidad**: Implementación de Decoradores para registrar tiempo de ejecución y métricas de rendimiento.

---

## 🏆 Desafíos y Soluciones

### Desafío 1: Inestabilidad de API Externa
*   **Problema**: La API VRP externa devolvía errores `500` impredecibles durante las pruebas de carga.
*   **Solución**: Pivotamos a una **Estrategia de Motor Local**. Implementamos Google OR-Tools directamente dentro del microservicio. Esto eliminó la dependencia de red y redujo la latencia a **< 50ms**.

### Desafío 2: Manejo Dinámico del Depósito
*   **Problema**: El solucionador necesitaba saber *exactamente* dónde comenzaba el camión, pero la entrada del usuario no estaba estructurada.
*   **Solución**: Refactorizamos el modelo de datos para soportar una **Definición Explícita del Depósito** en el payload JSON, fusionándolo inteligentemente con las paradas de entrega antes de resolver.

### Desafío 3: Estimación de Tiempo Real
*   **Problema**: Conocer la distancia no era suficiente; necesitábamos saber *cuánto tiempo* tomaría la entrega.
*   **Solución**: Implementamos una capa de estimación basada en física (`Tiempo = Distancia / Velocidad Promedio`), asumiendo un promedio urbano de 25km/h, proporcionando métricas accionables al usuario.

---

## 💼 Por Qué Esto Importa (La Perspectiva "Senior")
Este proyecto demuestra más que solo código; demuestra **Madurez Ingenieril**.
1.  **Funciona offline**: No es solo un wrapper de una API; es un motor independiente.
2.  **Es escalable**: La arquitectura (K8s + Async) lo deja listo cargas de producción.
3.  **Aporta valor**: La visualización 3D traduce matemática compleja en insights de negocio.
