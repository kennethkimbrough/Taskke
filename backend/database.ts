// backend/database.ts
import mongoose from 'mongoose';

const connectionString = 'mongodb://localhost:27017/taskke';

mongoose.connect(connectionString, { useNewUrlParser: true, useUnifiedTopology: true });

const db = mongoose.connection;

db.on('error', (error) => {
  console.error(error);
});

db.once('open', () => {
  console.log('Connected to MongoDB');
});
//NLU
const db = new Database();

app.post('/chat', (req, res) => {
  const input = req.body.message;
  const python = new pythonShell('nlu.py');

  python.send(input);
  python.on('message', (response) => {
    // Save the conversation to the database
    db.saveConversation(req.body.userId, input, response);
    res.json({ response: response });
  });
});
