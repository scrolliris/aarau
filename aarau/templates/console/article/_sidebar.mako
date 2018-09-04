<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <a class="item" href="${req.route_path('console.site.overview', namespace=project.namespace, slug=site.slug)}">Overview</a>
  <a class="active item" href="${req.route_path('console.article.list', namespace=project.namespace, slug=site.slug)}">Articles</a>
  <a class="disabled item">Insights</a>
  <a class="disabled item">Downloads</a>
  <a class="item" href="${req.route_path('console.site.settings', namespace=project.namespace, slug=site.slug)}">Settings</a>

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
