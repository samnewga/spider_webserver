from flask import Flask, render_template, url_for
import movements

#Uncomment after debugging of ml.py
#import ml

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/action1')
def action_one():
    movements.forward()
    return render_template('controls.html')

@app.route('/action2')
def action_two():
    movements.backward()
    return render_template('controls.html')

@app.route('/action3')
def action_three():
    movements.turn()
    return render_template('controls.html')

@app.route('/action4')
def action_four():
    movements.turn2()
    return render_template('controls.html')

# Place holder function for ML
@app.route('/action5')
def action_five():
    #uncomment after debugging of ml.py
    #ml.photo()
    return render_template('controls.html')

@app.route('/controls')
def controls():
    return render_template('controls.html')

# Remove debug=Treue and change to IP of network to access remotely
if __name__=='__main__':
    app.run(debug=True)