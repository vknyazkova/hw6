from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column('id', db.Integer, primary_key=True)
    question = db.Column('question', db.Text)


class Responders(db.Model):
    __tablename__ = 'responders'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text)
    age = db.Column('age', db.Integer)
    city = db.Column('city', db.String(30))
    gender = db.Column('gender', db.String(8))


class Answers(db.Model):
    __tablename__ = "answers"

    id = db.Column('id', db.Integer, primary_key=True)
    resp_id = db.Column('resp_id', db.Integer, db.ForeignKey("responders.id"))
    resp = db.relationship('Responders', primaryjoin="Answers.resp_id==Responders.id")

    q_id = db.Column('question_id', db.Integer, db.ForeignKey("questions.id"))
    q = db.relationship('Questions', primaryjoin="Answers.q_id==Questions.id")
    answer = db.Column('answer', db.Integer)


class Choices(db.Model):
    __tablename__ = "choices"

    id = db.Column('choice_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    ru_name = db.Column('ru_name', db.String(100))


class SelectedChoices(db.Model):
    __tablename__ = "selected_choices"

    id = db.Column('id', db.Integer, primary_key=True)
    choice_id = db.Column(db.Integer, db.ForeignKey('choices.choice_id'))
    choice = db.relationship('Choices', primaryjoin="SelectedChoices.choice_id==Choices.id")
    resp_id = db.Column(db.Integer, db.ForeignKey("responders.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
