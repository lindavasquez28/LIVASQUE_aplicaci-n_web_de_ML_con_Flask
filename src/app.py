import os
import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

ruta_actual = os.path.abspath(os.path.dirname(__file__))
ruta_modelo = os.path.join(ruta_actual, "..", "models", "modelo_listo.pkl")

# Carga
modelo_cargado = pickle.load(open(ruta_modelo, "rb"))

# ciccionario para traducir los numeros a texto
nombres_flores = {
    0: "Iris Setosa",
    1: "Iris Versicolor",
    2: "Iris Virginica"
}

@app.route("/", methods=["GET", "POST"])
def pagina_principal():
    resultado_prediccion = None
    
    if request.method == "POST":
        # datos numéricos que el usuario escribió en el formulario
        largo_sepalo = float(request.form["largo_sepalo"])
        ancho_sepalo = float(request.form["ancho_sepalo"])
        largo_petalo = float(request.form["largo_petalo"])
        ancho_petalo = float(request.form["ancho_petalo"])
        
        # se juntan los datos en una lista para el modelo
        datos_ingresados = [[largo_sepalo, ancho_sepalo, largo_petalo, ancho_petalo]]
        
        # prediccion y traduccion
        numero_predicho = modelo_cargado.predict(datos_ingresados)[0]
        resultado_prediccion = nombres_flores[numero_predicho]

    # Render
    return render_template("index.html", prediccion=resultado_prediccion)

# Para ejecutar:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)