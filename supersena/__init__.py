from flask import Flask, render_template, request
from supersena.functions import session, add_bet, add_person, list_bets, draw, verification, clear_database, awards
from supersena.models import Person

app = Flask(__name__)

# Home page route
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


# Betting page route
@app.route('/bet', methods=["POST", "GET"])
def bet():
    if request.method == "POST":
        # Checks type of request
        if "sent" in request.form:
            name = request.form.get('name')
            cpf = request.form.get('cpf')
            n1 = request.form.get('n1')
            n2 = request.form.get('n2')
            n3 = request.form.get('n3')
            n4 = request.form.get('n4')
            n5 = request.form.get('n5')

            # Tests if numbers are distinct
            set_of_numbers = set({n1, n2, n3, n4, n5})
            if len(set_of_numbers) == 5:
                warning_bets = ""
            else:
                warning_bets = "Todos os números devem ser distintos, tente novamente."

            # Check if the person already exists in the database
            person = session.query(Person).filter(Person.cpf == cpf).first()
            if not person:
                warning_name = ""
            else:
                # Tests if name matches cpf
                if request.form.get('name') != person.name:
                    warning_name = "Esse CPF já foi registrado com outro nome, tente novamente."
                else:
                    warning_name = ""

            if warning_bets == warning_name == "":
                # Add the person
                person = add_person(session, name, cpf)
                # Add the bet 
                add_bet(session, n1, n2, n3, n4, n5, cpf)

            # Get list of all bets as String
            text = list_bets()
            return render_template("bet.html", text=text, warning_name=warning_name, warning_bets=warning_bets)
        else:
            # If request unknown delete data and return error
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    elif request.method == "GET":
        # Checks type of request
        if "start" in request.args:
            # If request from homepage clear db
            clear_database()
            text = list_bets()
            return render_template("bet.html", text=text)
        # Checks type of request
        elif "surpresinha" in request.args:
            text = list_bets()
            return render_template("bet.html", text=text)
        elif "back" in request.args:
            # Handle the case where back button might have been used
            return "<p>DALLLEEEE</p>"
        else:
            # If request unknown delete data and return error
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    else:
        # If request unknown delete data and return error
        clear_database()
        text = list_bets()
        return "<p>ERROR</p>"


# Aposta Surpresinha page route
@app.route('/surpresinha', methods=["POST", "GET"])
def surpresinha():
    if request.method == "POST":
        # Checks type of request
        if "sent" in request.form:

            name = request.form.get('name')
            cpf = request.form.get('cpf')

            # Draw 5 random numbers
            numbers = []
            for i in range(5):
                numbers.append(draw(numbers))

            n1 = numbers[0]
            n2 = numbers[1]
            n3 = numbers[2]
            n4 = numbers[3]
            n5 = numbers[4]

            # Check if the person already exists in the database
            person = session.query(Person).filter(Person.cpf == cpf).first()
            if not person:
                warning_name = ""
            else:
                # Tests if name matches cpf
                if request.form.get('name') != person.name:
                    warning_name = "Esse CPF já foi registrado com outro nome, tente novamente."
                else:
                    warning_name = ""

            if warning_name == "":
                # Add the person
                person = add_person(session, name, cpf)
                # Add the bet 
                add_bet(session, n1, n2, n3, n4, n5, cpf)

            # Get list of all bets as String
            text = list_bets()
            return render_template("surpresinha.html", text=text, warning_name=warning_name)
        else:
            # If request unknown delete data and return error
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    elif request.method == "GET":
        # Checks type of request
        if "bet" in request.args:
            # Get list of all bets as String
            text = list_bets()
            return render_template("surpresinha.html", text=text)
        else:
            # If request unknown delete data and return error
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    else:
        # If request unknown delete data and return error
        clear_database()
        text = list_bets()
        return "<p>ERROR</p>"

# Results page route
@app.route('/results', methods=["GET"])
def results():
    if request.method == "GET":
        # Checks type of request
        if "draw" in request.args:
            # Get list of results as String
            text = verification()
            return render_template("results.html", text=text)
        else:
            # If request unknown delete data and return error
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    else:
        # If request unknown delete data and return error
        clear_database()
        text = list_bets()
        return "<p>ERROR</p>"

# Awarding page route
@app.route('/awarding', methods=["GET"])
def awarding():
    if request.method == "GET":
        # Checks type of request
        if "results" in request.args:
            # Get list of awards as String
            text = awards()
            return render_template("awarding.html", text=text)
        else:
            # If request unknown delete data and return error
            clear_database()
            text = list_bets()
            return "<p>ERROR</p>"
    else:
        # If request unknown delete data and return error
        clear_database()
        text = list_bets()
        return "<p>ERROR</p>"


if __name__ == "__main__":
    app.run(debug=True)