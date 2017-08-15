<%inherit file='../_layout-basic.mako'/>

<%block name='title'>
  Reset password | Scrolliris
</%block>

<%
  err_msg = (req.session.pop_flash('error') or [None])[0]
  suc_msg = (req.session.pop_flash('success') or [None])[0]
%>

<div class="content">
  <div class="reset-password grid">
    <div class="row">
      <div class="column-6 offset-5 column-v-8 offset-v-4 column-l-10 offset-l-3 column-m-16">
        <div class="embeded box">
          <div class="header">
            <a href="/"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-32x32.png')}"></a>
          </div>
          <form id="reset_password_request" class="form${' error' if err_msg else ' success' if suc_msg else ''}" action="${req.route_url('reset_password.request')}" method="post">
          % if suc_msg:
            <h4 class="header">Reset password</h4>
            <div class="positive message">${suc_msg}</div>
            <div class="field">
              <div class="description">
                <h6>NOTE</h6>
                <p>If you don't receive an email, and it's not in your spam folder,
                   this could mean you signed up with a different address.</p>
              </div>
            </div>
          % else:
            <h4 class="header">Reset password</h4>
          % if err_msg:
            <div class="error message" role="alert">${err_msg}</div>
          % endif
            ${form.csrf_token}

            <p class="description">Enter your email address below and we'll send you a link to reset your password.</p>

            <div class="required field${' error' if form.email.errors else ''}">
              ${form.email(class_='', placeholder='Email address')}
            </div>

            ${form.submit(class_='secondary button')}
          % endif
          </form>
          <p class="text"><a class="link" href="${req.route_url('login')}">Log in</a>&nbsp;or&nbsp;<a class="link" href="${req.route_url('signup')}">Sign up</a></p>
        </div>
      </div>
    </div>
  </div>
</div>
