<div class="sidebar">
  <%include file='aarau:templates/console/_sidebar_navi.mako'/>

  <a class="item" href="${req.route_path('console.site.overview', namespace=project.namespace, slug=site.slug)}">Overview</a>
  <a class="disabled item">Articles</a>
  <a class="disabled item">Insights</a>
  <a class="disabled item">Downloads</a>

  <span class="item active expanded">
    <%def name="link_to(route_name, text)">
      % if util.route_name == route_name:
        <a class="active item" href="${req.route_url(route_name, namespace=project.namespace, slug=site.slug)}">${text}</a>
      % else:
        <a class="item" href="${req.route_url(route_name, namespace=project.namespace, slug=site.slug)}">${text}</a>
      % endif
    </%def>

    <span class="item">Settings</span>
    <span class="item-container">
      ${link_to('console.site.settings', 'General')}
    </span>
  </span>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
