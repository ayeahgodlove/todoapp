from typing import final
from flask import Flask, jsonify, redirect, render_template, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ayeah:673687549@localhost:5432/todoapp'
db = SQLAlchemy(app, session_options={"expire_on_commit": False})
migrate = Migrate(app, db) # Bootstrap our application migrations

# models
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'
        
# db.create_all()

@app.route('/todos/create', methods=['POST', 'GET'])
def create_todo():
    error=False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description']=todo.description

    except:
        error=True
        db.session.rollback()
        error=True
        print(sys.exc_info())

    finally: 
        db.session.close()
    
    if error == True:
        abort (400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed=request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed=completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())
