Aplicación de Análisis de Consumo de Alcohol y Salud
Descripción
Esta aplicación permite gestionar y analizar datos relacionados con el consumo de alcohol y su impacto en la salud, utilizando una interfaz gráfica desarrollada en Tkinter y una base de datos en MySQL. La aplicación incluye funcionalidades para registrar datos, realizar consultas y visualizar estadísticas mediante gráficos, facilitando la toma de decisiones informadas en el ámbito de la salud pública.

Características
Interfaz gráfica amigable para ingresar y consultar datos.
Conexión a una base de datos MySQL para almacenamiento y gestión de información.
Visualización de gráficos de tendencias y patrones utilizando matplotlib.
Opciones para agregar, consultar y analizar registros fácilmente.
Requisitos del Sistema
Python 3.8 o superior
MySQL 5.7 o superior
Librerías de Python necesarias (ver Instalación)
Sistema operativo: Windows, macOS o Linux

Instalación
1. Clonar el repositorio
Descarga o clona el proyecto desde GitHub:

bash
Copiar código
git clone https://github.com/tuusuario/consumo-alcohol-salud.git
cd consumo-alcohol-salud
2. Instalar dependencias
Asegúrate de tener Python instalado y ejecuta el siguiente comando para instalar las dependencias necesarias:

bash
Copiar código
pip install -r requirements.txt
3. Configurar la base de datos
Instala y configura MySQL en tu sistema.
Crea una base de datos ejecutando los siguientes comandos en MySQL:
sql
Copiar código
CREATE DATABASE consumo_alcohol;
USE consumo_alcohol;
CREATE TABLE registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    edad INT NOT NULL,
    genero VARCHAR(10) NOT NULL,
    consumo_alcohol INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Configura las credenciales de la base de datos en el archivo config.py:
python
Copiar código
DB_CONFIG = {
    "host": "localhost",
    "user": "tu_usuario",
    "password": "tu_contraseña",
    "database": "consumo_alcohol"
}
Funcionamiento
1. Ejecutar la aplicación
Ejecuta el archivo principal para iniciar la aplicación:

bash
Copiar código
python main.py
2. Uso de la interfaz
Agregar datos: Ingresa la edad, género y consumo de alcohol de un individuo, y guarda el registro en la base de datos.
Consultar registros: Visualiza los registros almacenados en una tabla interactiva.
Generar estadísticas: Haz clic en el botón de estadísticas para ver gráficos que muestran tendencias y patrones de consumo.
3. Visualización de gráficos
La aplicación genera gráficos utilizando matplotlib, lo que facilita entender cómo el consumo de alcohol varía según los diferentes factores.

Capturas de Pantalla
Pantalla Principal:

Gráfico de Tendencias:

Tecnologías Utilizadas
Python: Para la lógica de la aplicación.
Tkinter: Para la interfaz gráfica.
MySQL: Para la gestión de la base de datos.
Matplotlib: Para la visualización de gráficos.
mysql-connector-python: Para la conexión con MySQL.
Contribuciones
Si deseas contribuir a este proyecto:

Haz un fork del repositorio.
Crea una nueva rama para tus cambios:
bash
Copiar código
git checkout -b mi-rama
Realiza tus cambios y súbelos:
bash
Copiar código
git add .
git commit -m "Descripción de los cambios"
git push origin mi-rama
Crea un pull request en el repositorio principal.
Licencia
Este proyecto está licenciado bajo la Licencia MIT. Puedes utilizarlo libremente para fines educativos o personales.
