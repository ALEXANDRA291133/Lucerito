# Lucerito - Sistema de Gestión de Inventario Cosmético e IA Local

**Lucerito** es un sistema de información web desarrollado en **Django 5.x** diseñado para administrar el inventario de una tienda de productos de belleza y cosméticos. Incluye un módulo CRUD completo, reportes analíticos basados en patrones de diseño (_Strategy_ y _Factory_), y un chatbot interactivo integrado con un modelo de Inteligencia Artificial local a través de **Ollama**.

---

## 📋 Características Principales

- **Gestión de Inventario (CRUD):** Registro, consulta, edición y eliminación de cosméticos con validaciones de unicidad de SKU/Código y valores no negativos.
- **Reportes Analíticos:** Generación de reportes como productos con stock crítico, cosméticos de mayor/menor precio y desgloses por categoría.
- **Chatbot con IA Local:** Integración con **Ollama** (`qwen2.5:1.5b`) mediante RAG simplificado para responder preguntas sobre el catálogo real sin depender de servicios en la nube.
- **Resiliencia y Seguridad:** Control estricto del prompt del sistema para evitar alucinaciones y manejo de errores cuando el servicio de IA no está disponible.
- **Arquitectura Limpia:** Aplicación de patrones de diseño, separación por aplicaciones y cobertura de pruebas unitarias.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.11+
- **Framework Web:** Django 5.x
- **Base de Datos:** SQLite
- **Motor de IA Local:** Ollama (`qwen2.5:1.5b` / `lucerito-bot`)
- **Librerías Auxiliares:** `requests`, `python-dotenv`
- **Estilos:** HTML5, CSS3, Bootstrap 5

---

## 🚀 Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu sistema (preferentemente Debian 12 / Linux):

1. **Python 3.11** o superior.
2. **Pip** (gestor de paquetes de Python).
3. **Ollama** (para la ejecución del modelo de IA local).

---

## ⚙️ Instalación y Configuración

### 1. Clonar o descomprimir el repositorio

```bash
git clone <url-del-repositorio>
cd Lucerito
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux / macOS
# venv\Scripts\activate  # En Windows
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copia el archivo `.env.example` a `.env` y configura los valores requeridos:

```bash
cp .env.example .env
```

Ejemplo de archivo `.env`:

```env
SECRET_KEY=django-insecure-lucerito-secret-key-change-in-production
DEBUG=True
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5:1.5b
```

---

## 🦙 Configuración de Ollama (IA Local)

### 1. Instalar Ollama

En Linux / Debian:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Descargar el modelo de IA

```bash
ollama pull qwen2.5:1.5b
```

### 3. (Opcional) Crear el modelo personalizado Lucerito

Si deseas usar el prompt ajustado definido en el `Modelfile`:

```bash
cd ollama
bash build_model.sh
cd ..
```

_Asegúrate de cambiar `OLLAMA_MODEL=lucerito-bot` en tu archivo `.env` si ejecutas este paso._

---

## 🗄️ Base de Datos y Servidor de Desarrollo

### 1. Aplicar las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Cargar datos iniciales de prueba (Fixtures)

Para contar con productos cosméticos precargados:

```bash
python manage.py loaddata inventario/fixtures/productos_iniciales.json
```

### 3. Crear un superusuario para el panel de administración

```bash
python manage.py createsuperuser
```

### 4. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El sistema estará accesible en: `http://127.0.2.1:8000/` o `http://localhost:8000/`.

---

## 🧪 Ejecución de Pruebas Unitarias

Para verificar la integridad del modelo de datos y las estrategias de reportes, ejecuta:

```bash
python manage.py test inventario
```

---
