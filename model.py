from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='Pending')
    assigned_to = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    comments = relationship("Comment", back_populates="task")
    attachments = relationship("Attachment", back_populates="task")
    progress = Column(Integer, nullable=False, default=0)
    analytics = Column(Text, nullable=True)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    tasks = relationship("Task", back_populates="project")
    progress = Column(Integer, nullable=False, default=0)
    analytics = Column(Text, nullable=True)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    task = relationship("Task", back_populates="comments")

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    file_path = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    task = relationship("Task", back_populates="attachments")

Project_management.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    dependencies = relationship("Task", secondary="task_dependencies", primaryjoin="Task.id==TaskDependency.task_id", secondaryjoin="Task.id==TaskDependency.dependency_id")
    project = relationship("Project", back_populates="tasks")

class TaskDependency(Base):
    __tablename__ = 'task_dependencies'
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    dependency_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)

# Database setup
DATABASE_URL = 'sqlite:///project_management.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create a new project
project = Project(name='Taskke', description='Project management system for Taskke')
session.add(project)
session.commit()

# Add tasks to the project
task1 = Task(name='Design Database Schema', duration=5, project_id=project.id)
task2 = Task(name='Implement CRUD Operations', duration=10, project_id=project.id)
task3 = Task(name='Develop Frontend', duration=7, project_id=project.id)
task4 = Task(name='Testing and Deployment', duration=3, project_id=project.id)

session.add_all([task1, task2, task3, task4])
session.commit()

# Define task dependencies
task2.dependencies.append(task1)
task3.dependencies.append(task2)
task4.dependencies.append(task3)
session.commit()

# Print project details
print(f"Project: {project.name}")
for task in project.tasks:
    print(f"Task: {task.name}, Duration: {task.duration} days, Dependencies: {[t.name for t in task.dependencies]}")

# Save project to file
with open('project_taskke.txt', 'w') as f:
    f.write(f"Project: {project.name}\n")
    for task in project.tasks:
        f.write(f"Task: {task.name}, Duration: {task.duration} days, Dependencies: {[t.name for t in task.dependencies]}\n")
