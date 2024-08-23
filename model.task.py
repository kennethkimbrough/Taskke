from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(20), nullable=False, default='open')
    due_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'Task {self.title}'

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    reminder_date = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'Reminder for Task {self.task_id}'

def create_task(title, description, priority, due_date):
    task = Task(title=title, description=description, priority=priority, due_date=due_date)
    db.session.add(task)
    db.session.commit()
    return task

def get_task(task_id):
    return Task.query.get(task_id)

def update_task(task_id, title, description, priority, due_date):
    task = get_task(task_id)
    if task:
        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date
        db.session.commit()
    return task

def delete_task(task_id):
    task = get_task(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

def list_tasks(status=None, priority=None):
    tasks = Task.query
    if status:
        tasks = tasks.filter_by(status=status)
    if priority:
        tasks = tasks.filter_by(priority=priority)
    return tasks.all()
