from flask import Flask, render_template, request, redirect
from supersena.functions import session, add_bet, add_person, list_bets
from supersena.models import Person, Bet

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/bet', methods=["POST", "GET"])
def bet():    
    if request.method == "POST":
        # if request.ok():
        name = request.form.get('name')
        cpf = request.form.get('cpf')
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        n3 = request.form.get('n3')
        n4 = request.form.get('n4')
        n5 = request.form.get('n5')


        person = session.query(Person).filter(Person.cpf == cpf).all()

        if not person:
            person = add_person(session, name, cpf)

        add_bet(session, n1, n2, n3, n4, n5, cpf)

        # session = add_bet(session, name, cpf, n1, n2, n3, n4, n5)

    text = list_bets()

    return render_template("bet.html", text=text)

@app.route('/results', methods=["GET"])
def results():
    text = list_bets()
    return render_template("results.html", text=text)

@app.route('/listar', methods=["GET"])
def listar():
    result = session.query(Bet).all()
    print("Bets?", result)
    return "<p>deu</p>"

if __name__ == "__main__":
    app.run(debug=True)
