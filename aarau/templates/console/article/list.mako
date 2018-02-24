<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Articles | Site | Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
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
      <div class="column-2">
        <h3>Articles</h3>
      </div>
      <div class="column-14" align="right">
        <a class="primary flat button" href="${req.route_path('console.article.new', namespace=project.namespace, slug=site.slug)}">New Article</a>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        % for article in articles:
        <div class="embedded flat article box" align="left">
          <a href="${req.route_path('console.article.edit', namespace=project.namespace, slug=site.slug, path=article.path)}">
            <h5 class="title">${article.title}</h5>
          </a>
          <p class="path">${article.path}</p>
          <span class="primary lined label">${article.progress_state}</span>
        </div>
        % endfor
      </div>

      <div class="column-16">
      </div>
    </div>
  </div>
</div>
