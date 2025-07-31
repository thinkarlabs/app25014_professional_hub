_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './fe/app/25014/mod01/web/txn/txn_dtl.htm';
	_cp.api.item = '/be/app/25014/api/app25014_professional_hub/be/mod01/txn/';
	
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

	
	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/accoutn/'+_filter, function(acc_data){
		_cp.data.accounts = acc_data.accounts
		from_acc.init(_cp.data.accounts,'Select an Account','_id','acc_title',':auto')
		
	});
		var _filter = '?org=' +_app.curr_ses.user.org_id;

	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/accoutn/'+_filter, function(acc_data){
		_cp.data.accounts = acc_data.accounts
		to_acc.init(_cp.data.accounts,'Select an Account','_id','acc_title',':auto')
	});
		var _filter = '?org=' +_app.curr_ses.user.org_id;

	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/category/'+_filter, function(cat_data){
		_cp.data.categories = cat_data.categories
		category.init(_cp.data.categories,'Select an Category','_id','name',':auto')
		
	});
	
	
	
	if (_cp.params !== ''){
		$('#txttxntitle').prop('disabled', true);
		$('#sel_txntype').prop('disabled', true);
		$('#sel_from_acc').prop('disabled', true);
		$('#sel_to_acc').prop('disabled', true);
		$('#txtdate').prop('disabled', true);
		$('#txtamt').prop('disabled', true);
		$('#sel_category').prop('disabled', true);
    }	
	_app.bind_event('#btnCancel','click',_cp.on.Cancel);
	_app.bind_event('#btnSave','click',_cp.on.Save);
	$('#sel_txntype').on('change',_cp.on.txnType);  

}

_cp.on.Cancel = function(){
	_app.nav_page('store.txn_lst');
	return false;
}


_cp.on.Save = function(){
	_app.post_form($('#txn_form'), _cp.api.item + _cp.params, function(resp){
		_app.nav_page('store.txn_lst');
	});
	return false;
}



_cp.on.txnType = function(){
	  var value = $('#sel_txntype').val();
	  if (value === 'D'){
		$('#sel_to_acc').prop('disabled', true);
		$('#sel_from_acc').prop('disabled', false);

	  }if (value === 'C'){
		$('#sel_from_acc').prop('disabled', true);
		$('#sel_to_acc').prop('disabled', false);

	  }if (value === 'T'){
		$('#sel_to_acc').prop('disabled', false);
		$('#sel_from_acc').prop('disabled', false);		
	  }
	  return false;
}


_cp.init();
