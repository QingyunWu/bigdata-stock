// import http dependency
var http = require('http')
var redis = require('redis')
var express = require('express')
var socketio = require('socket.io')
//minimist is similar to agrsparse
var argv = require('minimist')(process.argv.slice(2))
var redis_port = argv['redis_port']
var redis_host = argv['redis_host']
var subscribe_channel = argv['subscribe_channel']


//create an express() application
//express is to display html
var app = express()
var server = http.createServer(app);

var io = socketio(server)

//create redis client
var redisClinet = redis.createClient(redis_port, redis_host)
console.log('Subscribe to redis channel %s', subscribe_channel)
redisClinet.subscribe(subscribe_channel)

// when msg happens, do sth
redisClinet.on('message', function(channel, message) {
	console.log('message received %s', message)
	io.sockets.emit('data', message)
});


// setup express webapp routing
app.use(express.static(__dirname + '/public'))
app.use('/socket.io', express.static(__dirname + '/node_modules/socket.io/lib'))
app.use('/jquery', express.static(__dirname + '/node_modules/jquery/dist'))
app.use('/smoothie', express.static(__dirname + '/node_modules/smoothie'))
server.listen(3000)

 console.log('server started at port 3000')
