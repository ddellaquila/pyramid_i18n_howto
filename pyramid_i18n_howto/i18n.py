from pyramid.i18n import get_localizer, TranslationStringFactory

from pyramid.events import NewRequest
from pyramid.events import subscriber
from webob.acceptparse import Accept


tsf = TranslationStringFactory('pyramid_i18n_howto')

LOCALES = ('en', 'es', 'it')


def custom_locale_negotiator(request):
    """ The :term:`custom locale negotiator`. Returns a locale name.

    - First, the negotiator looks for the ``_LOCALE_`` attribute of
      the request object (possibly set by a view or a listener for an
      :term:`event`).

    - Then it looks for the ``request.params['_LOCALE_']`` value.

    - Then it looks for the ``request.cookies['_LOCALE_']`` value.

    - Then it looks for the ``Accept-Language`` header value,
      which is set by the user in his/her browser configuration.

    - Finally, if the locale could not be determined via any of
      the previous checks, the negotiator returns the
      :term:`default locale name`.
    """

    name = '_LOCALE_'
    locale_name = getattr(request, name, None)
    if locale_name is None:
        locale_name = request.params.get(name)
        if locale_name is None:
            locale_name = request.cookies.get(name)
            if locale_name is None:
                locale_name = request.accept_language.best_match(
                    LOCALES, request.registry.settings.default_locale_name)
                if not request.accept_language:
                    # If browser has no language configuration
                    # the default locale name is returned.
                    locale_name = request.registry.settings.default_locale_name

    return locale_name


def add_renderer_globals(event):
    request = event.get('request')
    if request is None:
        request = get_current_request()
    event['_'] = request.translate
    event['localizer'] = request.localizer


def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    def auto_translate(string):
        return localizer.translate(tsf(string))
    request.localizer = localizer
    request.translate = auto_translate
