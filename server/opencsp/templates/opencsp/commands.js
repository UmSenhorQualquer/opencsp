

function activateMenu(menulink) {
	$('.left-menu li').not('.small-menu li a').removeClass('active');
	$('#'+menulink).addClass('active');
}

function showBreadcrumbs(breadcrumbs, label){
	var html = '';
	for(var i=0; i<breadcrumbs.length; i++){
		html = "<a href='#view-"+breadcrumbs[i][1]+"' onclick='"+breadcrumbs[i][2]+"' >"+breadcrumbs[i][0]+"</a>"
		html += " > ";
	}
	html += label;
	$('#content-breadcrumbs').html(html);
}

function LoadCurrentView(){
	var href = window.location.href;
	var anchor = href.substring( href.indexOf('#')+1);
	if( anchor.substring(0,5)!='view-' ) return;
	var paramsStartIndex = anchor.indexOf('|');
	if( paramsStartIndex<0) paramsStartIndex = paramsStartIndex.length;
	var view = anchor.substring(5, paramsStartIndex);
	var params = anchor.substring(paramsStartIndex+1).split('+');

{% for ifcode in views_ifs %}{{ ifcode|safe }}{% endfor %}	
}