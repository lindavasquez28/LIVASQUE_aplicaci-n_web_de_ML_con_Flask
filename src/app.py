from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Variables
modelo_cargado = None
mensaje_error = ""

# Carga
try:
    ruta_actual = os.path.dirname(__file__)
    ruta_modelo = os.path.join(ruta_actual, "..", "models", "modelo_listo.pkl")
    
    with open(ruta_modelo, "rb") as archivo:
        modelo_cargado = pickle.load(archivo)
        
except Exception as error_detectado:
    # Si falla, atrapamos el error y guardamos la ruta que Python intentó leer
    mensaje_error = f"Error detectado: {error_detectado}. Ruta intentada: {os.path.abspath(ruta_modelo)}"

# diccionario para traducir la predicción
nombres_flores = {
    0: "Iris Setosa",
    1: "Iris Versicolor",
    2: "Iris Virginica"
}

@app.route("/", methods=["GET", "POST"])
def pagina_principal():
    if modelo_cargado is None:
        return f"<h1>⚠️ La aplicación encendió, pero el modelo falló</h1><p>{mensaje_error}</p><p>Revisa si el archivo 'modelo_listo.pkl' realmente está adentro de la carpeta 'models' en la página de GitHub.</p>"
    
    resultado_prediccion = None
    
    if request.method == "POST":
        largo_sepalo = float(request.form["largo_sepalo"])
        ancho_sepalo = float(request.form["ancho_sepalo"])
        largo_petalo = float(request.form["largo_petalo"])
        ancho_petalo = float(request.form["ancho_petalo"])
        
        datos_ingresados = [[largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo]]
        
        numero_predicho = modelo_cargado.predict(datos_ingresados)[0]
        resultado_prediccion = nombres_flores[numero_predicho]

    return render_template("index.html", prediccion=resultado_prediccion)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)