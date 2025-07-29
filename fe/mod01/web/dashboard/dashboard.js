_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './fe/app/25014/mod01/web/dashboard/dashboard.htm';
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
	_app.nav_page('money.account_dtl')
	return false;
}

_cp.on.Edit = function(id){
    _app.nav_page('money.account_dtl')
	return false;
}

_cp.on.Delete = function(id){
	_app.nav_page('money.account_lst')

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

			</tr>
		  </thead>
		  <tbody>
		  {% for item in accounts %}
			<tr>
			  <td class="col">{{item.acc_title}}</td>
			  <td class="col">{{item.acc_type_name}}</td>
			  <td class="col">{{item.balance}}</td>

			  
			</tr>
		  {% endfor %}
		  </tbody>
		</table>
`


_cp.init();