_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './fe/app/25014/mod01/web/account/account_lst.htm';
	_cp.api.list = '/be/app/25014/api/app25014_professional_hub/be/mod01/accoutn/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');	

	
	//Call the filter to get the data.
	_cp.on.filter_list();	

	//Bind events for add and search. 
	//NOTE : Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
}

_cp.on.filter_list = function(){
    _filter = ''
	_filter = '?staff=' +_app.curr_ses.user.id;

    _app.get(_cp.api.list + _filter, function( data ) {	
		_app.log(data);
		_cp.render_view(_cp.views._table,data, 'x-accounts');
		_cp.table = _cp.display_table('#tbl_accounts');
	});
	
	
};

_cp.on.Add = function(){
	_app.nav_page('store.account_dtl')
	return false;
}

_cp.on.Edit = function(id){
	_app.nav_page('store.account_dtl',id)
	return false;
}

_cp.on.Delete = function(id){
	_app.del(_cp.api.list + id, function(data){
		_cp.init();
	});

	return false;
}
_cp.on.Search = function(){
	_cp.table.search(this.value).draw();
	return false;
}



_cp.views._table = `
		<table class="table table-sm table-striped" id="tbl_accounts">
		  <!-- <thead class="table-dark"> -->
		  <thead>
			<tr>
			  <th>Account Title</th>
			  <th>Account Type</th>
			  <th>Balance</th>
			  <th class="text-center">Actions</th>
			</tr>
		  </thead>
		  <tbody>
		  
		  {% for item in accounts %}
			<tr>
			  <td class="col">{{item.acc_title}}</td>
			  <td class="col">{{item.acc_type_name}}</td>
			  <td class="col">{{item.balance}}</td>
			  <td class="text-center">
				<button type="button" class="btn btn-danger btn-sm float-end mx-2" 
					onclick='_cp.on.Delete("{{item._id}}");'><i class="bi bi-trash"></i> Delete</button>
				<button type="button" class="btn btn-primary btn-sm float-end mx-2" 
					onclick='_cp.on.Edit("{{item._id}}");'><i class="bi bi-pencil-square"></i> Edit</button>
			  </td>
			</tr>
		  {% endfor %}
		  </tbody>
		</table>
`


_cp.init();
