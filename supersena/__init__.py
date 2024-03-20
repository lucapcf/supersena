from flask import Flask, render_template, request, redirect
# from app import create_session, add_bet
from app import session, add_bet

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    print(request.method)
    print(request.form.get('start'))
    # if request.method == "GET" and request.form.get('start'):
    #     return redirect("aposta")
    return render_template("index.html")

@app.route('/aposta', methods=["POST", "GET"])
# @app.route('/')
def aposta():    
    if request.method == "POST":
        # if request.ok():
        name = request.form.get('name')
        cpf = request.form.get('cpf')
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        n3 = request.form.get('n3')
        n4 = request.form.get('n4')
        n5 = request.form.get('n5')

        # session = add_bet(session, name, cpf, n1, n2, n3, n4, n5)
        add_bet(session, name, cpf, n1, n2, n3, n4, n5)

    return render_template("aposta.html")

@app.route('/premiacao', methods=["GET"])
def premiacao():
    return render_template("premiacao.html")

if __name__ == "__main__":
    app.run(debug=True)
