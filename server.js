import express from 'express'
import { createServer } from "http"
import { Server } from "socket.io"
import path from 'path'
import fs from 'fs'
import { spawn } from 'child_process'
import { spawnSync } from 'child_process'

const port = process.env.PORT || 3000

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
  socket.on("UQ", ({img, UQ_r}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("UQ", UQ_r)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("MC", ({img, MC_d}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("MC", MC_d)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("KM", ({img, KM_c, KM_i}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("KM", KM_c, KM_i)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("VQ", ({img, VQ_c, VQ_e, VQ_w, VQ_h}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("VQ", VQ_c, VQ_e, VQ_w, VQ_h)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("OCT", ({img, OCT_p}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("OCT", OCT_p)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("AC", ({img, AC_c}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("AC", AC_c)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("PM", ({img, PM_c}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("PM", PM_c)

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })

  socket.on("SRCNN", ({img}) => {
    const buffer = Buffer.from(img);
    fs.writeFileSync('input.png', buffer)

    PythonAlgorithm("SRCNN")

    const imgOutput = fs.readFileSync('output.png')
    socket.emit('result', imgOutput)
  })
})

function PythonAlgorithm(type, par1, par2, par3, par4){
  const pythonScript = 'Algorithms/Main.py';

  const pythonProcess = spawnSync('python', [pythonScript, type, par1, par2, par3, par4], {
    cwd: process.cwd(),
    env: process.env,
    stdio: 'pipe',
    encoding: 'utf-8'
  });
}

server.listen(port)