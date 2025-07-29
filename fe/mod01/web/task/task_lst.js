_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './fe/app/25014/mod01/web/task/task_lst.htm';
	_cp.api.list = '/be/app/25014/api/app25014_professional_hub/be/mod01/task/';
	

	//Render the page.
	_cp.render_page(_cp.views.page,'');	
	
	
	//Fill the filter combo boxes.
	var _filter = '?staff=' +_app.curr_ses.user.id;
	_app.get('/be/app/25014/api/app25014_professional_hub/be/mod01/project/'+_filter, function(data){
		_cp.data.projects = data.projects
		project.init(_cp.data.projects,'All Projects','_id','project_title',"")
		_cp.on.filter_list();

	}); 


	// Call the filter to get the data.
	_cp.on.filter_list();	

	// Bind events for add and search. 
	// NOTE: Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#searchprojects','keyup',_cp.on.Search);
	_app.bind_event('#project, #status, #st_date, #en_date', 'change', _cp.on.filter_list);

}

//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.filter_list = function(){

	
	_filter = '?project=' + $('#sel_project').val()
	_filter += '&status=' + $('#sel_status').val()
	_filter += '&st=' + $('#st_date').val() 
	_filter += '&en=' + $('#en_date').val()
	_filter += '&staff=' +_app.curr_ses.user.id;
	

	_app.log(_filter);
 
	_app.get(_cp.api.list + _filter, function( data ) {	
		_app.log(data); 
		if ($('#sel_view').val() === 'C'){
			_cp.render_view(_cp.views.cardView,data, 'x-tasks');
		}
		else{
			_cp.render_view(_cp.views.tableView,data, 'x-tasks');
			_cp.table = _cp.display_table('#tbl_tasks');						
		}
	});	
}

_cp.on.Add = function(){
	_app.nav_page('store.task_dtl')
	return false;
}

_cp.on.Edit = function(id){
	p={"id":id,"pg":"task_lst"}

	_app.nav_page('store.task_dtl',p)
	return false;
}

_cp.on.Delete = function(id){
		_app.nav_page('store.task_lst')

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
	<table class="table table-sm table-striped" id="tbl_tasks">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  
		  <th>TaskTitle</th>
		  <th>ProjectTitle</th>
		  <th>TaskStatus</th>
		  <th>ReminderDate</th>
		   <th>Owner Name</th>




		  
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in tasks %}
	  
		<tr>
		  
		  <td class="col">{{item.title}}</td>
		  <td class="col">{{item.project_name}}</td>
		  <td class="col">{{item.status_name}}</td>
		  <td class="col">{{item.reminder_date}}</td>
		  <td class="col">{{item.owner_name}}</td>


		  
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

//////////////////////////////////// Call Current Page Init  ////////////////////

_cp.init();
