# 📑 Reporte Técnico: SimpliRoute Performance Engine

## 📊 Resumen Ejecutivo
Desarrollo de un motor de optimización de rutas de alto rendimiento, diseñado para demostrar capacidades de ingeniería Full Stack Senior. El sistema resuelve el problema VRP (Vehicle Routing Problem) utilizando una arquitectura de microservicios asíncrona y una interfaz moderna.

## 🎯 Motivación de Aprendizaje (Learning Compass)
Este proyecto nació de la iniciativa personal de **alinear mis habilidades técnicas con el stack real que utiliza SimpliRoute** hoy en día.

El objetivo de construir esta demo fue enfrentarme a la realidad de las herramientas de producción. Este proceso me permitió identificar brechas de conocimiento (Kubernetes, Celery, Redis) y me exigió invertir tiempo de estudio dedicado para entenderlas desde cero e implementarlas correctamente. Más que una demostración, fue un **ejercicio intensivo de auto-aprendizaje y adaptación tecnológica**.

---

## 🏆 Desafíos Técnicos y Curva de Aprendizaje

### 1. Cuello de Botella en Procesamiento (Arquitectura Asíncrona)
*   **Desafío**: El cálculo de rutas optimizadas es intensivo en CPU. Al implementarlo inicialmente, bloqueaba el servidor API, impidiendo manejar múltiples usuarios simultáneamente.
*   **Investigación y Solución**: Nunca había utilizado **Celery** ni **Redis**. Investigué estos patrones de arquitectura asíncrona ("Task Queues") e implementé un sistema donde el Worker procesa el cálculo en segundo plano mientras la API responde inmediatamente.

### 2. De Consumidor de API a Creador de Motores (Google OR-Tools)
*   **Bloqueo**: La intención original era consumir la API de SimpliRoute, pero encontré inestabilidad en el endpoint `/optimize` que impedía el avance (Errores 500 recurrentes).
*   **Adaptación**: En lugar de bloquearme, pivoté la estrategia. Investigué soluciones alternativas de optimización matemática y encontré **Google OR-Tools**.
*   **Implementación Profunda**: Tuve que estudiar la matemática detrás de las distancias geoespaciales (**Fórmula del Haversine**) y aplicarla en Python para alimentar la matriz de costos del algoritmo, creando así un motor de enrutamiento propio y funcional. (Obviamente esta solucion es muy basica y no considera nada mas que no sean distancias pero ya que esto no era algo fundamental a aprender, sino que los aprendizajes iban mas por el lado de Python + Infra)

### 3. Infraestructura y Orquestación (Kubernetes)
*   **Desafío**: El requisito de orquestar múltiples contenedores me llevó a una tecnología que desconocía: **Kubernetes**.
*   **Aprendizaje**: Realicé una investigación intensiva sobre qué es, sus componentes (Pods, Services, Deployments) y cómo opera. Aunque para el entregable final opté por Docker Compose/Railway por agilidad, adquirí el conocimiento fundacional para escalar esta arquitectura a un clúster real.

### 4. Visibilidad del Producto (Despliegue en Railway)
*   **Objetivo**: Quería que el CTO pudiera auditar el funcionamiento real del sistema desde su computadora, sin necesidad de clonar el repo.
*   **Solución**: Investigué plataformas de despliegue PaaS y configuré **Railway** para soportar la arquitectura multi-servicio (Frontend + Backend + Worker + Redis), logrando un link público de demostración totalmente funcional.

---

## 🛠️ Stack Tecnológico

### Backend & Datos
*   **FastAPI**: API REST de alto rendimiento.
*   **Google OR-Tools + Haversine**: Motor matemático propio.
*   **Celery + Redis**: Cola de tareas distribuida.

### Frontend
*   **React + Vite**: SPA Moderna.
*   **Tailwind CSS + Shadcn UI**: Diseño de interfaz profesional.
*   **Leaflet**: Mapas interactivos.

### Infraestructura
*   **Docker Compose**: Orquestación local.
*   **Railway**: Despliegue en la nube.
