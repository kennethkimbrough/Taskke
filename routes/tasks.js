// api/tasks.js
import express from 'express';
import { MongoDBDatabase } from '../database/mongodb';

const app = express();
const db = new MongoDBDatabase();

app.get('/tasks', async (req, res) => {
  try {
    const tasks = await db.getTasks();
    res.json(tasks);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error retrieving tasks' });
  }
});

app.get('/tasks/:id', async (req, res) => {
  try {
    const task = await db.getTaskById(req.params.id);
    if (!task) {
      res.status(404).json({ message: 'Task not found' });
    } else {
      res.json(task);
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error retrieving task' });
  }
});

// ...
