const _app = new RubixCore();
_app.init();
_app.debug = true;
_app.curr_ses = JSON.parse(sessionStorage.getItem('session_info'));

// if (_app.curr_ses.user.role_id === 'hub_admin') _app.load_page('store.activity_lst');
// if (_app.curr_ses.user.role_id === 'org_admin') _app.load_page('mob.request_lst');
_app.load_page('mob.request_lst');

 history.replaceState({}, null, "/neev/mob/");
