_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './fe/app/25014/mod01/web/task/task_dtl.htm';
	_cp.api.item = '/be/app/25014/api/app25014_professional_hub/be/mod01/task/';
	
	// If params then it is in EDIT mode. Else Add mode.
	if (_cp.params["id"]!== undefined){
		_app.get(_cp.api.item + _cp.params["id"], function(item_data){
			_cp.render_page(_cp.views.page,item_data);
			_cp.load();					
		});
	}
	else{
		_cp.render_page(_cp.views.page,'');		
		_cp.load();		
	}	
}

_cp.load = function(){
	var _filter = '?staff=' +_app.curr_ses.user.id;

	_app.get('/be/app/25014/api/app24005_professional_hub/be/mod01/project/'+_filter, function(project_data){
		_cp.data.projects = project_data.projects
		project.init(_cp.data.projects,'--Select an project--','_id','project_title',':auto')
		
		var _filter = '?staff=' +_app.curr_ses.user.id;

	
	_app.get('/be/app/25014/api/app24005_professional_hub/be/mod01/contact/'+_filter, function(data){
		_cp.data.contacts =data.contacts
		owner.init(_cp.data.contacts,'--Select an owner--','_id','contact_name',':auto')
	
	});
	
	

	 });
	
	_app.bind_event('#btnCancel','click',_cp.on.Cancel);
	_app.bind_event('#btnSave','click',_cp.on.Save);
	
}
//////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
		 
    if (_cp.params["pg"]==="dashboard") {
        _app.nav_page('store.dashboard_lst');
    } else {
        _app.nav_page('store.task_lst');
    }
	return false;
}





_cp.on.Save = function() {
    var id = _cp.params["id"]; 
    var form = $('#form_book');
    _app.post_form(form, _cp.api.item + (id ? id : ''), function(resp) {
        if (_cp.params["pg"] === "dashboard") {
            _app.nav_page('store.dashboard_lst');
        } else {
            _app.nav_page('store.task_lst');
        }
    });
    
    return false;
}


_cp.init()




