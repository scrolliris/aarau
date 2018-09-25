import pytest

from aarau.models import (
    Article,
    Project,
    Site
)


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        worker.conf.update(task_always_eager=False)

    request.addfinalizer(teardown)


# console

@pytest.mark.usefixtures('login')
def test_title_console_top(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/', status=200)
        assert 'Console - Scrolliris' == res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_project_new(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/projects/new', status=200)
        assert 'Create a New Project - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_project_settings(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        res = app.get('/{:s}/settings'.format(project.namespace), status=200)
        assert 'Settings - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_project_overview(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        res = app.get('/{:s}'.format(project.namespace), status=200)
        assert 'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_new(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        res = app.get('/{:s}/new'.format(project.namespace), status=200)
        assert 'Create a New Publication - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()

        res = app.get('/{:s}/new?type=publication'.format(project.namespace),
                      status=200)
        assert 'Create a New Publication - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()

        res = app.get('/{:s}/new?type=application'.format(project.namespace),
                      status=200)
        assert 'Create a New Application - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_insights(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # publication
        site = project.sites.where(Site.slug == 'playing-piano').get()
        res = app.get(
            '/{:s}/{:s}/insights'.format(project.namespace, site.slug),
            status=200)
        assert 'Insights - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_settings(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # publication
        site = project.sites.where(Site.slug == 'playing-piano').get()
        res = app.get(
            '/{:s}/{:s}/settings'.format(project.namespace, site.slug),
            status=200)
        assert 'General Settings - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()

        # application
        site = project.sites.where(Site.slug == 'playing-piano-notes').get()
        res = app.get(
            '/{:s}/{:s}/settings'.format(project.namespace, site.slug),
            status=200)
        assert 'General Settings - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_settings_scripts(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # application
        site = project.sites.where(Site.slug == 'playing-piano-notes').get()
        res = app.get(
            '/{:s}/{:s}/settings/scripts'.format(project.namespace, site.slug),
            status=200)
        assert 'Measure Scripts - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_settings_widgets(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # application
        site = project.sites.where(Site.slug == 'playing-piano-notes').get()
        res = app.get(
            '/{:s}/{:s}/settings/widgets'.format(project.namespace, site.slug),
            status=200)
        assert 'Heatmap Widgets - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_settings_badges(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # application
        site = project.sites.where(Site.slug == 'playing-piano-notes').get()
        res = app.get(
            '/{:s}/{:s}/settings/badges'.format(project.namespace, site.slug),
            status=200)
        assert 'Status Badges - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_site_overview(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # application
        site = project.sites.where(Site.slug == 'playing-piano-notes').get()
        res = app.get(
            '/{:s}/{:s}'.format(project.namespace, site.slug),
            status=200)
        assert 'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_article_list(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # publication
        site = project.sites.where(Site.slug == 'playing-piano').get()
        res = app.get(
            '/{:s}/{:s}/articles'.format(project.namespace, site.slug),
            status=200)
        assert 'Articles - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()


@pytest.mark.usefixtures('login')
def test_title_article_editor_new(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        project = user.projects.where(
            Project.namespace == 'piano-music-club').get()
        # publication
        site = project.sites.where(Site.slug == 'playing-piano').get()
        # new
        res = app.get(
            '/{:s}/{:s}/editor'.format(project.namespace, site.slug),
            status=200)
        assert 'Create a New Article - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()

        article = site.instance.articles.where(
            Article.path == 'piano-lesson').get()
        # edit
        res = app.get(
            '/{:s}/{:s}/editor?code={:s}'.format(
                project.namespace, site.slug, article.code),
            status=200)
        assert 'Piano Lesson - ' \
               'How to score music playing piano - ' \
               'Oswald & Weenie\'s Piano Music Club - Scrolliris' == \
            res.html.title.text.strip()
