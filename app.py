from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dating_app.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    preferences = db.Column(db.String(50), nullable=False)
    matches = db.relationship('Match', backref='user', lazy=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_id = db.Column(db.Integer, nullable=False)

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=1, max=10)])
    preferences = StringField('Preferences', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create Profile')

class MatchForm(FlaskForm):
    match_id = IntegerField('Match ID', validators=[DataRequired()])
    submit = SubmitField('Match')

db.create_all()

@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            age=form.age.data,
            bio=form.bio.data,
            gender=form.gender.data,
            preferences=form.preferences.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Profile created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_profile.html', form=form)

@app.route('/match/<int:id>', methods=['POST'])
def match(id):
    user = User.query.get_or_404(id)
    match_form = MatchForm()
    if match_form.validate_on_submit():
        new_match = Match(
            user_id=user.id,
            match_id=match_form.match_id.data
        )
        db.session.add(new_match)
        db.session.commit()
        flash('Matched successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('match.html', user=user, form=match_form)

if __name__ == '__main__':
    app.run(debug=True)
