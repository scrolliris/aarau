from pyramid.events import subscriber
from pyramid.events import BeforeRender, NewRequest
from pyramid.i18n import TranslationString


def get_translator_function(localizer):
    def translate(*args, **kwargs):
        if 'domain' not in kwargs:
            kwargs['domain'] = 'message'
        ts = TranslationString(*args, **kwargs)
        return localizer.translate(ts)
    return translate


@subscriber(NewRequest)
def add_localizer(event):
    request = event.request

    if request:
        localizer = request.localizer
        request.translate = get_translator_function(localizer)


@subscriber(BeforeRender)
def add_localizer_renderer_globals(event):
    request = event['request']

    if request and hasattr(request, 'translate'):
        _ = request.translate
        if _:
            event['_'] = _  # shortcut method for template
