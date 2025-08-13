from flask import Flask, render_template, request, send_file
import os
import robocontratos

app = Flask(__name__)


def executar_robo(valor: str, tipo: str) -> str:
    """Executa o robô principal e retorna o caminho do PDF gerado."""
    robocontratos.main()
    return os.path.join(robocontratos.Config.CONTRATOS_DIR, f"{valor}.pdf")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cnvw', methods=['GET', 'POST'])
def cnvw():
    if request.method == 'POST':
        valor = request.form['valor']
        pdf_path = executar_robo(valor, 'CNVW')
        return send_file(pdf_path, download_name='resultado.pdf', as_attachment=True)
    return render_template('form.html', titulo='CNVW')


@app.route('/fiat', methods=['GET', 'POST'])
def fiat():
    if request.method == 'POST':
        valor = request.form['valor']
        pdf_path = executar_robo(valor, 'FIAT')
        return send_file(pdf_path, download_name='resultado.pdf', as_attachment=True)
    return render_template('form.html', titulo='FIAT')


if __name__ == '__main__':
    app.run(debug=True)
