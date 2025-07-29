_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './fe/app/25014/mod01/web/asset/asset_dtl.htm';
	_cp.api.item = '/be/app/25014/api/app25014_professional_hub/be/mod01/asset/';
	
	
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
	var _filter = '?staff=' +_app.curr_ses.user.id;
	_app.get('/be/app/25014/api/app24005_personal_hub/be/mod01/assettype/'+_filter, function(data){
		_cp.data.assettypes = data.assettypes
		type.init(_cp.data.assettypes,'--Select an asset type--','_id','title',':auto')
	});
	var _filter = '?staff=' +_app.curr_ses.user.id;
	_app.get('/be/app/25014/api/app24005_personal_hub/be/mod01/contact/'+_filter, function(data){
		_cp.data.contacts =data.contacts
		contact.init(_cp.data.contacts,'--Select an owner--','_id','contact_name',':auto')
	});
	
    _app.bind_event('#btnCancel','click',_cp.on.Cancel);
    _app.bind_event('#btnSave','click',_cp.on.Save);    
   
}

//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('store.asset_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#form_asset'), _cp.api.item + _cp.params, function(resp){
	_app.nav_page('store.asset_lst');
	});
	return false;
}

_cp.init();
