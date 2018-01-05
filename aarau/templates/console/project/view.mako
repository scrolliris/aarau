<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <span class="item active">${project.name}</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/project/_sidebar.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="project" class="content">
  ${render_notice()}

  <div class="grid">
    <div class="row">
      <div class="column-16">
        <h4>${project.name}</h4>
        <label class="primary label">${project.namespace}</label>

        <p class="description">${project.description}</p>
        <form class="inline form" method="get" action="${req.route_path('console.site.{:s}.new'.format(hosting_type), project_id=project.id)}">
          <input type="hidden" name="type" value="${hosting_type}">
          <input class="primary button" type="submit" value="New Site">
        </form>
      </div>
    </div>

    <div class="row">
    % if hosting_type == 'publication':
      % for site in project.publication_sites:
        <div class="column-4 column-v-8 column-l-16">
          <div class="gray flat site box">
            <a href="${req.route_path('console.site.publication.overview', project_id=project.id, id=site.id, _query={'type':'publication'})}"><h5 class="header">${util.truncate(site.publication.name, 25)}</h5></a>
            <label class="secondary rounded label">${site.domain}</label>
            <p class="text">${util.truncate(site.publication.description, 30)}</p>
          </div>
        </div>
      % endfor
    % elif hosting_type == 'application':
      % for site in project.application_sites:
        <div class="column-4 column-v-8 column-l-16">
          <div class="blue flat site box">
            <a href="${req.route_path('console.site.application.overview', project_id=project.id, id=site.id, _query={'type':'application'})}"><h5 class="header">${util.truncate(site.application.name, 25)}</h5></a>
            <label class="secondary rounded label">${site.domain}</label>
            <p class="text">${util.truncate(site.application.description, 30)}</p>
          </div>
        </div>
      % endfor
    % endif
    </div>
  </div>
</div>
