# @12build/account-api-ts-axios-sdk

Generated account api client based on axios

## Features

- ES6 syntax, managed with Prettier + Eslint
- Typescript

## Install

```sh
yarn add @12build/account-api-ts-axios-sdk
// or
npm i @12build/account-api-ts-axios-sdk
```

### Requirements

- Axios

### Usage

```js
import { ProductsApiFactory } from "@12build/account-api-ts-axios-sdk";

const accountApi = new AccountsApiFactory({...options}, 'http://localhost');

await accountApi.addAccount({ data: { type: 'accounts', attributes: { name: 'foo' } } });
```
