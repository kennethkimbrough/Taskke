const express = require('express');
const app = express();
const pythonShell = require('python-shell');

app.post('/process_input', (req, res) => {
  const input = req.body.input;
  const python = new pythonShell('rasa_nlu.py');

  python.send(input);
  python.on('message', (response) => {
    res.json({ response: response });
  });
});

app.listen(3001, () => {
  console.log('Rasa NLU API listening on port 3001');
});
