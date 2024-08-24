from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)  # 1-5, where 1 is low and 5 is high
    status = db.Column(db.String(20), nullable=False, default='open')  # open, in_progress, completed
    due_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    dependencies = db.Column(db.String(200), nullable=True)  # comma-separated list of task IDs

    def __repr__(self):
        return f'Task {self.title}'

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    reminder_date = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'Reminder for Task {self.task_id}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'User {self.username}'

def create_task(title, description, priority, due_date, assigned_to=None, dependencies=None):
    task = Task(title=title, description=description, priority=priority, due_date=due_date, assigned_to=assigned_to, dependencies=dependencies)
    db.session.add(task)
    db.session.commit()
    return task

def get_task(task_id):
    return Task.query.get(task_id)

def update_task(task_id, title, description, priority, due_date, assigned_to=None, dependencies=None):
    task = get_task(task_id)
    if task:
        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date
        task.assigned_to = assigned_to
        task.dependencies = dependencies
        db.session.commit()
    return task

def delete_task(task_id):
    task = get_task(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

def list_tasks(status=None, priority=None, assigned_to=None):
    tasks = Task.query
    if status:
        tasks = tasks.filter_by(status=status)
    if priority:
        tasks = tasks.filter_by(priority=priority)
    if assigned_to:
        tasks = tasks.filter_by(assigned_to=assigned_to)
    return tasks.all()
