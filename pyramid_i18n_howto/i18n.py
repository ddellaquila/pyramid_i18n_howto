from pyramid.i18n import get_localizer, TranslationStringFactory

from pyramid.events import NewRequest
from pyramid.events import subscriber
from webob.acceptparse import Accept


@subscriber(NewRequest)
def setAcceptedLanguagesLocale(event):
    if not event.request.accept_language:
        return
    accepted = event.request.accept_language
    event.request._LOCALE_ = accepted.best_match(('en', 'es', 'it'), 'it')


def add_renderer_globals(event):
    request = event.get('request')
    if request is None:
        request = get_current_request()
    event['_'] = request.translate
    event['localizer'] = request.localizer


tsf = TranslationStringFactory('pyramid_i18n_howto')


def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    def auto_translate(string):
        return localizer.translate(tsf(string))
    request.localizer = localizer
    request.translate = auto_translate
