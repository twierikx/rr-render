from flask import Flask, render_template, request
from routers.database import database_bp
from routers.get_recipes import get_recipes_bp
# from routers import add_recipes, database, edit_recipes, get_recipes, models
app = Flask(__name__)

recipes = []

app.register_blueprint(database_bp)
app.register_blueprint(get_recipes_bp)

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
