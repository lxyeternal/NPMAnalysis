# random-vouchercode-generator

Generate voucher codes easily

## Usage
```javascript

const voucher_codes =  require('random-vouchercode-generator');
const voucher = voucher_codes.generate({
	length: 6, 
	count: 1, 
	charset: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
})[0];
```