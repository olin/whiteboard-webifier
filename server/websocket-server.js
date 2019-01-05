var socket = require('socket.io');



module.exports = class websocketServer {
    constructor(server) {
        this.server = server;
        this.io = socket(this.server);
        
        // Setup websocket listening functions
        this.io.on('connection', function(socket) {
            socket.on('point-vals', function(data) {
                let authString = socket.handshake.headers.authorization;

                // An auth header must exist
                if (authString != null) {
                    let authStringDecoded = Buffer.from(authString.slice(6), 'base64').toString('ascii')

                    let expectedAuth = process.env.ID + ':' + process.env.PASSWORD

                    if (authStringDecoded === expectedAuth) {
                        socket.broadcast.emit('points', data);
                    } else {
                        socket.disconnect()
                    }
                }
            })
            console.log('Client connected.');
        });
    
        // On disconnect
        this.io.on('disconnect', function() {console.log('Client disconnected.')});
    }
}

