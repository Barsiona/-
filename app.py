from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, unique=False, nullable=False)
    datas = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"Steps : {self.steps}, Data: {self.datas}"


@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')


# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    steps = request.form.get("steps")
    datas = request.form.get("datas")

    if steps and datas is not None:
        p = Profile(steps=steps, data=datas)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


@app.route('/delete/<int:id>')
def erase(id):
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()

