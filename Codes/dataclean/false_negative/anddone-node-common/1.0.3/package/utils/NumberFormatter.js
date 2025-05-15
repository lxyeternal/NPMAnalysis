
// This class used to PhoneNumber formate eg.console.log (format("{0:###-#-##-####}", 1234567898));

function format(formatString) {
    var result = '';
    for (var i = 0; i < formatString.length;) {
        if (formatString[i] == '}') {
            i++;
            if (formatString[i] == '}') {
                result += '}';
                i++;
                continue;
            }
            throw new Error("Unescaped substitution");
        }
        if (formatString[i] == '{') {
            var spec = '';
            i++;
            if (formatString[i] == '{') {
                result += '{';
                i++;
                continue;
            }
            for (; i < formatString.length;) {
                if (formatString[i] == '}') {
                    break;
                }
                spec += formatString[i++];
            }
            if (i == formatString.length) {
                throw new Error("Unterminated substitution");
            }
            i++;
            var alignTokenLoc = spec.indexOf(',');
            var specTokenLoc;
            var alignVal = 0;
            if (alignTokenLoc > 0) {
                specTokenLoc = spec.indexOf(':');
                if (specTokenLoc > 0) {
                    if (alignTokenLoc < specTokenLoc) {
                        alignVal = spec.substr(alignTokenLoc + 1, specTokenLoc - alignTokenLoc - 1);
                        spec = spec.substr(0, alignTokenLoc) + spec.substr(specTokenLoc);
                    }
                } else {
                    alignVal = spec.substr(alignTokenLoc + 1);
                    spec = spec.substr(0, alignTokenLoc);
                }
            }

            specTokenLoc = spec.indexOf(':');
            var fieldName, formatSpec;
            if (specTokenLoc > 0) {
                fieldName = spec.substr(0, specTokenLoc);
                formatSpec = spec.substr(specTokenLoc + 1);
            } else {
                fieldName = spec;
                formatSpec = null;
            }
            var val = getValue(arguments, fieldName);

            if (typeof (val) === 'number') {
                result += align(formatNumber(val, formatSpec), alignVal);
            }
        } else {
            result += formatString[i++];
        }
    }
    return result;
}

function align(str, val) {
    str = str || '';
    if (val < 0) {
        return padRight(str, ' ', Math.abs(val));
    } else if (val > 0) {
        return padLeft(str, ' ', val);
    }
    return str;
}

function padRight(str, char, totalWidth) {
    while (str.length < totalWidth) {
        str = str + char;
    }
    return str;
}

function padLeft(str, char, totalWidth) {
    while (str.length < totalWidth) {
        str = char + str;
    }
    return str;
}

function getValue(args, fieldName) {
    var fieldIndex = parseInt(fieldName);
    if (fieldIndex.toString() === fieldName) {
        return args[fieldIndex + 1];
    } else {
        var parts = splitFieldName(fieldName);
        var root = args[1];
        for (var i = 0; i < parts.length; i++) {
            var part = parts[i];

            if (part.length >= 1 && part[0] == '?') {
                if (typeof (root) == 'undefined') {
                    return undefined;
                } else {
                    part = part.substr(1);
                }
            }

            if (part.length >= 1 && part[0] == '[') {
                part = part.substr(1, part.length - 2);
                var strMatch = part.match(/^['"](.*)['"]$/);
                if (strMatch) {
                    root = root[strMatch[1]];
                }
                else if (part < 0) {
                    part = -part;
                    root = root[root.length - part];
                } else {
                    root = root[part];
                }
                continue;
            }

            root = root[part];
        }
        return root;
    }
}


function splitFieldName(fieldName) {
    var results = [];
    var part = '';
    for (var i = 0; i < fieldName.length;) {
        if (fieldName[i] == '.') {
            results.push(part);
            part = '';
            i++;
            continue;
        }

        if (fieldName[i] == '[') {
            results.push(part);
            part = '[';
            i++;
            continue;
        }

        part += fieldName[i++];
    }
    results.push(part);
    return results;
}

function formatNumber(num, format) {
    format = format || "0";

    var hex = format.match(/^([xX])([0-9]*)$/);
    if (hex) {
        var str = num.toString(16);
        if (hex[1] == 'x') {
            str = str.toLowerCase();
        } else {
            str = str.toUpperCase();
        }
        var width = parseInt(hex[2]);
        str = padLeft(str, '0', width);
        return str;
    }

    var negative = false;
    if (num < 0) {
        num = -num;
        negative = true;
    }

    var addPositiveSign = false;
    if (format.match(/^\+/)) {
        format = format.substr(1);
        addPositiveSign = true;
    }

    var formatParts = format.split('.');
    var formatBeforeDecimal = formatParts[0];
    var wholeNumber = Math.floor(num);
    var decimalVal = num - wholeNumber;
    var result = '';
    var wholeNumberStr = wholeNumber.toString();
    var formatIdx, numberIdx;

    // format whole number part
    for (formatIdx = formatBeforeDecimal.length - 1, numberIdx = wholeNumberStr.length - 1; numberIdx >= 0 || formatIdx >= 0; formatIdx--) {
        if (formatIdx < 0 && numberIdx >= 0) {
            result = wholeNumberStr[numberIdx--] + result;
            continue;
        }

        if (formatBeforeDecimal[formatIdx] == '0' || formatBeforeDecimal[formatIdx] == '#') {
            if (numberIdx >= 0) {
                result = wholeNumberStr[numberIdx--] + result;
            } else {
                if (formatBeforeDecimal[formatIdx] == '#') {
                    break;
                }
                result = '0' + result;
            }
            continue;
        }

        result = formatBeforeDecimal[formatIdx] + result;
    }
    result = result.replace(/^[^0-9]+/, '');

    // format decimal part
    if (formatParts.length > 1) {
        var formatAfterDecimal = formatParts[1];
        var decimalValStr = decimalVal.toString().substr(2);

        result += '.';
        for (formatIdx = 0, numberIdx = 0; formatIdx < formatAfterDecimal.length; formatIdx++) {
            if (formatAfterDecimal[formatIdx] == '0' || formatAfterDecimal[formatIdx] == '#') {
                if (numberIdx < decimalValStr.length) {
                    result += decimalValStr[numberIdx++];
                } else {
                    if (formatAfterDecimal[formatIdx] == '#') {
                        break;
                    }
                    result += '0';
                }
            } else {
                result += formatAfterDecimal[formatIdx];
            }
        }
    }

    if (result[result.length - 1] == '.') {
        result = result.substr(0, result.length - 1);
    }

    if (negative) {
        result = '-' + result;
    }
    if (!negative && addPositiveSign) {
        result = '+' + result;
    }

    return result;
}

exports.format = format;