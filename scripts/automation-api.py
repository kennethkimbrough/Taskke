from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['taskke']
tasks_collection = db['tasks']

# Automatic Task Assignment
@app.route('/assign_tasks', methods=['POST'])
def assign_tasks():
    # Get users and their workloads
    users = db['users'].find()
    user_workloads = {}
    for user in users:
        user_workloads[user['_id']] = user['workload']

    # Get tasks that need assignment
    tasks = tasks_collection.find({'assigned_to': None})

    # Assign tasks to users based on workload and priority
    for task in tasks:
        # Find the user with the lowest workload
        lowest_workload_user = min(user_workloads, key=user_workloads.get)
        # Assign the task to the user
        tasks_collection.update_one({'_id': task['_id']}, {'$set': {'assigned_to': lowest_workload_user}})
        # Update the user's workload
        db['users'].update_one({'_id': lowest_workload_user}, {'$inc': {'workload': 1}})

    return jsonify({'message': 'Tasks assigned successfully'})

# Task Reminders
@app.route('/send_reminders', methods=['POST'])
def send_reminders():
    # Get tasks with upcoming deadlines
    tasks = tasks_collection.find({'deadline': {'$lte': datetime.now() + timedelta(days=1)}})

    # Send reminders to users
    for task in tasks:
        user = db['users'].find_one({'_id': task['assigned_to']})
        # Send reminder email or notification
        print(f'Sending reminder to {user["email"]} for task {task["_id"]}')

    return jsonify({'message': 'Reminders sent successfully'})

# Task Status Updates
@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    # Get tasks that need status updates
    tasks = tasks_collection.find({'status': 'in_progress'})

    # Update task statuses based on user activity
    for task in tasks:
        # Check if the task is complete
        if task['progress'] == 100:
            tasks_collection.update_one({'_id': task['_id']}, {'$set': {'status': 'complete'}})

    return jsonify({'message': 'Task statuses updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)

# automation_api.py
from email_notifier import send_email_notification

# ...

@app.route('/assign_tasks', methods=['POST'])
def assign_tasks():
    # ...
    for task in tasks:
        # Assign the task to the user
        tasks_collection.update_one({'_id': task['_id']}, {'$set': {'assigned_to': lowest_workload_user}})
        # Send an email notification to the user
        send_email_notification(db['users'].find_one({'_id': lowest_workload_user}), task)
    # ...

