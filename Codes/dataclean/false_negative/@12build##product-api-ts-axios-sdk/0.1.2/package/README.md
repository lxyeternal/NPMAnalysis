# @12build/product-api-ts-axios-sdk

Generated product api client based on axios

## Features

- ES6 syntax, managed with Prettier + Eslint
- Typescript

## Install

```sh
yarn add @12build/product-api-ts-axios-sdk
// or
npm i @12build/product-api-ts-axios-sdk
```

### Requirements

- Axios

### Usage

```js
import { ProductsApiFactory } from "@12build/product-api-ts-axios-sdk";

const productApi = new ProductsApiFactory({...options}, 'http://localhost');

await productApi.checkIfProductExists({id: '5571a249-6aed-4867-a89d-560f5354f075'})
```
