/*import { SMTPClient } from 'emailjs';

const client = new SMTPClient({
	user: 'userhuiuser@kedrns.com',
	password: 'L3IXGUz2im^3',
	host: 'mail.kedrns.com',
	ssl: true,
//        domain:''
        port:'25',
	authentication: ['PLAIN', 'LOGIN']
});

// send the message and get a callback with an error or details of the message that was sent
client.send(
	{
		text: 'i hope this works',
		from: 'you <userhuiuser@kedrns.com>',
		to: 'someone <maanka@kedrns.com.com>',
		subject: 'testing emailjs',
	},
	(err, message) => {
		console.log(err || message);
	}
);
*/
const os = require('os')
const nodemailer = require('nodemailer');
const smtp = nodemailer.createTransport({
  host: "mail.kedrns.com",
  port:25,
  tls: {rejectUnauthorized: false},
  auth: {
    user: "userhuiuser@kedrns.com",
    pass: `L3IXGUz2im^3`
  }
});

  var mailOptions = {
    from: os.hostname()+'@kedrns.com',
    to: 'debug@kedrns.com',
    subject: 'subjest',
    text: 'This is debug message'
  }

  smtp.sendMail(mailOptions, function (error, response) {
    if (error) {
      console.log(error);
      res.end("error");
    } else {
      console.log("Email sent ");
      res.end("sent");
    }
  });
