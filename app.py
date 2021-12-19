from flask import Flask, render_template, request, flash
from models import db, Questions, Responders, Answers, SelectedChoices, Choices
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
    questions1 = Questions.query.all()
    if request.method == 'POST':

        r = Responders(age=int(request.form['2']),
                       name=request.form['1'],
                       city=request.form['3'],
                       gender=request.form['4'])
        db.session.add(r)
        db.session.commit()
        db.session.refresh(r)

        questions = ['5', '6', '11']
        for question in questions:
            answer = request.form[question]
            if len(answer) == 0:
                continue
            a = Answers(resp_id=r.id, q_id=int(question), answer=answer)
            db.session.add(a)

        wishes = request.form.getlist('7')
        if len(wishes) != 0:
            all_wishes = ''
            for wish in wishes:
                all_wishes += wish + ';'
            a = Answers(resp_id=r.id, q_id=7, answer=all_wishes)
            db.session.add(a)
        db.session.commit()

        choices_q = ['8', '9', '10']
        for q in choices_q:
            print(q)
            choices = request.form.getlist(q)
            for choice in choices:
                print(choice)
                ch = db.session.query(Choices).filter_by(name=choice).all()
                ch_id = ch[0].id
                c = SelectedChoices(choice_id=ch_id, resp_id=r.id, question_id=int(q))
                db.session.add(c)
        db.session.commit()
    return render_template('form2.html', questions=questions1)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    res = {}
    count_responders = db.session.query(func.count(Responders.id))
    res['resp_num'] = count_responders.first()[0]

    age = db.session.query(func.sum(Responders.age), func.count(Responders.id))
    age = age.all()
    res['av_age'] = age[0][0] // age[0][1]

    wishlist_exists_dict = {'no': 0, 'yes': 0}
    wishlist_exist = db.session.query(Answers.answer, func.count(Answers.resp_id)) \
                    .filter(Answers.q_id == 6) \
                    .group_by(Answers.answer)

    wishlist_exists_dict.update(dict(wishlist_exist.all()))
    res['wishlistExists'] = round(wishlist_exists_dict['yes'] / (wishlist_exists_dict['yes'] + wishlist_exists_dict['no']) * 100, 2)

    present_cost = db.session.query(Answers.answer, func.count(Answers.resp_id)) \
                    .filter(Answers.q_id == 5) \
                    .group_by(Answers.answer) \
                    .order_by(-func.count(Answers.resp_id))
    res['present_cost'] = dict(present_cost.all())
    for price in res['present_cost']:
        res['present_cost'][price] = round(res['present_cost'][price] / res['resp_num'] * 100, 2)

    popular_colors = db.session.query(Choices.ru_name, func.count(SelectedChoices.resp_id)) \
                    .join(Choices) \
                    .filter(SelectedChoices.question_id == 8) \
                    .group_by(SelectedChoices.choice_id) \
                    .order_by(-func.count(SelectedChoices.resp_id))
    res['colors'] = dict(popular_colors.all())

    popular_sweets = db.session.query(Choices.ru_name, func.count(SelectedChoices.resp_id)) \
        .join(Choices) \
        .filter(SelectedChoices.question_id == 9) \
        .group_by(SelectedChoices.choice_id) \
        .order_by(-func.count(SelectedChoices.resp_id))
    res['sweets'] = dict(popular_sweets.all())

    popular_drinks = db.session.query(Choices.ru_name, func.count(SelectedChoices.resp_id)) \
        .join(Choices) \
        .filter(SelectedChoices.question_id == 10) \
        .group_by(SelectedChoices.choice_id) \
        .order_by(-func.count(SelectedChoices.resp_id))
    res['drinks'] = dict(popular_drinks.all())

    print(res)
    return render_template('statistics.html', results=res)


if __name__ == '__main__':
    app.run(debug=True)
