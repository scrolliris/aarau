<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title(_('title.console'))}</%block>

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
          <p>${project.description}</p>
          <%
            members_count = len(project.users)
          %>
          <span>${members_count} ${'members' if members_count > 1 else 'member'}</span>
        </div>
        <div class="attached message">
          <pre>${project.namespace}</pre>
        </div>
      </div>
    % endfor
    </div>
  </div>
</div>
