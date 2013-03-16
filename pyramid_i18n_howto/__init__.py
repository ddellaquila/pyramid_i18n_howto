from pyramid.config import Configurator

from i18n import custom_locale_negotiator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('locale', '/locale')
    config.scan()
    config.add_translation_dirs('pyramid_i18n_howto:locale')
    config.add_subscriber('pyramid_i18n_howto.i18n.add_renderer_globals',
                          'pyramid.events.BeforeRender')
    config.add_subscriber('pyramid_i18n_howto.i18n.add_localizer',
                          'pyramid.events.NewRequest')
    config.set_locale_negotiator(custom_locale_negotiator)
    return config.make_wsgi_app()
