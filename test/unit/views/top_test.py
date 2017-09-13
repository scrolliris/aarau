# pylint: disable=unused-argument
"""Unit tests for top page.
"""
import pytest


@pytest.fixture(autouse=True)
def setup(config):
    """Setup.
    """
    pass


def test_view_top(users, dummy_request):
    """Test top view.
    """
    from aarau.views.top import top

    dummy_request.user = users['oswald']
    res = top(dummy_request)
    assert {} == res
