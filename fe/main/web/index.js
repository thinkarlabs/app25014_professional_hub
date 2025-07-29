const _app = new RubixCore();
_app.msg("app14..")
_app.init();
_app.debug = true;
_app.curr_ses = JSON.parse(sessionStorage.getItem('session_info'));

// if (_app.curr_ses.user.role_id === 'program_admin') _app.load_page("store.dashboard_lst");
// history.replaceState({}, null, "/app11/");
_app.load_page('store.dashboard_lst');


history.replaceState({}, null, "/neev/web/");
