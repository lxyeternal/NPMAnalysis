# web3-provider-patchers

web3-provider-patchers is a library that provides advanced patching capabilities for the web3-provider-engine library. It enables you to customize your Ethereum provider by adding additional functionalities like filtering and wallet interactions.

## Features

- Apply filter patcher to handle event filtering efficiently.
- Apply wallet patcher for secure wallet interactions (optional).
- Simplify integration with Ethereum networks using Infura.
- Improved control over your Ethereum provider.

## Installation

`npm install web3-provider-patchers`

### Usage
Here's an example of how you can set up a custom Ethereum provider using web3-provider-patchers:

1. Install the required libraries:

`npm install web3-provider-engine web3 eth-json-rpc-infura`

2. Create a main.js file with the following code:
```
const Web3 = require('web3');
const Web3ProviderEngine = require('web3-provider-engine');
const FilterSubprovider = require('web3-provider-engine/subproviders/filters');
const RpcSubprovider = require('web3-provider-engine/subproviders/rpc');
const ProviderPatchers = require('web3-provider-patchers');
const createInfuraMiddleware = require('eth-json-rpc-infura');

// Configure the Infura middleware
const infuraMiddleware = createInfuraMiddleware({
  projectId: 'YOUR_INFURA_PROJECT_ID',
  projectSecret: 'YOUR_INFURA_PROJECT_SECRET', // Optional: Only required for some networks
});

// Create a Web3ProviderEngine instance
const engine = new Web3ProviderEngine();

// Add the Infura middleware
engine.addProvider(infuraMiddleware);

// Apply filter patcher to the engine
ProviderPatchers.applyFilterPatcher(engine);

// Add RPC subprovider
engine.addProvider(new RpcSubprovider({
  rpcUrl: 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID', // Replace with your Infura URL
}));

// Start the engine
engine.start();

// Create a Web3 instance using the custom provider
const web3 = new Web3(engine);

// Example usage...
Replace 'YOUR_INFURA_PROJECT_ID' and 'YOUR_INFURA_PROJECT_SECRET' with your actual Infura project credentials.
```
3. Run the main.js script:

`node main.js`