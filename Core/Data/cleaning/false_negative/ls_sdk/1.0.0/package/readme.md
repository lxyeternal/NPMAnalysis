# LEDGERSWARM SDK

> SDK for triggering actions on the RLN 

## Prerequisites

This project requires NodeJS (developed on v18) and NPM.
[Node](http://nodejs.org/) and [NPM](https://npmjs.org/) are really easy to install.
To make sure you have them available on your machine,
try running the following command.

```sh
$ npm -v && node -v
6.4.1
v8.16.0
```

## Table of contents

- [Project Name](#project-name)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [License](#license)

## Getting Started

Set up a new nodejs project in your development environment and install the library as follows

```sh
$ npm install @ledgerswarm/ls_sdk
```

## Usage

```js
const LS = require ('@ledgerswarm/ls_sdk')
const INSTANCE = "demo" // replace with your instance name
const ls = new LS(INSTANCE+"apiserver.setllabs.io", "USERNAME", "PASSWORD");

async function testledgerswarm(){

    // Create an new transaction on the RLN

    console.log('[create]')
    
    res = await ls.create({
        "id": "optional-id-for-whole-group-of-pac008s",
        "from": "Test-participant-1",
        "groups": [
            {
            "id": "optional-id-for-this-pac008-max35",
            "transactions": [
                {
                "id": "optional-id-for-txn-max35",
                "amount": 18.5,
                "currency": "USD",
                "creditor": {
                    "account": "Use a valid IBAN unless isAddress is true",
                    "agent": "Use a valid BIC",
                    "isAddress": false
                },
                "debtor": {
                    "account": "Use a valid IBAN unless isAddress is true",
                    "agent": "Use a valid BIC",
                    "isAddress": false
                }
                }
            ]
            }
        ]
    })
    console.log(res)

    // Query balances on the RLN

    console.log('[Balance]')

    res = await ls.balance({
        walletId:1
    }) 
    console.log(res);

    // Query transactions on the RLN

    console.log('[Transactions]')

    res = await ls.transactions({
        incompleteOnly:true, 
        limit:10, 
        offset:0
    })
    console.log(res);

    // Query the RLN for any transactions waiting for approval

    console.log('[Approval List]')

    res = await ls.approvalList()
    console.log(res);

    // Change the status of an transaction to APPROVE or REJECT

    console.log('[Approval Status]')

    res = await ls.approvalStatus({
        "id": 2,
        "status": "APPROVE"
    })
    console.log(res);

    // Query the list of instruments that are being auto approved

    console.log('[Autoapprove List]')

    res = await ls.autoapproveList({})
    console.log(res);

    // Set up an instrument for autoapprove (set to 0 to turn it off)

    console.log('[autoapprove]')

    res = await ls.autoapprove({
        username:"USERNAME", 
        assetCode:"USD", 
        maxAutoApprove:2000
    })
    console.log(res);
}

testledgerswarm()
```



## License

[MIT License](https://andreasonny.mit-license.org/2019) 