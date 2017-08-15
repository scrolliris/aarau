<%inherit file='../_layout-basic.mako'/>

<%block name='title'>
  Log in |
</%block>

<%
  err_msg = (req.session.pop_flash('error') or [None])[0]
  suc_msg = (req.session.pop_flash('success') or [None])[0]

  def render_errors(field):
      return ''.join(['<span class="error">{}</span>'.format(e) for e in field.errors])
%>

<div class="content">
  <div class="login grid">
    <div class="row">
      <div class="column-6 offset-5 column-v-8 offset-v-4 column-l-10 offset-l-3 column-m-16">
        <div class="embeded box">
          <div class="header">
            <a href="${req.route_url('top', namespace=None)}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-32x32.png')}"></a>
          </div>
          <form id="login" class="form${' error' if err_msg  else ' success' if suc_msg else ''}" action="${req.route_url('login')}" method="post">
            <h4 class="header">Log in to Scrolliris</h4>
          % if err_msg:
            <div class="error message" role="alert">${err_msg}</div>
          % elif suc_msg:
            <div class="positive message" role="alert">${suc_msg}</div>
          % endif
            <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
            <input type="hidden" name="next" value="${next_path}">

            <div class="field">
              <label class="label" for="emai">Email</label>
              <input type="text" id="email" name="email" value="${email}" placeholder="Email address">
            </div>

            <div class="field">
              <label class="label" for="password">Password</label>
              <input type="password" id="password" name="password" placeholder="Secret password">
            </div>
            <button class="primary button" type="submit" name="submit" value="1">Log in</button>
          </form>
          <p><a href="${req.route_url('reset_password.request')}">Fogot your password?</a>&nbsp;or new to Scrolliris?&nbsp;<a class="link" href="${req.route_url('signup')}">Sign up</a></p>
        </div>
      </div>
    </div>
  </div>
</div>
