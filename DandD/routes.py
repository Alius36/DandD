def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('home', '/')


    # AUTHENTICATION
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('login_view', '/login_view')
    config.add_route('registration', '/registration')
    config.add_route('registration_view', '/registration_view')
    config.add_route('logout', '/logout')
