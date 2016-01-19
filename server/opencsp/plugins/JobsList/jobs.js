function jobFiles(pk){
    loading();
    $('#dialog-window').html('');
    $('#dialog-window').dialog('open');
    $('#dialog-window').load("/plugins/jobslist/check_output_files/"+pk+"/",function() {
        not_loading();
        $(this).scrollTop($(this)[0].scrollHeight);
    });
}

function jobOutput(pk){
    loading();
    $('#dialog-window').html('');
    $('#dialog-window').dialog('open');
    $('#dialog-window').load("/plugins/jobslist/check_job_output/"+pk+"/",function() {
        not_loading();
        $(this).scrollTop($(this)[0].scrollHeight);
    });
}

function jobOpen(application, pk){
    $('#top-pane').load("/load/"+application+"/", {job: pk});
}

function stopJob(pk){
    loading();
    $.ajax({
        url: "/plugins/jobslist/kill_job/"+pk+"/",
        success: function(){
            $('#alljobs-browser-div').dataviewer();
            not_loading();
        }
    });
}



