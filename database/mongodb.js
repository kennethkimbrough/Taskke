// database/mongodb.js
import { MongoClient } from 'mongodb';
import { Database } from './db';

class MongoDBDatabase implements Database {
  private client: MongoClient;

  async connect() {
    this.client = await MongoClient.connect('mongodb://localhost:27017', { useNewUrlParser: true, useUnifiedTopology: true });
  }

  async disconnect() {
    await this.client.close();
  }

  async getTasks() {
    const tasks = await this.client.collection('tasks').find().toArray();
    return tasks;
  }

  async getTaskById(id: string) {
    const task = await this.client.collection('tasks').findOne({ _id: new ObjectId(id) });
    return task;
  }

  async createTask(task: Task) {
    const result = await this.client.collection('tasks').insertOne(task);
    return result.ops[0];
  }

  async updateTask(task: Task) {
    const result = await this.client.collection('tasks').updateOne({ _id: new ObjectId(task._id) }, { $set: task });
    return result.ops[0];
  }

  async deleteTask(id: string) {
    await this.client.collection('tasks').deleteOne({ _id: new ObjectId(id) });
  }
}

export default MongoDBDatabase;
