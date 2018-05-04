from pyramid.view import view_config


@view_config(route_name='dashboard', renderer='../templates/header.jinja2', permission='play')
def my_view(request):
    return {'project': 'DandD'}

