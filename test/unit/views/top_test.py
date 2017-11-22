import pytest

from webob.multidict import NestedMultiDict, NoVars


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_get_site_type():
    from aarau.views.top import get_site_type

    assert 'publication' == get_site_type(NoVars())
    assert 'publication' == get_site_type({})
    assert 'publication' == get_site_type(NestedMultiDict({}))
    assert 'publication' == get_site_type({'type': 'publication'})
    assert 'application' == get_site_type({'type': 'application'})


def test_view_top(users, dummy_request):
    from aarau.models import Site
    from aarau.views.top import top

    user = users['oswald']
    dummy_request.user = user
    res = top(dummy_request)

    assert isinstance(res, dict)
    assert ('site_type', 'sites') == tuple(sorted(res.keys()))
    assert 'publication' == res['site_type']
    assert {Site} == set([s.__class__ for s in res['sites']])
    assert False not in set([hasattr(s, 'publication') for s in res['sites']])


def test_view_top_type_publication(users, dummy_request):
    from aarau.models import Site
    from aarau.views.top import top

    user = users['oswald']
    query_param = {'type': 'publication'}
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.params = query_param

    res = top(dummy_request)

    assert isinstance(res, dict)
    assert ('site_type', 'sites') == tuple(sorted(res.keys()))
    assert 'publication' == res['site_type']
    assert {Site} == set([s.__class__ for s in res['sites']])
    assert False not in set([hasattr(s, 'publication') for s in res['sites']])


def test_view_top_type_application(users, dummy_request):
    from aarau.models import Site
    from aarau.views.top import top

    user = users['oswald']
    query_param = {'type': 'application'}
    dummy_request.user = user
    dummy_request.GET = NestedMultiDict(query_param)
    dummy_request.params = query_param

    res = top(dummy_request)

    assert isinstance(res, dict)
    assert ('site_type', 'sites') == tuple(sorted(res.keys()))
    assert 'application' == res['site_type']
    assert {Site} == set([s.__class__ for s in res['sites']])
    assert False not in set([hasattr(s, 'application') for s in res['sites']])
