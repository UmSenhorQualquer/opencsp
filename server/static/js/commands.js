function runApplist(){
	loading();
	activateMenu('menu-applist');
	showBreadcrumbs([], 'Applications');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/applist/applist/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runApplistLoadjob(application,job){
	loading();
	activateMenu('menu-applist');
	showBreadcrumbs([['Applications', 'applist', 'runApplist();']], 'Application parameters');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/applist/loadjob/"+application+"/"+job+"/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runApplistLoad(application){
	loading();
	activateMenu('menu-applist');
	showBreadcrumbs([['Applications', 'applist', 'runApplist();']], 'Application parameters');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/applist/load/"+application+"/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runJobslistBrowsejobs(){
	loading();
	activateMenu('menu-jobslist');
}

function runJobslist(){
	loading();
	activateMenu('menu-jobslist');
	showBreadcrumbs([], 'Jobs');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/jobslist/jobslist/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMyservers(){
	loading();
	activateMenu('menu-myservers');
	showBreadcrumbs([], 'Servers');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/myservers/myservers/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMyserversBrowseservers(){
	loading();
	activateMenu('menu-myservers');
}

function runMyarea(){
	loading();
	activateMenu('menu-myarea');
	LoadMyArea();
}

function runMysettings(){
	loading();
	activateMenu('menu-mysettings');
	showBreadcrumbs([], 'Settings');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/mysettings/mysettings/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runAdminstats(){
	loading();
	activateMenu('menu-adminstats');
	showBreadcrumbs([], 'Statistics');
	clearInterval(refreshEvent);
	$('#top-pane').load("/plugins/adminstats/adminstats/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runAdminarea(){
	loading();
	activateMenu('menu-adminarea');
window.open('/plugins/adminarea/adminarea/');}



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

	if(view=='applist') runApplist.apply(null, params);
	if(view=='applist-loadjob') runApplistLoadjob.apply(null, params);
	if(view=='applist-load') runApplistLoad.apply(null, params);
	if(view=='jobslist-check_job_output') runJobslistCheck_job_output.apply(null, params);
	if(view=='jobslist-kill_job') runJobslistKill_job.apply(null, params);
	if(view=='jobslist-check_job_parameters') runJobslistCheck_job_parameters.apply(null, params);
	if(view=='jobslist-check_output_files') runJobslistCheck_output_files.apply(null, params);
	if(view=='jobslist-browsejobs') runJobslistBrowsejobs.apply(null, params);
	if(view=='jobslist-reset_job') runJobslistReset_job.apply(null, params);
	if(view=='jobslist') runJobslist.apply(null, params);
	if(view=='jobslist-run_job') runJobslistRun_job.apply(null, params);
	if(view=='myservers') runMyservers.apply(null, params);
	if(view=='myservers-installcluster') runMyserversInstallcluster.apply(null, params);
	if(view=='myservers-synchronize_server') runMyserversSynchronize_server.apply(null, params);
	if(view=='myservers-browseservers') runMyserversBrowseservers.apply(null, params);
	if(view=='myarea') runMyarea.apply(null, params);
	if(view=='mysettings') runMysettings.apply(null, params);
	if(view=='adminstats') runAdminstats.apply(null, params);
	if(view=='adminarea') runAdminarea.apply(null, params);
	
}