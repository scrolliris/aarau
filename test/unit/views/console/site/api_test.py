import json

import pytest


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


# GET api_application_insights_data

@pytest.mark.parametrize('params', [
    {},
    {'project_id': '0'}
], ids=['missing', 'invalid'])
def test_application_insights_data_with_invalid_project_id(
        users, params, dummy_request):
    from aarau.views.console.site.api import api_application_insights_data

    user = users['oswald']
    dummy_request.user = user
    dummy_request.matchdict = params

    res = api_application_insights_data(dummy_request)
    assert 404 == res.status_code
    json_body = json.loads(res.body.decode())
    assert ['error'] == list(json_body.keys())
    expected = 'The project or site was not found'
    assert expected == json_body['error']


@pytest.mark.parametrize('params', [
    {},
    {'id': '0'}  # site.id
], ids=['missing', 'invalid'])
def test_application_insights_data_with_invalid_site_id(
        users, params, dummy_request):
    from aarau.views.console.site.api import api_application_insights_data

    user = users['oswald']
    params['project_id'] = user.projects[0].id
    dummy_request.user = user
    dummy_request.matchdict = params

    res = api_application_insights_data(dummy_request)
    assert 404 == res.status_code
    expected = 'The project or site was not found'
    assert expected == json.loads(res.body.decode())['error']


# GET api_application_insights_metrics

@pytest.mark.parametrize('params', [
    {},
    {'project_id': '0'}
], ids=['missing', 'invalid'])
def test_application_insights_metrics_with_invalid_project_id(
        users, params, dummy_request):
    from aarau.views.console.site.api import api_application_insights_metrics

    user = users['oswald']
    dummy_request.user = user
    dummy_request.matchdict = params

    res = api_application_insights_metrics(dummy_request)
    assert 404 == res.status_code
    json_body = json.loads(res.body.decode())
    assert ['error'] == list(json_body.keys())
    expected = 'The project or site was not found'
    assert expected == json_body['error']


@pytest.mark.parametrize('params', [
    {},
    {'id': '0'}  # site.id
], ids=['missing', 'invalid'])
def test_application_insights_metrics_with_invalid_site_id(
        users, params, dummy_request):
    from aarau.views.console.site.api import api_application_insights_metrics

    user = users['oswald']
    params['project_id'] = user.projects[0].id
    dummy_request.user = user
    dummy_request.matchdict = params

    res = api_application_insights_metrics(dummy_request)
    assert 404 == res.status_code
    expected = 'The project or site was not found'
    assert expected == json.loads(res.body.decode())['error']
