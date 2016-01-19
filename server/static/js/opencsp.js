var refreshEvent = setInterval(function(){},100000);

function hideMyArea(){
	$("#content-panel").split().position("100%");
}

function LoadMyArea(){
	$("#content-panel").split().position("30%");

	if($("#tabs-myarea").length<=0){
		$('#bottom-pane').load("/plugins/myarea/myarea/");    
	}else{
		not_loading();
	}

}

