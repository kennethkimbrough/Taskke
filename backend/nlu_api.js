const express = require('express');
const app = express();
const pythonShell = require('python-shell');
const session = require('express-session');
const MongoDBStore = require('connect-mongodb-session')(session);
const mongoose = require('mongoose');

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/taskke', { useNewUrlParser: true, useUnifiedTopology: true });

// Create a MongoDB store for sessions
const store = new MongoDBStore({
  uri: 'mongodb://localhost:27017/taskke',
  collection: 'sessions'
});

// Use sessions
app.use(session({
  secret: 'taskke-secret',
  resave: false,
  saveUninitialized: true,
  store: store
}));

// Define the User model
const userSchema = new mongoose.Schema({
  userId: String,
  name: String,
  conversationHistory: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Conversation' }]
});

const User = mongoose.model('User', userSchema);

// Define the Conversation model
const conversationSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  input: String,
  response: String
});

const Conversation = mongoose.model('Conversation', conversationSchema);

app.post('/chat', (req, res) => {
  const userId = req.session.userId;
  const input = req.body.message;
  const python = new pythonShell('rasa_nlu.py');

  // Check if the user exists
  User.findOne({ userId: userId }, (err, user) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else if (!user) {
      // Create a new user
      const newUser = new User({ userId: userId, name: 'Unknown' });
      newUser.save((err, user) => {
        if (err) {
          console.error(err);
          res.status(500).json({ error: 'Internal Server Error' });
        } else {
          // Process the input
          python.send(input);
          python.on('message', (response) => {
            // Save the conversation to the database
            const conversation = new Conversation({ userId: user._id, input: input, response: response });
            conversation.save((err, conversation) => {
              if (err) {
                console.error(err);
                res.status(500).json({ error: 'Internal Server Error' });
              } else {
                res.json({ response: response });
              }
            });
          });
        }
      });
    } else {
      // Process the input
      python.send(input);
      python.on('message', (response) => {
        // Save the conversation to the database
        const conversation = new Conversation({ userId: user._id, input: input, response: response });
        conversation.save((err, conversation) => {
          if (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal Server Error' });
          } else {
            res.json({ response: response });
          }
        });
      });
    }
  });
});

app.listen(3001, () => {
  console.log('Rasa NLU API listening on port 3001');
});
