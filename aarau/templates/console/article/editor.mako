<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Editor | Article')}</%block>
<%block name='body_attr'> data-locale-file="${req.util.static_url('{}')|unquote,formatting('locale/{{lng}}/{{ns}}.json'),h}"</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <%include file='aarau:templates/console/article/_breadcrumb_parent_items.mako'/>
  <a class="item" href="${req.route_path('console.article.list', namespace=project.namespace, slug=site.slug)}">Articles</a>
  <span class="divider">/</span>
  <span class="active item">Editor</span>
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
        ## Editor
        <div id="article_editor_form_container"
          data-action="${req.route_path('api.console.article.editor', namespace=project.namespace, slug=site.slug)}"
          data-csrf-token="${editor_form.csrf_token.current_token}"
          data-namespace="${project.namespace}"
          data-slug="${site.slug}"
          data-code="${article.code or ''}"
          data-content="${article.content or ''}"></div>
      </div>
    </div>
  </div>
</div>

<%block name='toolbar_checkbox'>
  % if article.code:
    <input type="checkbox" id="toolbar_checkbox" class="toolbar-checkbox">
  % else:
    <input type="checkbox" id="toolbar_checkbox" class="toolbar-checkbox" checked>
  % endif
</%block>
<%block name='toolbar'>
  <div class="toolbar sidebar">
    <%include file='aarau:templates/shared/_toolbar_navi.mako'/>
    <h6 class="section-title">Configuration</h6>
    <hr>
    ## Config
    <div id="article_config_form_container"
      data-action="${req.route_path('api.console.article.config', namespace=project.namespace, slug=site.slug)}"
      data-csrf-token="${config_form.csrf_token.current_token}"
      data-namespace="${project.namespace}"
      data-slug="${site.slug}"
      data-code="${article.code or ''}"
      data-path="${article.path or ''}"
      data-title="${article.title or ''}"></div>
  </div>
</%block>

<%block name='footer'>
</%block>
