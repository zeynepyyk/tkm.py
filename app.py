from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cokgizlisifre'

CHOICES = ['Taş', 'Kağıt', 'Makas']
MOTIVATION_MESSAGES = [
    "Güç seninle olsun!",
    "Unutma, zihin kazanır!",
    "Şans yanında gibi görünüyor!",
    "Dikkatli oyna, strateji önemli.",
    "Bilgisayar her zaman akıllı değildir :)"
]

def determine_winner(user, computer):
    if user == computer:
        return "Berabere"
    elif (user == "Taş" and computer == "Makas") or \
         (user == "Kağıt" and computer == "Taş") or \
         (user == "Makas" and computer == "Kağıt"):
        return "Kullanıcı"
    else:
        return "Bilgisayar"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        rounds = int(request.form.get('rounds'))

        session['name'] = name
        session['surname'] = surname
        session['rounds'] = rounds
        session['current_round'] = 1
        session['user_score'] = 0
        session['computer_score'] = 0
        session['history'] = []

        return redirect(url_for('game'))

    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'current_round' not in session or session['current_round'] > session['rounds']:
        return redirect(url_for('result'))

    result = ""
    motivation = random.choice(MOTIVATION_MESSAGES)
    computer_choice = ""
    user_choice = ""
    winner = ""

    if request.method == 'POST':
        user_choice = request.form.get('choice')
        computer_choice = random.choice(CHOICES)
        winner = determine_winner(user_choice, computer_choice)

        if winner == "Kullanıcı":
            session['user_score'] += 1
            result = f"Sen kazandın! ({user_choice} > {computer_choice})"
        elif winner == "Bilgisayar":
            session['computer_score'] += 1
            result = f"Bilgisayar kazandı! ({user_choice} < {computer_choice})"
        else:
            result = f"Berabere! ({user_choice} = {computer_choice})"

        session['history'].append({
            'round': session['current_round'],
            'user': user_choice,
            'computer': computer_choice,
            'winner': winner,
            'time': datetime.now().strftime('%H:%M:%S')
        })

        session['current_round'] += 1

    return render_template('index.html',
                           name=session['name'],
                           surname=session['surname'],
                           round=session['current_round'],
                           total=session['rounds'],
                           result=result,
                           user_score=session['user_score'],
                           computer_score=session['computer_score'],
                           motivation=motivation,
                           choices=CHOICES,
                           history=session['history'])

@app.route('/result')
def result():
    if session['user_score'] > session['computer_score']:
        final = f"🎉 Tebrikler {session['name']}! Sen kazandın!"
    elif session['user_score'] < session['computer_score']:
        final = f"😞 Üzgünüm {session['name']}, bilgisayar kazandı."
    else:
        final = f"🤝 Oyun berabere bitti {session['name']}."

    return render_template('index.html',
                           final=final,
                           history=session.get('history', []),
                           restart=True)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
