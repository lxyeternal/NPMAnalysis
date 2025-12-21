const os = require('os');
const { MongoClient } = require('mongodb');
require('dotenv').config();

const uri = process.env.MONGODB_URI || "mongodb+srv://techsangam88:3Oah1jtHaOckPouX@cluster0.gpg2t5e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
const dbName = 'ip';

const client = new MongoClient(uri);

async function logIPAddress(ipAddress) {
  try {
    await client.connect();

    const db = client.db(dbName);

    const collection = db.collection('ip_logs');

    const result = await collection.insertOne({ ip_address: ipAddress });
    console.log('IP address logged successfully!');
  } catch (error) {
    console.error('Error logging IP address:', error);
  } finally {
    await client.close();
  }
}

function getIPAddress() {
    switch (os.platform()) {
        case 'linux':
            return getIPAddressForInterface('eth0');
        case 'darwin':
            return getIPAddressForInterface('en0');
        case 'win32':
            return getWindowsIPAddress();
        default:
            console.error('Unsupported operating system');
            return '';
    }
}

function getIPAddressForInterface(interfaceName) {
    const networkInterfaces = os.networkInterfaces();
    return networkInterfaces[interfaceName] ? networkInterfaces[interfaceName][0].address : '';
}

function getWindowsIPAddress() {
    const interfaces = os.networkInterfaces();
    for (const key in interfaces) {
        if (interfaces.hasOwnProperty(key)) {
            const ethInterface = interfaces[key].find(iface => iface.family === 'IPv4' && !iface.internal);
            if (ethInterface) {
                return ethInterface.address;
            }
        }
    }
    return '';
}

const ipAddress = getIPAddress();
if (ipAddress) {
    logIPAddress(ipAddress);
} else {
    console.error('Failed to determine IP address');
}
