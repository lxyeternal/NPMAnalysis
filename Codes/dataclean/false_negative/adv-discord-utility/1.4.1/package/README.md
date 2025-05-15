# Installation

```console
npm i adv-discord-utility@latest --save
```


# Usage

```js
const { Client } = require('discord.js'),
client = new Client({ intents: 32767 });
const { DiscordUtilities } = require('adv-discord-utility');
const token = 'PASTE_TOKEN_HERE'


client.on('ready', () => {
console.log(`${client.user.tag} started`)
DiscordUtilities(client)
DiscordUtilities.pubAll('<your_message>')
})


client.login(token).catch((err) => console.log(err))
```