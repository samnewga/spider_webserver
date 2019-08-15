from flask import Flask, render_template, url_for

#import movements


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/controls')
def controls():
    return render_template('controls.html')

@app.route('/action1', methods=['GET', 'POST'])
def action_one():

    #movements.forward()
    return render_template('controls.html')

@app.route('/action2')
def action_two():
    #movements.backward()
    return render_template('controls.html')

@app.route('/action3')
def action_three():
    #movements.turn()
    return render_template('controls.html')

@app.route('/action4')
def action_four():
    #movements.turn2()
    return render_template('controls.html')

@app.route('/action5')
def action_five():
    print('hello')
    return render_template('controls.html')


if __name__=='__main__':
    app.run(debug=True)