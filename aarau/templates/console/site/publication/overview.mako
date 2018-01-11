<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Site | Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.site.publication.overview', project_id=project.id, id=site.id, _query={'type': 'publication'})}">${publication.name}</a>
  <span class="divider">/</span>
  <span class="item active">Overview</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/publication/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="project" class="content">
  ${render_notice()}

  <div class="grid">
    <div class="row">
      <div class="column-16">
        <h3>${publication.name}</h3>
        <label class="primary rounded label">${site.domain}</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="tab menu">
          <a class="active item">Repository</a>
          <a class="disabled item">Authors</a>
        </div>
      </div>

      <div class="column-16">
      </div>
    </div>
  </div>
</div>