# [discordjs-invites](https://discord.gg/luppux)

> **Track the invites in your servers to know who invited who and with which invite!**

#
### ❔ [Support](https://discord.gg/luppux)
### 📂 [NPM](https://npmjs.com/discordjs-invites)
### 📝 [Github](https://github.com/Bes-js/discordjs-invites)

#
# Installation

```bash
npm i discordjs-invites
```
#
# Quick Example
 
**Example For CommonJS**
```js
/* Importing The Package */
const InviteManager = require('discordjs-invites');
const invClient = new InviteManager(client); // client = Discord.Client();

```
#
**Events**
```js
/* Guild Member Join Event */
client.on("memberJoin",async(member,inviter,invite) => { });

/* Guild Member Leave Event */
client.on("memberLeave",async(member,inviter,invite) => { });
```
#
**Functions**
```js
const InviteManager = require('discordjs-invites');
const { Client } = require("discord.js");
const invClient = new InviteManager(client);

invClient.inviteAdd(guildId, user); /* <null> */
invClient.inviteRemove(guildId, user); /* <null> */
invClient.getMemberInvites(guildId, user); /* <Object> */
invClient.getGuildInvites(guildId, limit); /* <Array> - limit = min 1 / max 50 / default 10 */
```
#
**Example Usage;**
```js
const InviteManager = require('discordjs-invites');
const { Client } = require("discord.js");
const invClient = new InviteManager(client); // client = Discord.Client();


/* Join Event */

client.on("memberJoin", async function(member, inviter, invite) {
if(!inviter) {
  console.log(`${member.user.username} joined the server, but I couldn't find out who was invited.`);
} else if(member.id == inviter.id) {
  console.log(`${member.user.username} Joined the server by his own invitation!`);
}else if(member.guild.vanityURLCode == inviter) {
  console.log(`${member.user.username} Joined Server Using Vanity URL!`);
} else {
  invClient.inviteAdd(member.guild.id, inviter);
  console.log(`${member.user.tag} Joined the server! inviter ${inviter.username}`);
};
});

/* Leave Event */

client.on("memberLeave",async(member,inviter,invite) => { 
if(!inviter) {
 console.log(`${member.user.tag} Lefted the server, but I couldn't find out who was invited.`);
} else if(member.id == inviter.id) {
 console.log(`${member.user.tag} Lefted the server by his own invitation!`);
} else if(member.guild.vanityURLCode == inviter) {
 console.log(`${member.user.tag} Lefted Server Using Vanity URL!`);
} else {
 invClient.inviteRemove(member.guild.id, inviter);
 console.log(`${member.user.tag} Lefted the server! inviter ${inviter.tag}`);
};
});


client.login("your secret bot token 👻")
```
**[discordjs-invites](https://discord.gg/luppux) Also Supports TypeScript And EsModule 🥳!**

#
# Credits
 
**Made by [FiveSoBes](https://github.com/Bes-js), [Relivent](https://github.com/Relivent) And [Luppux Development](https://github.com/Luppux)**


# Contact & Support & Donate
<a href="https://www.buymeacoffee.com/beykant" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" width="120px" height="30px" alt="Buy Me A Coffee"></a>

[![Discord Banner](https://api.weblutions.com/discord/invite/luppux/)](https://discord.gg/luppux)
