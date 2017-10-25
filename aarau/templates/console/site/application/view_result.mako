<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Site | Project')}</%block>
<%block name='body_attr'> data-locale-file="${req.util.static_url('{}')|unquote,formatting('locale/{{lng}}/{{ns}}.json'),h}"</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="item active">${application.name}</span>
</div>
</%block>

<%block name='footer'>
</%block>

<div id ="project" class="content">
  ${render_notice()}

  <div class="grid">
    <div class="row">
      <div class="column-16">
        <h3>${application.name}</h3>
        <label class="primary label">${site.domain}</label>
      </div>
    </div>
    <div class="row">
      <div class="column-16">
        <div class="tab menu">
          <a class="active item">Results</a>
          <a class="item" href="${req.route_path('console.site.application.view.script', project_id=project.id, id=site.id, _query={'type': 'application'})}">Scripts</a>
          <a class="item" href="${req.route_path('console.site.application.view.badge', project_id=project.id, id=site.id, _query={'type': 'application'})}">Badges</a>
        </div>
      </div>
      <div class="column-16">
        <h5>Pages</h5>
        <div id="page_table_container" data-project-id="${project.id}", data-site-id="${site.id}"></div>
      </div>
    </div>
  </div>
</div>
