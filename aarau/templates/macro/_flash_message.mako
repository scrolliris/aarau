<%block name='render_announcement'>
<%
  msg = (req.session.pop_flash('announcement') or [None])[0]
%>
% if msg:
  <div class="warning message" role="alert">
    <div class="header">NOTICE</div>
    <p>${msg}</p>
  </div>
% endif
</%block>

<%block name='render_notice'>
<%
  failure_message = (req.session.pop_flash('failure') or [None])[0]
%>
% if failure_message:
  <div class="failure error message" role="alert">
    <p>${failure_message}</p>
  </div>
% endif

<%
  success_message = (req.session.pop_flash('success') or [None])[0]
%>
% if success_message:
  <div class="success primary message" role="alert">
    <p>${success_message}</p>
  </div>
% endif

<%
  warning_message = (req.session.pop_flash('warning') or [None])[0]
%>
% if warning_message:
  <div class="warning warning message" role="alert">
    <p>${warning_message}</p>
  </div>
% endif
</%block>
