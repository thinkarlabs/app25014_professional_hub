_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './fe/app/25014/mod01/web/contact/contact_dtl.htm';

	_cp.api.item = '/be/app/25014/api/app25014_professional_hub/be/mod01/contact/';
	
	
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
// SAVE
_cp.load = function(){
    _app.bind_event('#btnCancel','click',_cp.on.Cancel);
    _app.bind_event('#btnSave','click',_cp.on.Save);    
        
}
//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('store.contact_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#form_contact'), _cp.api.item + _cp.params, function(resp){
	_app.nav_page('store.contact_lst');
	});
	return false;
}

_cp.init();
