const path = require('path');
const express = require('express');
const amqp = require('amqplib');

if (!process.env.PORT) {
  throw new Error(
    'Please specify the port number for the HTTP server with the environment variable PORT.'
  );
}

const PORT = process.env.PORT;
const RABBIT = process.env.RABBIT;

const app = express();

async function sendUploadedMessage(messageChannel, filePath) {
  try {
    console.log(`Publishing message on "uploaded" queue.`);
    const msg = { filePath: filePath };
    const jsonMsg = JSON.stringify(msg);
    messageChannel.publish('', 'uploaded', Buffer.from(jsonMsg));
  } catch (err) {
    console.error('Failed to send message:', err);
  }
}

async function main() {
  const messagingConnection = await amqp.connect(RABBIT);
  const messageChannel = await messagingConnection.createChannel();

  app.post('/upload', async (req, res) => {
    try {
      const filePath = path.join(
        __dirname,
        '..',
        'songs',
        'Cy-Curnin-Comfy-Couches.mp3'
      );
      await sendUploadedMessage(messageChannel, filePath);
      res
        .status(202)
        .json({ message: 'Song upload accepted and processing will begin.' });
    } catch (err) {
      console.error('Upload failed:', err);
      res.status(500).json({ message: 'Internal Server Error' });
    }
  });

  app.listen(PORT, () => {
    console.log(
      `Microservice listening on port ${PORT}, point your browser at http://localhost:${PORT}/`
    );
  });
}

main().catch((err) => {
  console.error('Microservice failed to start.');
  console.error((err && err.stack) || err);
});
