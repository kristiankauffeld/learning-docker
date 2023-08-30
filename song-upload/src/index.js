const express = require('express');

if (!process.env.PORT) {
  throw new Error(
    'Please specify the port number for the HTTP server with the environment variable PORT.'
  );
}

const PORT = process.env.PORT;

const app = express();

app.get('/', (req, res) => {
  res.send('Hello !');
});

app.listen(PORT, () => {
  console.log(
    `Microservice listening on port ${PORT}, point your browser at http://localhost:${PORT}/`
  );
});
