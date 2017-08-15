<%inherit file='_layout.mako'/>

<%block name='title'>
  Console | Scrolliris
</%block>

<%block name='breadcrumb'>
</%block>

<div id="top" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        <a class="primary${' disabled' if len(req.user.projects) >= 1 else ''} button" href="${req.route_path('console.project.new')}">New Project</a>
        <p class="note">You can create only one project while in beta.</p>
      </div>
    % for project in projects:
      <div class="column-4 column-v-8 column-l-16">
        <div class="attached box">
          <a href="${req.route_url('console.project.view', id=project.id)}"><h4 class="header">${project.name}</h4></a>
          <label class="primary label">${project.plan.name}</label>
          <p>${project.description}</p>
          <a class="petit flat button" href="${req.route_path('console.project.edit', id=project.id)}">Edit</a>
        </div>
        <div class="attached message">
          <p class="text">${project.namespace}</p>
        </div>
      </div>
    % endfor
    </div>
  </div>
</div>
