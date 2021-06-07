from flask import Flask, render_template, request
from lib.analysis import ObtenerValores
from lib.predict import Texto_On

app = Flask(__name__)

@app.route('/')
def index():
  opcion = request.args.get('op', type=int, default=-1)
  if opcion is None or opcion < 0:
    return render_template('index.html')
  else:
    texto_kichwa, texto_esp, jacard_values, cos_values, sentimiento = ObtenerValores(opcion)
    return render_template('index.html', kichwa=texto_kichwa, esp=texto_esp, jac=jacard_values, cos=cos_values, sent=sentimiento)

@app.route('/analisis', methods=['GET', 'POST'])
def analisis():
  if request.method == 'POST':
    text = request.form['text']
    jac_values, cos_values, sentimiento = Texto_On(text)
    return render_template('prediccion.html', jac=jac_values, cos=cos_values, sent=sentimiento, text=text)

  else:
    return render_template('prediccion.html')
