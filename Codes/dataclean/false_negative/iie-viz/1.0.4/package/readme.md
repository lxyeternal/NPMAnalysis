#INSTALL
npm install iie-viz --save

#EXAMPLE

##HTML
    <div id="qipao"></div>

##JS
    var qipao = require('iie-viz').qipao;
    var o = {
        container:"qipao",
        id:"svg_name",
        colorlist:["red","green","orange","blue","gray"],
    };
    var qipao = new qipao(o);
    var i = 0;
    var add = function(){
        var t={};
        t.r = random(30,100);
        t.dr = 30;
        t.text = "iPhone";
        t.id = "id" + i++;
        t.color = i<2?"red":null;
        t.text_color = "white";

        c.addCircle(t);
    }