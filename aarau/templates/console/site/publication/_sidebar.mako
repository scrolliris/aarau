<div class="sidebar">
  <div class="item">
    <a href="${req.route_url('console.top')}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
  </div>
  <a class="item active">Overview</a>
  <a class="disabled item">Articles</a>
  <a class="disabled item">Insights</a>
  <a class="disabled item">Downloads</a>
  <a class="item" href="${req.route_url('console.site.publication.settings', project_id=project.id, id=site.id, _query={'type': 'publication'})}">Settings</a>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
