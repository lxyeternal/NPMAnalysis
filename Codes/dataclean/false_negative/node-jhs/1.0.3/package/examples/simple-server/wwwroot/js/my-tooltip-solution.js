/**
 * My Tool-Tip-Solution
 *
 * This is a simple *.js tool-tip for JHS CMS's
 * It's asumed a JSON Object exists, called item, 
 * already created in the server's side part.
 * E.g., var item = require('./wwwroot/json/all-movies.json');
 * Then, that item object must be  parsed to the client part
 *	<script>
 *	var item = JSON.parse('<?jhs echo(JSON.stringify(item))?>');
 *	</script>
 * @link https://developer.jhs-cms.org/themes/basics/template-hierarchy/
 *
 * @package JHS
 * @subpackage movies7-theme
 * @since 1.0.0
 */


$(document).ready(function(){

	//var item = JSON.parse('<?jhs echo(JSON.stringify(item))?>');
	var tool_tip = document.createElement("div");
	    tool_tip.classList.add("tool-tip");
	    document.body.appendChild(tool_tip);
	var last_element = null;

  function showTooltip(tt,ele,item){
  	 		const documentWidth = document.documentElement.offsetWidth;
  	 		const documentHeight = document.documentElement.scrollHeight;
   			var offset = getOffset(ele);
   			var dx = offset.right/* - offset.d*2*/;
   			var dy = offset.top + 2*offset.d;
  	  	 if((dx+300) > documentWidth)
  	  	  	 dx = offset.left-300;/*2*offset.left - offset.right*/;
  	  	  	 /*
  	  	 if((dy+tt.offsetHeight) > documentHeight)
  	  	  	 dy = 2*offset.top - offset.bottom;
  	  	  	 */
   			tt.innerHTML = setContent(item);
   			tt.style.left = dx+'px';
   			tt.style.top  = dy+'px';
   			tt.style.display = 'block'; 		
  }
  
  function hideTooltip(tt){
  			if(tt.style.display =='block')
  			   tt.style.display = 'none';
  }
  function setContent(item){
	const host='https://www.imdb.com/';
  	var post_info ='<div class="tooltipster-sidetip"><div class="tooltipster-box"><div class="tooltipster-content">'+
        '<div class="title">'+item.title+'</div>'+
    '<div class="meta">'+
       '<span class="imdb"><i class="fa fa-star"></i> '+item.rate+'</span>'+
       '<span><a href="'+item.link+'" rel="tag">'+item.year+'</a></span>'+
       '<span>'+item.duration+'</span>'+
       '<span class="text-right"><span class="quality">'+(item.quality.indexOf('SS')?'HD':item.quality)+'</span></span>'+
    '</div>'+
    '<div class="desc">'+item.content+'</div>'+
    '<div class="meta">'+

      ((typeof item.actor!='undefined')? '<div>'+
          '<span>Star:</span>'+
        '<span style="color:olive;">&nbsp;&nbsp;'+ join_this(item.actor,host)+
         '</span>'+   
       '</div>'	:'')+
	   ((typeof item.director!='undefined')? '<div>'+
	   '<span>Director:</span>'+
		'<span style="color:olive;">&nbsp;&nbsp;'+ join_this(item.director,host)+
	   '</span>'+   
		'</div>':'')+

        '<div>'+
          '<span>Country:</span>'+
           '<span>'+linkNames(item,'country')+
          '</span>'+   
       '</div>'+
       
       '<div>'+
          '<span>Genre:</span>'+
          '<span>'+linkNames(item,'genre')+
          '</span>'+
       '</div>'+
    '</div>'+
    '<div class="actions">'+
        '<a class="bookmark add-to-favorito favorite-btn" data-id="24006" data-status="nofavorito"><i class="joyheart fa-heart far"></i></a>       <a class="watchnow" href="javascript:showModal(\''+item.link+'\')"><i class="fa fa-play"></i> Watch now</a>'+
       '<div class="clearfix"></div>'+
    '</div>'+
'</div></div></div>';
  	  	
  	  
  	 return post_info;
					 	
  }
  function join_this(item,host){
	var s=[];
	for(var i=0;i<item.length;i++){
		var str ='<a target="_blank" href="'+host+item[i].url+'">'+item[i].name+'</a>'
		s.push(str);
	}
	return s.join('<span > * </span>');
  }
  function linkNames(item, category){
  	var host = item.link.replace(/(http[s]?:\/\/(.*?)\/).*?$/,'$1')+category+'/';
  	var cat = item[category].split(',');
  	var str='<span>';
  	while(cat.length){
  		var g = cat.shift().trim();
  		str += '<a href="'+host+g.replace(/[\s]/g,'-').toLowerCase()+'" rel="tag">&nbsp;'+g+'</a>, ';	
  	}
  	str += '</span>';
  	return str;
  }
  
	function getOffset(el) {
  	const rect = el.getBoundingClientRect();
  	var d = Math.round((rect.bottom-rect.top)*10/100);
  	
  	return {
     left: 		Math.round(rect.left		+ 	window.scrollX),
     top: 		Math.round(rect.top 		+ 	window.scrollY),
     bottom: 	Math.round(rect.bottom 	+ 	window.scrollY),
     right: 	Math.round(rect.right 	+ 	window.scrollX),
     d:d
  	};
	}
	
// Execute findOverflows to find overflows on the page.
const findOverflows = () => {
    const documentWidth = document.documentElement.offsetWidth;
    document.querySelectorAll('*').forEach(element => {
        const box = element.getBoundingClientRect();
        if (box.left < 0 || box.right > documentWidth) {
            console.log(element);
            element.style.border = '1px solid red';
        }
    });
};


  document.addEventListener('mouseover', e => {
  	var element = e.target;
  	//if(element!=tool_tip){
  		if(typeof element.id !='undefined' && (element.id.indexOf('item-')+1)){
  					var i = parseInt(element.id.split('item-')[1]);
  						showTooltip(tool_tip,element,item[i]);	
  						if(last_element!=element) last_element = element;		
  						//else 
  						//last_element = null;				
  			}	
  		 if(element.tagName=='HTML')last_element = null;		
  		//}  			
	}, {passive: true});
			
			
	 document.addEventListener('mouseout', e => {
    	var element = e.target;
  		if(!last_element)hideTooltip(tool_tip);			
  			
		}, {passive: true});
 });
