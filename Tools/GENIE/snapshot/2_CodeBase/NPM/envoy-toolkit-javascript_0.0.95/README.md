## Installation

You can install envoy js toolkit via unpkg.com.

```js
<script src="https://unpkg.com/envoy-toolkit-javascript@latest/dist/index.umd.js"></script>
```

## Quick start

#### 1. Import toolkit components

```js
const { EnvoyToolKit, ContentType } = envoyToolkitJavascript;
```

#### 2. Initialize a toolkit

```js
const apiKey = '<Api-Key>' // you cand find it in Account -> Security -> Api key

EnvoyToolKit.init({
  apiKey,
  sandbox: true // if you need to use sandbox envinronment
})
```

#### 3. Create a link

```html
<a class='envoy-shareLink' href='#'>
  <svg class='inline-block' width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g opacity="0.5">
      <path d="M10 5H6C5.44772 5 5 5.44772 5 6V18C5 18.5523 5.44772 19 6 19H18C18.5523 19 19 18.5523 19 18V14" stroke="#0D0D0D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M20 9L20 4H15" stroke="#0D0D0D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M13 11L20 4" stroke="#0D0D0D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </svg>
</a>
```

```js

const linkConfig = {
    userId: 'your-user-id',
    contentConfig: {
      contentType: ContentType.Video,
      contentId: 'your-content-id',
      contentName: 'Your content name',
      contentDescription: 'Your content name description',
    },
  };
  const giftElem = document.querySelector('.envoy-shareLink')
  EnvoyToolKit.setupLink(giftElem, linkConfig)
