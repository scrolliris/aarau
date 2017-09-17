<%inherit file='../../_layout.mako'/>

<%block name='title'>
  Site | Project | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="item active">${application.name}</span>
</div>
</%block>

<div id ="project" class="content">
  <%namespace name='msg' file='../../../shared/_message.mako'/>
  ${msg.form()}

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
      % if not results:
        <div class="info message">
          <h6>Are you ready?</h6>
          <p>Otherwise, please check `Scripts` tab. It takes few minutes stating logging and calculation. The data will be shown here. Please access again, later :-D</p>
        </div>
      % else:
        <h5>Pages</h5>
        <table class="bordered table">
          <thead>
            <tr>
              <th>Path</th>
              <th>Paragraph</th>
              <th>Record Count</th>
            </tr>
          </thead>
          <tbody>
          % for r in results:
            <tr>
              <td>${r.path}</td>
              <td>${r.paragraph_numbers}</td>
              <td>${r.total_count}</td>
            </tr>
          % endfor
          </tbody>
        </table>
      % endif
      </div>
    </div>
  </div>
</div>

<%block name='footer'>
</%block>
