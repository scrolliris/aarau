import pytest

from aarau.utils.template import TemplateUtil


@pytest.fixture(autouse=True)
def setup(config, monkeypatch):  # pylint: disable=unused-argument
    import time
    from pyramid.static import QueryStringConstantCacheBuster

    def dummy_time():
        return 1508764197.683521

    monkeypatch.setattr('time.time', dummy_time)

    # replace actual cache buster in route.py
    config.add_cache_buster('aarau:../static/', QueryStringConstantCacheBuster(
        str(int(time.time()))))


def test_static_url_in_development(dummy_request):
    template_util = TemplateUtil({}, dummy_request)

    expected = 'http://example.org/assets/img/touch-icon-120.png?x=1508764197'
    assert expected == template_util.static_url('img/touch-icon-120.png')


def test_static_url_in_production(monkeypatch, dummy_request):
    class DummyEnv(object):
        @property
        def is_production(self):
            return True

    template_util = TemplateUtil({}, dummy_request)
    monkeypatch.setattr(template_util, 'env', DummyEnv())

    expected = 'https://cdn.example.com/org.example/v1/static/' \
        'img/touch-icon-120.png'
    assert expected == template_util.static_url('img/touch-icon-120.png')
