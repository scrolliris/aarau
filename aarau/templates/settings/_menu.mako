<%def name="item_class_in_section(section, default=False)">
  %if (default and util.route_name == 'settings') or util.is_matched({'section': section}):
    <% return 'active item' %>
  %else:
    <% return 'item' %>
  %endif
</%def>

<div class="vertical menu">
  <a class="${item_class_in_section('account', default=True)}" href="${req.route_path('settings.section', section='account')}">Account</a>
  <a class="${item_class_in_section('email')}" href="${req.route_path('settings.section', section='email')}">Email</a>
  <a class="${item_class_in_section('password')}" href="${req.route_path('settings.section', section='password')}">Password</a>
</div>
