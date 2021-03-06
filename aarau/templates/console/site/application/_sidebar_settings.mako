<div class="sidebar">
  <% locked = cookie.get('console.sidebar') %>
  <%include file='aarau:templates/shared/_sidebar_navi.mako' args="locked=locked,"/>

  <a class="item" href="${req.route_path('console.site.overview', namespace=project.namespace, slug=site.slug)}">Overview</a>
  <a class="item" href="${req.route_path('console.site.insights', namespace=project.namespace, slug=site.slug)}">Insights</a>
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
      ${link_to('console.site.settings.scripts', _('title.settings.scripts'))}
      ${link_to('console.site.settings.widgets', _('title.settings.widgets'))}
      ${link_to('console.site.settings.badges', _('title.settings.badges'))}
    </span>
  </span>

  <hr class="divider">
  <%include file='aarau:templates/shared/_sidebar_bottom_console.mako' />

  ## desktop only
  <div class="bottom note item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
