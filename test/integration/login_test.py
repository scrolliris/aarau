import pytest

from ..server import BASE_URL


@pytest.fixture(autouse=True)
def setup(server_run, request, config):  # pylint: disable=unused-argument
    def teardown():
        pass

    request.addfinalizer(teardown)


def test_login_failure(selenium):
    login_url = '{}/login'.format(BASE_URL)
    selenium.get(login_url)

    form = selenium.find_element_by_xpath('//form[@id="login"]')
    assert 'form' == form.get_attribute('class')

    email = form.find_element_by_xpath('//input[@id="email"]')
    email.send_keys("unknown@example.org")

    password = form.find_element_by_xpath('//input[@id="password"]')
    password.send_keys("Wr0ngPassw0rd")

    form.find_element_by_name('submit').click()

    assert login_url == selenium.current_url
    assert 'Log in - Scrolliris' == selenium.title

    assert 'The credential you\'ve entered is incorrect' \
        in selenium.page_source


def test_login_success(selenium):
    selenium.get('{}/login'.format(BASE_URL))

    form = selenium.find_element_by_xpath('//form[@id="login"]')
    assert 'form' == form.get_attribute('class')

    email = form.find_element_by_xpath('//input[@id="email"]')
    email.send_keys("oswald@example.org")

    password = form.find_element_by_xpath('//input[@id="password"]')
    password.send_keys("0PlayingPiano")

    form.find_element_by_name('submit').click()

    next_url = BASE_URL + '/'
    assert next_url == selenium.current_url
    assert 'Scrolliris' == selenium.title
