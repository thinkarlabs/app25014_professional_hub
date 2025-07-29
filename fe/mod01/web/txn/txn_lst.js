_cp = _app.curr_page

_cp.init = function(){
	// _app.msg('reverse')
	//Define the page URL and the base API
	_cp.views.page = './fe/app/25014/mod01/web/txn/txn_lst.htm';
	_cp.api.list = '/be/app/25014/api/app25014_professional_hub/be/mod01/txn/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');
		var _filter = '?staff=' +_app.curr_ses.user.id;
	
			
	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/category/'+_filter, function(data){
		_cp.data.categories = data.categories
		category.init(_cp.data.categories,'All Categories-D','_id','name','')
        _cp.on.filter_list();		
	});		

	//Bind events for add and search. 
	//NOTE : Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
	_app.bind_event('#st_date','change',_cp.on.filter_list);
	_app.bind_event('#en_date','change',_cp.on.filter_list);
	_app.bind_event('#category','changed',_cp.on.filter_list);

}

//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.filter_list = function(){
	
	var startDate = $('#st_date').val();
    var endDate = $('#en_date').val();
	_app.log(startDate)
	_app.log(endDate)
	_filter ='?category=' + $('#sel_category').val()
    _filter+= '&st=' + $('#st_date').val() + '&en=' + $('#en_date').val()
	_filter += '&staff=' +_app.curr_ses.user.id;

	
	_app.log(_filter);
	_app.get(_cp.api.list + _filter, function(data) {
        _app.log(data);
	    _cp.render_view(_cp.views.tableView,data, 'x-txns');
		_cp.table = _cp.display_table('#tbl_txns');	
	});		
}

_cp.on.Add = function(){
	_app.nav_page('store.txn_dtl')
	return false;
}

_cp.on.Edit = function(id){
	_app.nav_page('store.txn_dtl',id)
	return false;
}

﻿_cp.on.Reverse = function(id){
	_app.post(_cp.api.list+'reverse/' + id,'', function(data){
		_cp.init();
	});
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

//////////////////////////////////// Define all the views for the page here  ////////////////////

_cp.views.tableView = `
	<table class="table table-sm table-striped" id="tbl_txns">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>Transaction Title</th>
		  <th>Transaction Type</th>
		  <th>From Account</th>
		  <th>To Account</th>
		  <th>Category</th>
		  <th>Amount</th>
		  <th>Date</th>
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in txns %}
		<tr>
		  <td class="col">{{item.txn_title}}</td>
		  <td class="col">{{item.txntype_name}}</td>
		  <td class="col">{{item.from_acc_name}}</td>
		  <td class="col">{{item.to_acc_name}}</td>
		  <td class="col">{{item.category_name}}</td>
		  <td class="col">{{item.amt}}</td>
		  <td class="col">{{item.txn_date}}</td>	
		{% if item.txntype_name== 'Reversed'%}
		    <td class="text-center">
				<button type="button" class="btn btn-danger btn-sm float-end mx-2" 
					onclick='_cp.on.Edit("{{item._id}}");'>View</button>
		    </td>
		{% else %}
		    <td class="text-center">
				<button type="button" class="btn btn-primary btn-sm float-end mx-2" 
					onclick='_cp.on.Reverse("{{item._id}}");'>Reverse</button>			
		    </td>
		{% endif %}
		</tr>
	  {% endfor %}
	  </tbody>
	</table>	
`

//////////////////////////////////// Call Current Page Init  ////////////////////

_cp.init();
