<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <a class="item" href="${req.route_path('console.site.overview', namespace=project.namespace, slug=site.slug)}">Overview</a>

  <span class="item active expanded">
    <span class="item">Documents</span>
    <span class="item-container">
      <a class="item" href="${req.route_path('console.chapter.tree', namespace=project.namespace, slug=site.slug)}">Chapters Tree</a>
      <a class="${'active ' if not util.route_name.startswith('console.article.editor') else ''}item" href="${req.route_path('console.article.list', namespace=project.namespace, slug=site.slug)}">All Articles</a>
    </span>
  </span>

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
