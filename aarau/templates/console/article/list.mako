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
        <div class="embedded flat article box" align="left">
          <a href="${req.route_path('console.article.editor.edit', namespace=project.namespace, slug=site.slug, _query={'code': article.code})}">
            <h5 class="title">${article.title or 'Untitled'}</h5>
          </a>
          <p class="path">${article.path or 'none'}</p>
          <span class="state">${article.progress_state}</span>
        </div>
        % endfor
      </div>

      <div class="column-16">
      </div>
    </div>
  </div>
</div>
