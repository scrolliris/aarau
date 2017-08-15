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
    req = event.request

    if req:
        req.translate = get_translator_function(req.localizer)


@subscriber(BeforeRender)
def add_localizer_renderer_globals(event):
    req = event['request']

    if req and hasattr(req, 'localizer'):
        __ = req.localizer.translate
        if __:
            event['__'] = __  # util method for translation string

    if req and hasattr(req, 'translate'):
        _ = req.translate
        if _:
            event['_'] = _  # shortcut method for template
