from pyramid.view import view_config


@view_config(route_name='/pippo', renderer='../templates/mytemplate.jinja2', permission='play')
def my_view(request):
    return {'project': 'DandD'}

