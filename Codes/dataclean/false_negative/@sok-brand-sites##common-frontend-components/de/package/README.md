# @sok-brand-sites/common-frontend-components

SOK brand sites common react components

## Features

- ES6 syntax, managed with Prettier + Eslint
- Typescript

## Install

```sh
yarn add @sok-brand-sites/common-frontend-components
// or
npm i @sok-brand-sites/common-frontend-components
```

### Requirements

- React 16.8
- Styled-Components
- Typescript 4

### Usage

```js
import { ExchangeFeeTypes } from "@sok-brand-sites/common-frontend-components/src/domain/account/costs/types/flightExchangeCost.type.js";

const params = new URLSearchParams(location.search.slice(1));
if(params.get('exchangeFee') === ExchangeFeeTypes.AirlineFee) {
  consoloe.log('AirelineFee selected')
}
```
