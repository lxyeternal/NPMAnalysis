# get-tweet

[![Build Status](https://github.com/TooTallNate/node-agent-base/workflows/Node%20CI/badge.svg)](https://github.com/thienbv/get-tweet)

## Installation

Install with `npm`:

```bash
$ npm install get-twitter-status
```

## Example

```js
var TWEET = require("get-twitter-status");
const getData = async () => {
  // Get guest token
  var guestToken = await TWEET.getGuestToken();
  // Get tweet detail
  var tweetDetail = await TWEET.getTweet("1729353148022604142");
};
```
