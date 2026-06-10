from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/h2h')
def h2h():
    return render_template('h2h.html')

@app.route('/predictor')
def predictor():
    return render_template('predictor.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)