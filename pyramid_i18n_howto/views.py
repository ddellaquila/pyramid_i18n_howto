from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    _ = request.translate
    return {'project': _('My i18n project')}
