const Web3Abi = require("web3-abi")

function test ()
{
    var a = {address: '0xDF975d7409A9F44fBAF430baaD0eB846c54D90ee',
    privateKey: '0x1f92fca661bdf9581dbf6fbdcb6fc66442e2dab2b0ba26f49cbb46b4eff4dba2',

    }
    Web3Abi.add(a)

}
test()