function loading(){ $("#loading-label").show(); };
function not_loading(){ $("#loading-label").hide(); }


function show_msgs(){ $('#dialog-msg').dialog('open'); };
function update_msgs_icon(){ 
	var size = $('#dialog-msg .alert .msg-text').size();
	if( size==0 ){
		$('.header-toolbox #msg').remove();
		$('#dialog-msg').dialog('close');
	}else{
		var html = size;
		$('.header-toolbox #msg div').html(html);
	}
	
	var errors_size = $('#dialog-msg .alert-danger .msg-text').size();
	if(errors_size>0)
		$('.header-toolbox #msg div').addClass('system-msgs-icon-error');
	else 
		$('.header-toolbox #msg div').removeClass('system-msgs-icon-error');
};


function increment_msg_icon(){
	if( $('.header-toolbox #msg').length==0 ){
		$('.header-toolbox').append("<a href='javascript:show_msgs();' id='msg' style='display:none;' ><div class='system-msgs-icon' >0</div></i></a>")
		$('.header-toolbox #msg').fadeIn('slow');
		
		$('.header-toolbox #msg div').tooltip({
			title: function(){
				var html = '';

				$('#dialog-msg .alert').each(function(){
					var msg_text =  $(this).children('.msg-text').text();
					msg_text = msg_text.substring(0, ((msg_text.length>150)?150:msg_text.length) );

					if( $(this).hasClass('alert-danger') ){
						html += '<p style="color:red">'+msg_text+' ...</p>';
					}else{
						html += '<p>'+msg_text+' ...</p>';
					};
				});
				return html;
			},
			placement: 'bottom',
			html: true
		});
	}

	update_msgs_icon();
}

function success_msg(msg){
	var alert_elem = $('#dialog-msg').prepend('<div class="alert alert-success" role="alert"><a href="#" class="close" data-dismiss="alert">&times;</a><div class="msg-text" >'+msg+'</div></div>');
	$(".alert").alert();
	
	increment_msg_icon();
	$(alert_elem).on('close.bs.alert', function(){setTimeout("update_msgs_icon();", 500);});     
};

function error_msg(msg){
	var alert_elem = $('#dialog-msg').prepend('<div class="alert alert-danger" role="alert"><a href="#" class="close" data-dismiss="alert">&times;</a><i style="color:#a94442" class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></i> <i class="sr-only">Error:</i><pre class="msg-text" >'+msg+'</pre></div>');
	$(".alert").alert();
	
	increment_msg_icon();
	$(alert_elem).on('close.bs.alert', function(){setTimeout("update_msgs_icon();", 500);});
};



$(function(){
	$('body').append("<div id='dialog-msg' class='dialog' style='display:none;' title='Messages'></div>");
	$('#dialog-msg').dialog({
        autoOpen: false,
        show: 'slideDown',
        width: '80%',
        height: 600,
        position: {at: "top"},
        draggable: false
    });
});