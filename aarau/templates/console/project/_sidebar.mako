<div class="sidebar">
  <div class="item">
    <a href="${req.route_url('console.top')}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
  </div>
  <span class="item active">
    <%def name="link_to(route_name, type_name, text, default_link=False)">
      <a class="${site_item_class(route_name, type_name, default_link)}" href="${req.route_url(route_name, id=project.id, _query={'type': type_name})}">${text}</a>
    </%def>

    <%def name="site_item_class(route_name, type_name, default_link)">
      <% type_ = req.params.get('type', '') %>
      %if util.route_name == route_name and (type_ == type_name or (type_ == '' and default_link)):
        <% return 'active item' %>
      %else:
        <% return 'item' %>
      %endif
    </%def>

    <span class="item">Scrolls</span>
    <span class="item-container">
      ${link_to('console.project.view', 'publication', 'Publications', default_link=True)}
      ${link_to('console.project.view', 'application', 'Applications')}
    </span>
  </span>
  <a class="disabled item">Members</a>
  <a class="disabled item">Settings</a>

  <div class="bottom item">
    <%include file='aarau:templates/console/_sidebar_note.mako'/>
  </div>
</div>
