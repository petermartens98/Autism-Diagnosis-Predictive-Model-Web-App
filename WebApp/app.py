from flask import Flask, render_template, request, redirect, flash,  url_for, session
import pandas as pd
import tensorflow as tf
from tensorflow import keras

model = tf.keras.models.load_model('AQ10_model_weights.h5')
app = Flask(__name__)
app.secret_key = 'app_secret_key'

@app.route('/submit', methods=['POST'])
def submit():
    scores = {
        'A1_Score': 0,
        'A2_Score': 0,
        'A3_Score': 0,
        'A4_Score': 0,
        'A5_Score': 0,
        'A6_Score': 0,
        'A7_Score': 0,
        'A8_Score': 0,
        'A9_Score': 0,
        'A10_Score': 0
    }
    
    for i in range(1, 11):
        key = 'A{}_Score'.format(i)
        answer = request.form.get('q{}'.format(i))
        if answer:
            if answer == 'agree':
                scores[key] = 1
            elif answer == 'disagree':
                scores[key] = 0

    df = pd.DataFrame(scores, index=[0])
    predictions = model.predict(df)
    percentage_yes = predictions[0][1] * 100
    percentage_no = predictions[0][0] * 100
    if percentage_yes >= percentage_no: diagnosis = "Yes"
    else: diagnosis = "No"
    session['diagnosis'] = diagnosis
    session['scores'] = scores
    flash(f"Autism Prediction: {diagnosis}")
    return redirect(url_for('index'))

@app.route('/')
def index():
    diagnosis = session.get('diagnosis', None)
    scores = session.get('scores', {
        'A1_Score': '',
        'A2_Score': '',
        'A3_Score': '',
        'A4_Score': '',
        'A5_Score': '',
        'A6_Score': '',
        'A7_Score': '',
        'A8_Score': '',
        'A9_Score': '',
        'A10_Score': ''
    })
    return render_template('index.html', diagnosis=diagnosis, scores=scores)

if __name__ == '__main__':
    app.run(debug=True)