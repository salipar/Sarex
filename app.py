from flask import Flask, render_template
from funcs import funcs_bp  # Import the Blueprint

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(funcs_bp)

@app.route('/calc')
def calc():
    return render_template('calc.html')


@app.route('/')
def hello_world():
#    return 'Hello, Sali!'
    return render_template('index.html')

if __name__ == '__main__':
   app.run(host = '0.0.0.0', debug=True)
#first program to test
