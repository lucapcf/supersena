from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/aposta', methods=["POST"])
def aposta():
    if request.method == "POST":
        if request.ok():
            print("shit")

    name = "string"
    return render_template("index.html", name=name)

@app.route('/premiacao')
def premiacao():

if __name__ == "__main__":
    app.run(debug=True)
