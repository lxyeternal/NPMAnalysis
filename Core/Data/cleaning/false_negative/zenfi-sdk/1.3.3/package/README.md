# Zenfi JavaScript SDK

![](https://img.shields.io/github/actions/workflow/status/zenfi/js-sdk/tests.yml?branch=main)
![](https://img.shields.io/badge/license-MIT-blue?style=flat)

JavaScript SDK for Zenfi partners. Useful to:
* Auto-fill inputs with user data, making forms completion easier.
* Track lead events (register, clicks, etc).

## Usage

### NodeJS

Install with npm or yarn:

```bash
npm install --save zenfi-sdk
```

### Browser

Add the following script to your project:

```html
<!-- Latest version -->
<script src="https://cdn.jsdelivr.net/gh/zenfi/js-sdk@main/dist/index.js" type="text/javascript"></script>

<!-- Or specify a version -->
<script src="https://cdn.jsdelivr.net/gh/zenfi/js-sdk@v1.3.3/dist/index.js" type="text/javascript"></script>

<!-- This will export a variable named "ZenfiSDK": -->
<script type="text/javascript">
  var zenfi = new ZenfiSDK(...args);
  zenfi.fillTargets();
</script>
```


## API

### `new ZenfiSDK(...)`

Creates a new instance of the Zenfi SDK.

**Parameters**

| Parameter | Type | Default value | Description |
| --------- | ---- | - | ----------- |
|`cookiesDomain`|String|-|The [domain space](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie) where the cookies will be available. When this value is empty, cookies will be only accessible in the current domain / subdomain.|
|`partnerName`|String|-|The name of the platform which implements this code. This parameter is required to send events to the Zenfi API.|
|`targets`|[Object]|`[]`|The list of html elements and their configuration to be filled.|
|`targets.dataKey`|String|-|The name of the key in the `leadInfo` object which contains the information to be filled.|
|`targets.selector`|String \| Function|-|The css selector to find the element in the DOM. If a function is passed, it will receive an object with `{ dataKey, strategy, value }` as param properties and must return a string with the css selector.|
|`targets.strategy`|Enum(`value` \| `text` \| `click`)|`value`|Indicates the type of strategy to fill the DOM element. Possible values are: `value`: sets the value property of an input, `text`: puts the content inside the HTML tag as text, used for `<div />`s, `click`: triggers a click on the DOM element.|
|`targets.beforeAction`|Function|-|An optional function that is executed before the target is filled. It will receive an object with `{ selector, strategy, value }` properties.|
|`targets.afterAction`|Function|-|An optional function that is executed after the target is filled. It will receive an object with `{ element, selector, strategy, value }` properties (`element` is the DOM node being filled).|


**Example**

```javascript
const zenfi = new ZenfiSDK({
  partnerName: 'credifast',
  cookiesDomain: 'credifast.com',
  targets: [
    {
      dataKey: 'name',
      strategy: 'html',
      selector: '#nameInput',
    },
    {
      dataKey: 'email',
      strategy: 'value',
      selector: ({ dataKey }) => `#${dataKey}Input`,
      beforeAction: () => console.log('before filling info'),
      afterAction: ({ element }) => element.classList.add('changed'),
    },
  ],
});
```

### `.fetchData()`

Fetches the lead information from the Zenfi API.

**Parameters**

This function takes no parameters.

**Example**

```javascript
const zenfi = new ZenfiSDK();
await zenfi.fetchData();

console.log(zenfi.leadInfo);
/*
Prints:

{
  name: 'Chewbacca',
  email: 'chewy@lucasfilm.com'
}

*/
```

### `.fillTargets()`

Auto-fills the labels and inputs specified in the `targets` configuration.
It also fetches the lead information from the Zenfi API, if information is not available yet.

**Parameters**

This function takes no parameters.

**Example**

```javascript
const zenfi = new ZenfiSDK({
  targets: [
    {
      dataKey: 'name',
      selector: '#nameInput',
      strategy: 'html',
    },
    {
      dataKey: 'email',
      strategy: 'value',
      selector: ({ dataKey }) => `#${dataKey}Input`,
      afterAction: ({ element }) => element.classList.add('changed'),
    },
  ]
});
await zenfi.fillTargets();
// It will fill the #nameInput and #emailInput nodes automatically.
```

### `.trackConversion(name, properties)`

Sends a conversion event to the Zenfi API (the user is moving forward in the funnel): `https://api.zenfi.mx/webhooks/leads/:partner/converted`.

**Parameters**

| Parameter | Type | Description |
| --------- | ---- | ----------- |
|`name`|String|Any descriptive name for the event to be tracked (eg. `register`, `click`, `addToCart`).|
|`properties`|Object|Any data related with the event to be tracked.|


**Example**

```javascript
zenfi.trackConversion('addToCart', {
  price: 100,
  amount: 2,
});
// It will track a "addToCart" event
```

### `.trackAbortion(name, properties)`

Sends an abortion event to the Zenfi API (the user was rejected and can not move forward in the funnel): `https://api.zenfi.mx/webhooks/leads/:partner/aborted`.

**Parameters**

| Parameter | Type | Description |
| --------- | ---- | ----------- |
|`name`|String|Any descriptive name for the event to be tracked (eg. `rejected`, `declinedOffer`).|
|`properties`|Object|Any data related with the event to be tracked.|


**Example**

```javascript
zenfi.trackConversion('declinedOffer', {
  reason: 'User got a better interest rate elsewhere'
});
// It will track a "declinedOffer" event
```

### `.trackPageView()`

Sends an conversion event with name "PageView" to the Zenfi API. It includes metadata about the visited URL: `href`, `hash`, `search`, `protocol`, `hostname` and `pathname`.

**Parameters**

This function takes no parameters.


**Example**

```javascript
zenfi.trackPageView();
// It will track a "PageView" event
```

### `.initPageViewsTracking()`

Starts a listener that tracks page view events automatically.

**Parameters**

This function takes no parameters.


**Example**

```javascript
zenfi.initPageViewsTracking();
// Listens to url changes and sends events
```


## License

MIT
