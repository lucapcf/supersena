from flask import Flask, render_template, request, redirect, url_for
from supersena.functions import session, add_bet, add_person, list_bets, draw, verification, clear_database
from supersena.models import Person, Bet

app = Flask(__name__)


# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     # response.headers['Cache-Control'] = 'public, max-age=600'
#     # response.headers['Pragma'] = 'no-cache'
#     # response.headers['Expires'] = '0'
#     response.headers['Cache-Control'] = "no-store"
#     return response

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/bet', methods=["POST", "GET"])
def bet():
    if request.method == "POST":
        if "sent" in request.form:
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
            text = list_bets()
            return render_template("bet.html", text=text)
        if "start" in request.form:
            text = list_bets()
            return render_template("bet.html", text=text)
    else:
        if request.method == "GET":
            if "start" in request.args:
                clear_database()
                text = list_bets()
                return render_template("bet.html", text=text)
            elif "surpresinha" in request.args:
                text = list_bets()
                return render_template("bet.html", text=text)
            else:
                clear_database()
                text = list_bets()
                return "<p>ERROR</p>"


@app.route('/surpresinha', methods=["POST", "GET"])
def surpresinha():
    if request.method == "POST":
        if "sent" in request.form:

            name = request.form.get('name')
            cpf = request.form.get('cpf')

            numbers = []

            for i in range(5):
                numbers.append(draw())

            n1 = numbers[0]
            n2 = numbers[1]
            n3 = numbers[2]
            n4 = numbers[3]
            n5 = numbers[4]

            person = session.query(Person).filter(Person.cpf == cpf).all()

            if not person:
                person = add_person(session, name, cpf)

            add_bet(session, n1, n2, n3, n4, n5, cpf)

            text = list_bets()
            return render_template("surpresinha.html", text=text)
        else:
            return "<p>ERROR</p>"
    elif request.method == "GET":
        if "bet" in request.args:
            text = list_bets()
            return render_template("surpresinha.html", text=text)
        else:
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    else:
        clear_database()
        text = list_bets()
        return "<p>ERROR</p>"


@app.route('/results', methods=["GET"])
def results():
    if request.method == "GET":
        if "draw" in request.args:
            text = verification()
            return render_template("results.html", text=text)
        else:
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    else:
        clear_database()
        text = list_bets()
        return "<p>ERROR</p>"


if __name__ == "__main__":
    app.run(debug=True)