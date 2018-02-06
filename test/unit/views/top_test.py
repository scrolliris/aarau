from collections.abc import Mapping

import pytest

from webob.multidict import NestedMultiDict


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_view_top(users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.top import top

    user = users['oswald']
    dummy_request.user = user
    dummy_request.POST = NestedMultiDict()

    res = top(dummy_request)
    form = build_new_project_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)


def test_view_top_type_publication(users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.top import top

    user = users['oswald']
    dummy_request.user = user
    dummy_request.POST = NestedMultiDict()

    res = top(dummy_request)
    form = build_new_project_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)


def test_view_top_type_application(users, dummy_request):
    from aarau.views.console.project.form import build_new_project_form
    from aarau.views.top import top

    user = users['oswald']
    dummy_request.user = user
    dummy_request.POST = NestedMultiDict()

    res = top(dummy_request)
    form = build_new_project_form(dummy_request)

    assert isinstance(res, Mapping)
    assert ('form',) == tuple(sorted(res.keys()))
    assert isinstance(res['form'], form.__class__)
