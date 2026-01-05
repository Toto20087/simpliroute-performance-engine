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
*   **Aprendizaje**: Investigué sus componentes y arquitectura. Implementé una solución completa con **Deployments**, **Services** y **HPA (Horizontal Pod Autoscaler)** para garantizar alta disponibilidad y escalabilidad automática según la carga de CPU.

### 4. Visibilidad del Producto (Despliegue)
*   **Objetivo**: Permitir auditar el funcionamiento real del sistema de forma sencilla.
*   **Solución**: Se configuraron pipelines de despliegue tanto locales (Docker Compose) como escalables (Kubernetes) para demostrar versatilidad.

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
*   **Docker Compose**: Desarrollo local rápido.
*   **Kubernetes (K8s)**: Orquestación escalable para producción.

---

## 🚀 Cómo Ejecutar el Proyecto

A continuación se detallan las dos formas de levantar el proyecto: **Modo Desarrollo (Docker Compose)** y **Modo Producción Escalable (Kubernetes)**.

### 📋 Requisitos Previos (Prerequisites)
*   [Docker Desktop](https://www.docker.com) instalado y corriendo.
*   (Solo para Opción 2) **Kubernetes** habilitado en Docker Desktop.
*   (Solo para Opción 2) `kubectl` instalado (generalmente viene con Docker Desktop).

---

### Opción 1: Inicio Rápido con Docker Compose
*Ideal para desarrollo local, pruebas rápidas y debugging.*

1.  **Clonar el repositorio:**
    ```bash
    git clone <tu-repositorio>
    cd simpliroute-performance-engine
    ```

2.  **Ejecutar el entorno:**
    Este comando construye las imágenes y levanta todos los servicios (Frontend, Backend, Worker, Redis).
    ```bash
    docker-compose up --build
    ```

3.  **Acceder a la aplicación:**
    *   **Frontend Web:** [http://localhost:8501](http://localhost:8501)
    *   **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

4.  **Detener:** Presiona `Ctrl+C` o ejecuta `docker-compose down`.

---

### Opción 2: Despliegue Escalable con Kubernetes
*Ideal para simular un entorno de producción con alta disponibilidad, balanceo de carga y auto-escalado.*

**Nota Importante:** Si usas esta opción, asegúrate de que Docker Compose no esté corriendo (`docker-compose down`) para liberar los puertos.

1.  **Construir las Imágenes Docker:**
    Kubernetes necesita que las imágenes estén creadas y etiquetadas correctamente.
    ```bash
    # Construir imagen del Backend/Worker
    docker build -t simpliroute-engine:v1 -f infra/docker/Dockerfile .

    # Construir imagen del Frontend
    docker build -t simpliroute-frontend:v1 ./src/frontend-react
    ```

2.  **Desplegar en Kubernetes:**
    Este comando crea todos los recursos (Deployments, Services, HPA).
    ```bash
    kubectl apply -f infra/k8s/
    ```

3.  **Verificar el Estado:**
    Comprueba que los pods estén corriendo (Status: `Running`).
    ```bash
    kubectl get pods
    ```

4.  **Acceder a la aplicación:**
    *   **Frontend Web:** [http://localhost:8501](http://localhost:8501) (Puerto expuesto por el LoadBalancer).
    *   **API Docs:** [http://localhost:80/docs](http://localhost:80/docs) (Puerto estándar 80).

5.  **Detener y Limpiar:**
    Para borrar todos los recursos creados en el clúster.
    ```bash
    kubectl delete -f infra/k8s/
    ```

### ✨ Características del Despliegue en Kubernetes
*   **Alta Disponibilidad:** 3 réplicas del Backend corriendo simultáneamente.
*   **Auto-Escalado (HPA):** Si el uso de CPU supera el 50%, el sistema crea automáticamente más réplicas (hasta 10) para soportar el tráfico.
*   **Load Balancing:** Distribución inteligente del tráfico entre las réplicas disponibles.
