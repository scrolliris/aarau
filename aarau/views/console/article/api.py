from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from aarau.models.article import Article
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.filter import login_required
from aarau.views.console.article.form import (
    build_article_editor_form,
    build_article_settings_form,
)


def save_content(req, article):
    form = build_article_editor_form(req, article)

    if form.validate():
        with req.db.cardinal.atomic():
            article.content = form.content.data or ''

            article.save()

    return (article, form.errors)


def save_meta(req, article):
    form = build_article_settings_form(req, article)

    if form.validate():
        with req.db.cardinal.atomic():
            article.title = form.title.data
            article.scope = 'private' if not form.scope.data else 'public'
            article.progress_state = Article.progress_states[
                int(form.progress_state.data)]
            # optional
            article.path = form.path.data

            article.save()

    return (article, form.errors)


def handle_post(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    code = req.params.get('code')  # update

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    if code:
        try:
            article = publication.articles.where(
                Article.code == code).get()
        except Article.DoesNotExist:
            article = None

    if not article:
        code = Article.grab_unique_code()
        article = Article(
            code=code,
            path=code,
            title='Untitled',
            copyright='',
            publication=publication)

    context = req.params.get('context', None)
    _ = req.translate
    if context == 'editor':
        (article, errors) = save_content(req, article)
    elif context == 'settings':
        (article, errors) = save_meta(req, article)
    else:
        raise HTTPNotFound

    message = _('article.save.failure')
    if not errors:
        message = _('article.save.success')

    return dict(
        status='ok',
        code=article.code,
        errors=errors,
        message=message)


@view_config(route_name='console.api.article.settings',
             request_method='POST',
             renderer='json')
@login_required
def api_article_settings(req):
    try:
        return handle_post(req)
    except HTTPNotFound:
        return Response(status=404, json_body={
            'status': 'error',
            'error': 'The resource was not found'})


@view_config(route_name='console.api.article.editor',
             request_method='POST',
             renderer='json')
@login_required
def api_article_editor(req):
    try:
        return handle_post(req)
    except HTTPNotFound:
        return Response(status=404, json_body={
            'status': 'error',
            'error': 'The resource was not found'})


@view_config(route_name='console.api.article.progress_states',
             request_method='GET',
             renderer='json')
@login_required
def api_article_progress_states(req):
    try:
        namespace = req.matchdict.get('namespace')
        slug = req.matchdict.get('slug')
        code = req.matchdict.get('code')

        project = get_project(namespace, user=req.user)
        site = get_site(slug, project=project)

        if site.type != 'publication':
            raise HTTPNotFound

        publication = site.instance

        article = publication.articles.where(
            Article.code == code).get()
        states = article.available_progress_states_as_choices
    except (HTTPNotFound, Article.DoesNotExist):
        article = None
        states = Article.progress_state_as_choices

    data = {}
    current_state = article.progress_state if article else 'draft'
    for (i, v) in enumerate(Article.progress_states):
        data[v] = {'value': i, 'label': v}
        if (str(i), v) not in states:
            data[v]['disabled'] = True
        elif v == current_state:
            data[v]['selected'] = True

    return dict(
        status='ok',
        data=data,
        errors=[],
        message='')
