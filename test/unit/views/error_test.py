import pytest


@pytest.fixture(autouse=True)
def setup(config):
    pass


def test_notfound_error(users, dummy_request):
    from aarau.views.error import notfound

    dummy_request.user = users['oswald']
    res = notfound(dummy_request)

    assert '404 Not Found' == dummy_request.response.status
    assert {} == res
