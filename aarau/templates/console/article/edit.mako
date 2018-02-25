<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Edit Article')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <%include file='aarau:templates/console/article/_breadcrumb_parent_items.mako'/>
  <a class="item" href="${req.route_path('console.article.list', namespace=project.namespace, slug=site.slug)}">Articles</a>
  <span class="divider">/</span>
  <span class="active item">Edit</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/article/_sidebar.mako'/>
</%block>

<%block name='right_menu'>
<div class="right menu">
  <label class="item toolbar-show-button" for="toolbar_checkbox" title="Show Toolbar">&#9881;</label>
</div>
</%block>

<div id="article" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <%
          act = req.route_path('console.article.edit', namespace=project.namespace, slug=site.slug, path=article.path)
          ctx = 'edit'
          err = ''
          obj = None
        %>
        <%include file="aarau:templates/console/article/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>

<%block name='toolbar_checkbox'>
  <input type="checkbox" id="toolbar_checkbox" class="toolbar-checkbox">
</%block>
<%block name='toolbar'>
  <div class="toolbar sidebar">
    <%include file='aarau:templates/shared/_toolbar_navi.mako'/>
    <h6 class="section-title">Article Configuration</h6>
    <hr>

    <%namespace file='aarau:templates/macro/_error_message.mako' import='render_error_message'/>
    <form id="article_settings" class="form" action="${req.route_path('console.article.new', namespace=project.namespace, slug=site.slug)}" method="post">
    ${form.csrf_token}

    <div class="row">
      <div class="field-16">
        <label class="label" for="path">Path</label>
        <input type="text" value="${article.path}" disabled>
      </div>
    </div>
    ${form.submit(class_='primary flat button')}
    </form>
  </div>
</%block>

<%block name='footer'>
</%block>
