from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask('Steps')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steps.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer)
    date = db.Column(db.date)
    in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Product{self.id}. {self.steps} - {self.date}'


@app.route('/')
def main():
    steps = Steps.query.all()
    return render_template('index.html', steps_list=steps)


@app.route('/in_stock/<product_id>', methods=['PATCH'])
def modify_product(product_id):
    product = Product.query.get(product_id)
    product.in_stock = request.json['in_stock']
    db.session.commit()


@app.route('/add', methods=['POST'])
def add_product():
    data = request.json
    product = Product(**data)
    db.session.add(product)
    db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



with app.app_context():
    db.create_all()
app.run()
