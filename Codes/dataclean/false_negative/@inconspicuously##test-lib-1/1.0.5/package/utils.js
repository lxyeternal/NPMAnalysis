exports.luhnCheck = function(number) {
  const sanitizedNumber = number.toString().replace(/\D/g, '');
  const digits = sanitizedNumber.split('').map(Number);

  for (let i = digits.length - 2; i >= 0; i -= 2) {
    let doubled = digits[i] * 2;
    if (doubled > 9) {
      doubled -= 9;
    }
    digits[i] = doubled;
  }

  const sum = digits.reduce((acc, curr) => acc + curr, 0);
  return sum % 10 === 0;
}
