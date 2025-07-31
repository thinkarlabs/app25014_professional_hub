_cp = _app.curr_page
_app.msg("hyyyyy5")
_cp.init = function(){
	_cp.views.page = './fe/app/25014/mod01/web/resource/resource_dtl.htm';
	_cp.api.item = '/be/app/25014/api/app25014_professional_hub/be/mod01/resource/';
	
	
	//If params then it is in EDIT mode. Else Add mode.
	if (_cp.params !== ''){
		_app.get(_cp.api.item + _cp.params, function(item_data){
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
	var _filter = '?org=' +_app.curr_ses.user.org_id;
	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/resourcetype/'+_filter, function(data){
		_cp.data.resourcetypes = data.resourcetypes
		type.init(_cp.data.resourcetypes,'--Select an resource type--','_id','title',':auto')
	});
	var _filter = '?org=' +_app.curr_ses.user.org_id;
	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/contact/'+_filter, function(data){
		_cp.data.contacts =data.contacts
		contact.init(_cp.data.contacts,'--Select an owner--','_id','contact_name',':auto')
	});
	
    _app.bind_event('#btnCancel','click',_cp.on.Cancel);
    _app.bind_event('#btnSave','click',_cp.on.Save);    
   
}

//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('store.resource_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#form_resource'), _cp.api.item + _cp.params, function(resp){
	_app.nav_page('store.resource_lst');
	});
	return false;
}

_cp.init();
