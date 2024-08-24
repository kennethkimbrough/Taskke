//TaskController.ts
import express, { Request, Response } from 'express';
import Task from '../models/Task';

const router = express.Router();

router.get('/', async (req: Request, res: Response) => {
  const tasks = await Task.find().populate('userId');
  res.json(tasks);
});

router.post('/', async (req: Request, res: Response) => {
  const task = new Task(req.body);
  await task.save();
  res.json(task);
});

router.get('/:id', async (req: Request, res: Response) => {
  const task = await Task.findById(req.params.id).populate('userId');
  if (!task) {
    res.status(404).json({ message: 'Task not found' });
  } else {
    res.json(task);
 
