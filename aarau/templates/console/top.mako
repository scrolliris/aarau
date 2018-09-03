<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Console')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <span class="active item">Projects</span>
</div>
</%block>

<div id="top" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <a class="primary flat button" href="${req.route_path('console.project.new')}">New Project</a>
      </div>
    % for project in projects:
      <div class="column-4 column-v-8 column-l-16">
        <div class="attached box">
          <a href="${req.route_url('console.project.overview', namespace=project.namespace)}"><h4 class="header">${project.name}</h4></a>
          <label class="primary label">${project.plan.name}</label>
          <p>${project.description}</p>
          <a class="petit flat button" href="${req.route_path('console.project.edit', namespace=project.namespace)}">Edit</a>
        </div>
        <div class="attached message">
          <p class="text">${project.namespace}</p>
        </div>
      </div>
    % endfor
    </div>
  </div>
</div>
