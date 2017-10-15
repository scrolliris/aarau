<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout-basic.mako'/>

<%block name='title'>${render_title('Reset password')}</%block>

<div class="content">
  <div class="reset-password grid">
    <div class="row">
      <div class="column-6 offset-5 column-v-8 offset-v-4 column-l-10 offset-l-3 column-m-16">
        <div class="embeded box">
          <div class="header">
            <a href="/"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-32x32.png')}"></a>
          </div>
          <form id="reset_password" class="form${' error' if err_msg else ''}" action="${req.route_url('reset_password', token=token)}" method="post">
            ${form.csrf_token}

            <h4 class="header">Reset password</h4>
            ${render_notice()}

            <p class="description">At least, use one lower and one UPPER letter <code>A-z</code>, and one digit from: <code>0-9</code>. 8 characters are minimum length. Make it strong.</p>
            <div class="required field${' error' if form.new_password.errors else ''}">
              <label class="label" for="new_password">New password</label>
              ${form.new_password(class_='', placeholder='Don\'t foget :)')}
              ${render_error_message(form.new_password)}
            </div>

            <div class="required field${' error' if form.new_password_confirmation.errors else ''}">
              <label class="label" for="new_password_confirmation">New password confirmation</label>
              ${form.new_password_confirmation(class_='')}
              ${render_error_message(form.new_password_confirmation)}
            </div>

            ${form.submit(class_='secondary button')}
          </form>
          <p class="text"><a class="link" href="${req.route_path('login')}">Log in</a>&nbsp;or Go to&nbsp;<a class="link" href="/">Top</a></p>
        </div>
      </div>
    </div>
  </div>
</div>
