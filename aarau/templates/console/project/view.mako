<%inherit file='../_layout.mako'/>

<%block name='title'>
  Project | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <span class="item active">${project.name}</span>
</div>
</%block>

<div id ="publication" class="content">
  <%namespace name='msg' file='../../shared/_message.mako'/>
  ${msg.form()}

  <div class="grid">
    <div class="row">
      <div class="column-16">
        <h3>${project.name}</h3>
        <label class="primary label">${project.namespace}</label>
        <p class="description">${project.description}</p>
        <form class="inline form" method="get" action="${req.route_path('console.site.new', project_id=project.id)}">
          <div class="field-2 field-v-4 field-l-16">
            <select name="type">
              <option value="application">Application</option>
              <option disabled="disabled" value="publication">Publication</option>
            </select>
          </div>
          <div class="field-3 field-v-6 field-l-16">
            <input class="primary button" type="submit" value="New Site">
          </div>
        </form>
      </div>
    </div>
    <div class="row">
    % for site in project.application_sites():
      <div class="column-4 column-v-8 column-l-16">
        <div class="blue flat box">
          <a href="${req.route_path('console.site.view', project_id=project.id, id=site.id, _query={'type':'application'})}"><h6 class="header">${util.truncate(site.application.name, 25)}</h6></a>
          <label class="secondary label">${site.domain}</label>
          <p class="text">${util.truncate(site.application.description, 30)}</p>
          <p class="link"><a class="petit flat button" href="${req.route_path('console.site.edit', project_id=project.id, id=site.id)}">Edit</a></p>
        </div>
      </div>
    % endfor
    % for site in project.publication_sites():
      <div class="column-4 column-v-8 column-l-16">
        <div class="gray flat box">
          <h6 class="header">${util.truncate(site.publication.name, 25)}</h6>
          <label class="secondary label">${site.domain}</label>
          <p class="text">${util.truncate(site.publication.description, 30)}</p>
        </div>
      </div>
    % endfor
    </div>
  </div>
</div>

<%block name='footer'>
</%block>
