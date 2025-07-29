_cp = _app.curr_page
_app.log("Helloooo")
_cp.init = function(){
	//Define the page URL and the base API

	_cp.views.page = './fe/app/25014/mod01/web/dashboard/dashboard_lst.htm';
	_cp.api.list = '/be/app/25014/api/app25014_personal_hub/be/mod01/task/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');	
	
	
	// Call the filter to get the data.
	_cp.on.filter_list();	

	//Bind events for add and search. 
	//NOTE : Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#searchprojects','keyup',_cp.on.Search);
	_app.bind_event('#en_date','change',_cp.on.filter_list);
	_app.bind_event('#sel_status','changed',_cp.on.filter_list);
	
}







_cp.on.filter_list = function() {
    _filter = '';
    
    var today = new Date();
	today.setDate(today.getDate() - 1);
    
    var formattedDate = today.toISOString().split('T')[0];
    
    _filter = "?en=" + formattedDate + "&st=2024-01-01";
    _filter += '&notstatus=CP';
	_filter += '&staff=' +_app.curr_ses.user.id;

    
    _app.log(_filter);
    _app.get(_cp.api.list + _filter, function(data) {
        _app.log(data);
        _cp.render_view(_cp.views.tableView, data, 'x-tasks');
        _cp.table = _cp.display_table('#tbl_tasks');
    });
}



_cp.on.Change = function(id){
	p={"id":id,"pg":"dashboard"}
	_app.nav_page('store.task_dtl',p)
	return false;
}





//////////////////////////////////// Define all the views for the page here  ////////////////////

_cp.views.tableView = `
	<table class="table table-sm table-striped" id="tbl_tasks">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>Project Title</th>
		  <th>Task Title</th>
		  <th>Task Satus</th>
		   <th>Reminder Date</th>
		   <th>Owner</th>




		  
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  
	
	  {% for item in tasks %}
	  
		<tr>
		  
		  <td class="col">{{item.project_name}}</td>
		  <td class="col">{{item.title}}</td>
		  <td class="col">{{item.status_name}}</td>
		  <td class="col">{{item.reminder_date}}</td>
		  <td class="col">{{item.owner_name}}</td>



		  
		  <td class="text-center">
			
			<button type="button" class="btn btn-primary btn-sm float-end mx-2" 
				onclick='_cp.on.Change("{{item._id}}");'><i class="bi bi-pencil-square"></i> Change</button>
		</td>
		</tr>
	  {% endfor %}
	  </tbody>
	</table>	
`

//////////////////////////////////// Call Current Page Init  ////////////////////

_cp.init();
