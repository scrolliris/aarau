import pytest


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_view_top(users, dummy_request):
    from aarau.views.top import top

    dummy_request.user = users['oswald']
    res = top(dummy_request)
    assert {} == res
