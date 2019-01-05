var socket = require('socket.io');

module.exports = class websocketServer {
    constructor(server) {
        this.server = server;
        this.io = socket(this.server);
        
        // Setup websocket listening functions
        this.io.on('connection', function(socket) {
            
            socket.on('point-vals', function(data) {
                socket.broadcast.emit('points', data)
            })
            console.log('Client connected.')
        });
    
        // On disconnect
        this.io.on('disconnect', function() {console.log('Client disconnected.')});
    }
}

