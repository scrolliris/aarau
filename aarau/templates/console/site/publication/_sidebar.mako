<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

  <a class="item active">Overview</a>
  <a class="disabled item">Articles</a>
  <a class="disabled item">Insights</a>
  <a class="disabled item">Downloads</a>
  <a class="item" href="${req.route_url('console.site.settings', namespace=project.namespace, slug=site.slug)}">Settings</a>

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
