## msg.announcement()
<%block name='announcement'>
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

## msg.form()
<%block name='form'>
<%
  err_msg = (req.session.pop_flash('error') or [None])[0]
  suc_msg = (req.session.pop_flash('success') or [None])[0]
%>
% if err_msg:
  <div class="negative message" role="alert">
    <div class="header">VALIDATION FAILURE</div>
    <p>${err_msg}</p>
  </div>
% elif suc_msg:
  <div class="positive message" role="alert">
    <p>${suc_msg}</p>
  </div>
% endif
</%block>
