from flask import Flask, render_template, request

app = Flask(__name__)

recipes = []

@app.route('/')
def home():
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['POST'])
def add_recipe():
    recipe = request.form['recipe']
    recipes.append(recipe)
    return render_template('index.html', recipes=recipes)

@app.route('/api')
def api():
    return "<h3>This is the API</h3>"

if __name__ == '__main__':
    app.run(debug=True)
