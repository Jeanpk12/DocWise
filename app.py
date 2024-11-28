from flask import Flask, render_template
from controllers.translation_controller import translation_controller
from controllers.explanation_controller import explanation_controller

app = Flask(__name__)

# Registrando os blueprints
app.register_blueprint(translation_controller)
app.register_blueprint(explanation_controller)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
