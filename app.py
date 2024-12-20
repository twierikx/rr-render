from flask import Flask, render_template, redirect
from datetime import datetime

from flask import Blueprint
from pages.all_recipes import all_recipes_bp
from pages.one_recipe import one_recipe_bp
# from pages.edit_recipes import edit_recipes_bp
# from pages.add_recipes import add_recipes_bp

app = Flask(__name__)

app.register_blueprint(all_recipes_bp)
app.register_blueprint(one_recipe_bp)
# app.register_blueprint(edit_recipes_bp)
# app.register_blueprint(add_recipes_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/regalitodemargot')
def regalito_de_margot():
    return render_template('regalito-de-margot.html')

@app.route('/regalito-de-margot')
def regalito_de_margot2():
    return redirect('/regalitodemargot')

if __name__ == '__main__':
    app.run(debug=True)
