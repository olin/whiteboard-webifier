import express from 'express';
import cors from 'cors';
const app = express();
const socket = require('./websocket-server');
const http = require('http');
const bodyParser = require('body-parser');
import dotenv from 'dotenv';
import fs from 'fs';


if (fs.existsSync('./.env')) {
    dotenv.config();
}
// Initializing server + websockets

var server = http.Server(app);
var socketServer = new socket(server);

app.use(express.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

// Begin servergi
server.listen(9091);