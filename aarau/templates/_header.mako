<%block name='header'>
<div class="global-message${' user' if req.user else ''}">
% if util.route_name == 'signup' or (util.route_name == 'top' and not req.user):
  <p>Increase your Text Readability</p>
% else:
  <div id="ticker" class="pride"></div>
% endif
</div>
</%block>
