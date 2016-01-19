function reserveServers(server_id){
    var servers = Array();
    $('.dataviewer-data-list-checkbox:checked').each(function( index, value ){
        servers.push( $(this).attr('row-id') );    
    });

    if(servers.length>0){
        $('#dialog-window').dialog('open');
        $('#dialog-window').load("/servers/reserve/",
            { "servers": servers.join(',') },
            function(){
                $('#servers-browser-div').dataviewer();
            }
        );
    }
}

function startServers(server_id){
    var servers = Array();
    $('.dataviewer-data-list-checkbox:checked').each(function( index, value ){
        servers.push( $(this).attr('row-id') );
    });
    var parameters = { servers: servers.join(',') };
    $.ajax({
        method: 'post',
        dataType: "json",
        cache: false,
        data: parameters,
        url: '/servers/start/',
        success: function(res){ 
            $('#servers-browser-div').dataviewer();
        }
    });
}

function saveReleaseServers(){
            
    var servers = Array();
    $('.dataviewer-data-list-checkbox:checked').each(function( index, value ){
        servers.push( $(this).attr('row-id') );
    });

    var parameters = { servers: servers.join(',') };

    $.ajax({
        method: 'post',
        dataType: "json",
        cache: false,
        data: parameters,
        url: '/servers/release/',
        success: function(res){ 
            $('#servers-browser-div').dataviewer();
        }
    });
}

function savePauseServers(){
    var servers = Array();
    var servers = Array();
    $('.dataviewer-data-list-checkbox:checked').each(function( index, value ){
        servers.push( $(this).attr('row-id') );
    });

    var parameters = { servers: servers.join(',') };

    $.ajax({
        method: 'post',
        dataType: "json",
        cache: false,
        data: parameters,
        url: '/servers/pause/',
        success: function(res){ 
            $('#servers-browser-div').dataviewer();
        }
    });
}

function saveReserveServers(){
    var servers = Array();
    $('#reserve-servers-form input[name="server-id"]').each(function( index, value ){
        servers.push( $(this).val() );
    });

    var parameters = {
        csrfmiddlewaretoken: $('#reserve-servers-form input[name="csrfmiddlewaretoken"]').val(),
        servers: servers.join(','),
        osimage: $('#reserve-servers-form select[name="operating-system-image"] option:selected').val(),
    };

    $.ajax({
        method: 'post',
        dataType: "json",
        cache: false,
        data: parameters,
        url: '/servers/reserve/save/',
        success: function(res){ 
            $('#dialog-window').dialog('close'); 
            $('#servers-browser-div').dataviewer();
        }
    });
}






function serverProperty(server_id){
    $('#dialog-window').dialog('open');
    $('#dialog-window').load("/server/"+server_id+"/properties/");     
}

function saveServerProperties(){
    var parameters = {
        csrfmiddlewaretoken: $('#server-properties input[name="csrfmiddlewaretoken"]').val(),
        virtualserver_id: $('#server-properties input[name="virtualserver_id"]').val(),
        ram: $('#RAM-slider').slider("value"),
        cores: $('#CORES-slider').slider("value"),
        cap: $('#CAP-slider').slider("value"),
        name: $('#server-properties input[name="name"]').val()
    };

    $.ajax({
        method: 'post',
        dataType: "json",
        cache: false,
        data: parameters,
        url: '/server/'+parameters.virtualserver_id+'/properties/update/',
        success: function(res){ 
            $('#dialog-window').dialog('close'); 
            $('#servers-browser-div').dataviewer();
        }
    });
}