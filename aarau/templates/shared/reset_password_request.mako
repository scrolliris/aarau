<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout-basic.mako'/>

<%block name='title'>${render_title('Reset password')}</%block>

<%
  is_failure = (len(req.session.peek_flash('failure')) > 0)
  is_success = (len(req.session.peek_flash('success')) > 0)
%>

<div class="content">
  <div class="reset-password grid">
    <div class="row">
      <div class="column-6 offset-5 column-v-8 offset-v-4 column-l-10 offset-l-3 column-m-16">
        <div class="embeded box">
          <div class="header">
            <a href="/"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-32x32.png')}"></a>
          </div>
          <form id="reset_password_request" class="form${' error' if is_failure else ''}" action="${req.route_url('reset_password.request')}" method="post">
            ${form.csrf_token}

            <h4 class="header">Reset password</h4>
            ${render_notice()}

          % if is_success:
              <div class="field">
                <div class="description">
                  <h6>NOTE</h6>
                  <p>If you don&apos;t receive an email, and it&apos;s not in your spam folder,
                     this could mean you signed up with a different address.</p>
                </div>
              </div>
          % else:
            <p class="description">Enter your email address below and we&apos;ll send you a link to reset your password.</p>

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
