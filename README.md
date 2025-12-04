# Secuencia Didáctica: La Derivada y la Densidad Mineral Ósea

Esta plataforma web es una herramienta educativa diseñada para facilitar la enseñanza y el aprendizaje del concepto matemático de la **Derivada**, utilizando como contexto de aplicación la **Densidad Mineral Ósea (DMO)**.

El sistema gestiona una secuencia didáctica interactiva donde los estudiantes pueden aprender, colaborar y ser evaluados, mientras que el tutor mantiene el control total sobre el contenido y las evaluaciones.

## 🚀 Funcionalidades Principales

### 1. Gestión de Contenido (Rol de Tutor)
* **Creación de Actividades:** El tutor puede diseñar la secuencia didáctica paso a paso.
* **Edición Exclusiva:** Solo los usuarios con permisos de *Staff/Administrador* pueden crear, editar o eliminar actividades y componentes.
* **Editor de Texto Enriquecido:** Integración con CKEditor para incluir fórmulas matemáticas, imágenes y formato avanzado en las descripciones.

### 2. Herramientas de Evaluación y Participación
* **Exámenes y Cuestionarios:** Soportan preguntas tanto **abiertas** como de **opción múltiple**.
* **Formularios:** Para la recolección de datos dentro de la secuencia.
* **Foros de Discusión:** Espacios dedicados para que los alumnos participen, debatan y resuelvan dudas sobre los temas vistos.

### 3. 🆕 Glosario Global Flotante
* **Acceso Universal:** Un botón flotante ("Recursos") disponible en todas las vistas del sitio (Inicio, Exámenes, Foros).
* **Contenido Persistente:** Muestra definiciones clave, fórmulas y recursos de apoyo que acompañan al alumno durante toda la navegación.
* **Gestión Centralizada:** El contenido es único para todo el curso y solo puede ser modificado por el tutor.

### 4. Roles de Usuario
* **Tutor (Admin/Staff):** Tiene control total (CRUD) sobre actividades, exámenes y el glosario global.
* **Alumno:** Puede visualizar el contenido, responder exámenes, formularios o cuestionarios, participar en foros y consultar el glosario.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django 5.2.
* **Base de Datos:** SQLite (por defecto).
* **Frontend:** HTML5, CSS3 (Estilos personalizados y responsivos), JavaScript.
* **Librerías Clave:**
    * `django-ckeditor` / `django-ckeditor-5`: Para edición de texto enriquecido.
    * `pillow`: Para manejo de imágenes.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Jupazumur/Proyecto_IngSoft2_2025-2.git](https://github.com/Jupazumur/Proyecto_IngSoft2_2025-2.git)
    cd Proyecto_IngSoft2_2025-2
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv .venv
    # En Windows:
    .\.venv\Scripts\activate
    # En Mac/Linux:
    source .venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install Django==5.2.8 django-ckeditor==6.7.3 django-ckeditor-5==0.2.18 django-js-asset==3.1.2 pillow==12.0.0 sqlparse==0.5.3 asgiref==3.10.0
    ```

4.  **Aplicar migraciones:**
    ```bash
    python manage.py migrate
    ```

5.  **Crear un superusuario (Tutor):**
    Para poder editar el contenido y el glosario, necesitas una cuenta de administrador.
    ```bash
    python manage.py createsuperuser
    ```

6.  **Ejecutar el servidor:**
    ```bash
    python manage.py runserver
    ```

¡Y Listo!

---

## 📖 Guía de Uso Rápido

1.  **Para editar contenido:** Inicia sesión con tu cuenta de superusuario. Verás botones de "Editar" en las actividades y el botón naranja dentro del Glosario Global.
2.  **Para ver como alumno:** Cierra sesión o abre una ventana de incógnito. Los botones de edición desaparecerán, pero podrás interactuar con los foros y exámenes.

---

## 👥 Créditos
Proyecto desarrollado para la materia de Ingeniería de Software II.

**Herramientas de Asistencia:**
* El desarrollo contó con la asistencia de **Gemini** y **ChatGPT** para la optimización de código, corrección de bugs y generación de *snippets* de Django/HTML.
