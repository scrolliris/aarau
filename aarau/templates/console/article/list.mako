<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s} - {:s}'.format(_('title.article.list'), site.instance.name, project.name))}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/article/_breadcrumb_parent_items.mako'/>
  <span class="item active">Articles</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/article/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="article" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-8">
        <h4>${site.instance.name}</h4>
        <label class="publication label">scrolliris.com</label>
      </div>
      <div class="column-8" align="right">
        <a class="primary flat button" href="${req.route_path('console.article.editor.new', namespace=project.namespace, slug=site.slug)}">New Article</a>
      </div>
    </div>

    <div class="row">
      <div class="article-list column-16">
        % for article in articles:
        <div class="container">
          <div class="embedded attached article box" align="left">
            <div class="col">
              <a href="${req.route_path('console.article.editor.edit', namespace=project.namespace, slug=site.slug, _query={'code': article.code})}">
                <h6 class="title">${article.title or 'Untitled'}</h6>
                <span class="label progress_state ${article.progress_state}"></span>
              </a>
            </div>
            <div class="col">
              <p class="content">${util.truncate(article.content, length=80)}</p>
            </div>
          </div>
          <div class="embedded attached article footer message">
            <div class="col"></div>
            <div class="col">
              % if article.chapter:
              <a href="${req.route_path('console.chapter.edit', namespace=project.namespace, slug=site.slug, chapter_slug=article.chapter.slug)}">
                <span class="chapter-name">${article.chapter.name}</span>
              </a>
              % else:
                <span class="chapter-name">None</span>
              % endif
              <span class="updated_at">${article.updated_at}</span>
            </div>
          </div>
        </div>
        % endfor
      </div>
    </div>
  </div>
</div>
