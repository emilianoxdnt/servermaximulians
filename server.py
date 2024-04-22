import os
from flask import Flask, request, send_file, render_template
from pytube import YouTube
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    default_limits=["1000 per day", "50 per hour"]
)

# Directorio donde se guardarán los archivos descargados
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Videos")

# Credenciales de autenticación
USERNAME = "maximus"
PASSWORD = "emiguap030"

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Descargar Archivos</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 50px;
                background-color: #f0f0f0; /* Color de fondo claro */
                color: #333; /* Color de texto oscuro */
            }
            .container {
                max-width: 500px;
                margin: 0 auto;
            }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"], select, .mode-button, .download-button {
                background-color: #4CAF50; /* Color de fondo verde */
                color: white; /* Color de texto blanco */
                padding: 15px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
            }
            input[type="submit"]:hover, select:hover, .mode-button:hover, .download-button:hover {
                background-color: #45a049; /* Cambiar color del botón al pasar el ratón */
            }

            /* Estilos para el modo oscuro */
            .dark-mode {
                background-color: #000; /* Fondo oscuro */
                color: #fff; /* Texto blanco */
            }

            .dark-mode .mode-button, .dark-mode .download-button {
                background-color: #222; /* Color de fondo oscuro */
            }

            /* Estilos para el modo claro */
            .light-mode .mode-button, .light-mode .download-button {
                background-color: #fff; /* Color de fondo claro */
                color: #333; /* Color de texto oscuro */
                border: 2px solid #45a049; /* Borde verde */
            }

            /* Estilos para los botones de descarga */
            .download-button {
                display: block;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Maximulian Descargador</h1>
            <form action="/download" method="post">
                <label for="username">Usuario:</label><br>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Contraseña:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <label for="url">URL del video de YouTube:</label><br>
                <input type="text" id="url" name="url" required><br><br>
                <label for="option">Tipo de archivo:</label><br>
                <select id="option" name="option">
                    <option value="video">Video.mp4</option>
                    <option value="music">Música.mp3</option>
                </select><br><br>
                <input type="submit" value="Descargar" class="download-button">
            </form>
        </div>
        <button class="mode-button" onclick="toggleDarkMode()">&#127769; Modo Oscuro</button>
        <button class="mode-button" onclick="toggleLightMode()">&#9728; Modo Claro</button>
        <script>
            function toggleDarkMode() {
                document.body.classList.add("dark-mode");
                document.body.classList.remove("light-mode");
            }
            function toggleLightMode() {
                document.body.classList.remove("dark-mode");
                document.body.classList.add("light-mode");
            }
        </script>
    </body>
    </html>
    """

@app.route('/download', methods=['POST'])
@limiter.limit("10 per minute")
def download():
    username = request.form['username']
    password = request.form['password']
    if username == USERNAME and password == PASSWORD:
        url = request.form['url']
        option = request.form['option']
        try:
            if option == 'video':
                return download_video(url)
            elif option == 'music':
                return download_music(url)
        except Exception as e:
            return f"Error al descargar el archivo: {str(e)}"
    else:
        return "Credenciales incorrectas. Por favor, intenta de nuevo."

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    filename = "".join(c for c in yt.title if c.isalnum() or c in [' ', '.', '_', '-'])
    filepath = os.path.join(DOWNLOADS_DIR, f"{filename}.mp4")
    video.download(output_path=DOWNLOADS_DIR, filename=f"{filename}.mp4")
    return send_file(filepath, as_attachment=True)

def download_music(url):
    yt = YouTube(url)
    filename = "".join(c for c in yt.title if c.isalnum() or c in [' ', '.', '_', '-'])
    filepath = os.path.join(DOWNLOADS_DIR, f"{filename}.mp3")
    video_stream = yt.streams.filter(only_audio=True).first()
    video_stream.download(output_path=DOWNLOADS_DIR, filename=f"{filename}.mp3")
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    # Crear el directorio de descargas si no existe
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)
    app.run(debug=True, host='0.0.0.0', port=80)
