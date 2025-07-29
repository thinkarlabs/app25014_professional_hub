_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './fe/app/24005/mod01/web/assettype/assettype_lst.htm';
	_cp.api.list = '/be/app/24005/api/app24005_personal_hub/be/mod01/assettype/';

	_cp.render_page(_cp.views.page,'');	

	_cp.on.filter_list();	

	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#searchAssettypes','keyup',_cp.on.Search);
}


_cp.on.filter_list = function() {
    _filter = '?staff=' +_app.curr_ses.user.id;
	_app.log("_filter")
	_app.log(_filter)
    _app.get(_cp.api.list + _filter, function(data) {
        console.log("Data fetched for asserttype list: ", data);
        _cp.render_view(_cp.views.tableView,data, 'x-assettypes');
		 _cp.table = _cp.display_table('#tbl_assettypes');
    });
};



//ADD
_cp.on.Add = function(){
	_app.nav_page('store.assettype_dtl')
	return false;
}
//search
// SEARCH
_cp.on.Search = function(){
	_cp.table.search(this.value).draw();
	return false;
}

//EDIT
_cp.on.Edit = function(id){
	_app.nav_page('store.assettype_dtl',id)	
	return false;
}

// DELETE
_cp.on.Delete = function(id){
_app.del(_cp.api.list + id, function(data){
	_cp.init();
	});
	return false;
}

_cp.views.tableView = `
		<table class="table table-sm table-striped" id="tbl_assettypes">
		  <!-- <thead class="table-dark"> -->
		  <thead>
			<tr>
			  <th>Title</th>
			  <th class="text-center">Actions</th>
			</tr>
		  </thead>
		  <tbody>
		  {% for item in assettypes %}
			<tr>
			  <td class="col">{{item.title}}</td>
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

