import pytest

from aarau.models import Classification


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


# GET api_classification_tree

def test_classification_tree_without_data(users, dummy_request):
    from aarau.views.console.classification.api import api_classification_tree

    user = users['oswald']
    dummy_request.user = user
    dummy_request.matchdict = {}

    res = api_classification_tree(dummy_request)
    assert {'data': []} == res


def test_classification_tree(users, dummy_request):
    from aarau.views.console.classification.api import api_classification_tree

    Classification.rebuild_all()

    user = users['oswald']
    dummy_request.user = user
    dummy_request.matchdict = {}

    res = api_classification_tree(dummy_request)
    assert {
        'children': [{
            'children': [{
                'children': [],
                'label': 'Science and knowledge in general. Organization of '
                         'intellectual work',
                'value': '001'
            }],
            'label': 'Prolegomena. Fundamentals of knowledge and culture. '
                     'Propaedeutics',
            'value': '00'
        }, {
            'children': [],
            'label': 'Bibliography and bibliographies. Catalogues',
            'value': '01'
        }],
        'label': 'Science and Knowledge. '
                 'Organization. Computer Science. Information. '
                 'Documentation. Librarianship. Institutions. Publications',
        'value': '0',
    } == res['data'][0]
