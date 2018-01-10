<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

  <a class="item active">Overview</a>
  <a class="disabled item">Articles</a>
  <a class="disabled item">Insights</a>
  <a class="disabled item">Downloads</a>
  <a class="item" href="${req.route_url('console.site.publication.settings', project_id=project.id, id=site.id, _query={'type': 'publication'})}">Settings</a>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
