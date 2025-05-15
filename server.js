import express from 'express'
import { createServer } from "http"
import { Server } from "socket.io"
import path from 'path'
import fs from 'fs'
import { spawn } from 'child_process'
import { spawnSync } from 'child_process'

const port = 3000

const app = express()
const server = createServer(app)
const io = new Server(server, {
    maxHttpBufferSize: 1e8
  })

app.use(express.static('public'))

app.get('/', (req, res) => {
    return res.sendFile(path.resolve() + '/public/index.html');
  });

io.on('connection', (socket) => {
  socket.on("image", (img) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('img.png', buffer)
    fs.writeFileSync('Algorithms/input.png', buffer)

    const imgReturn = fs.readFileSync('img.png')
    socket.emit('hello', imgReturn)

    PythonAlgorithm()

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('hello', imgOutput)
  }); 
})

function PythonAlgorithm(){
  // Path to your Python script 
  const pythonScript = 'Algorithms/Main.py';

  // Dynamic value from Node.js
  const dynamicValue = '0';

  // Spawn a child process
  const pythonProcess = spawnSync('python', [pythonScript, dynamicValue, '4', '5']);

}

server.listen(port)