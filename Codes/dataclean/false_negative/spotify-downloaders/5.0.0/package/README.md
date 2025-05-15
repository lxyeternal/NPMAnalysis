## Installation:

```sh
npm i spotify-downloaders
```
## Example Usage:

# Downloading
```js
const track = require('spotify-downloaders');

(async () => {
  const result = await spotify('https://open.spotify.com/track/1bEnIDpwKsyhDauHVoMz6t');
  console.log(result);
})();
```          
# Searching
```js
const search = require('spotify-downloaders');

(async () => {
  const result = await search('blue bird');
  console.log(result);
})();
```          