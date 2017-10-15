<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('Password - Settings')}</%block>

<div class="content">
  <div id="settings">
    <div class="grid">
      <div class="column-3 offset-2 column-v-4 offset-v-1 column-l-16">
        <%include file='aarau:templates/settings/_menu.mako'/>
      </div>

      <div class="column-8 column-v-10 column-l-16">
        ${render_notice()}

        <div class="attached header"><h6>Password</h6></div>
        <div class="attached box">

          <form id="change_password" class="form${' error' if err_msg else ' success' if suc_msg else ''}" action="${req.route_url('settings.section', section='password', subdomain='')}" method="post">
            ${form.csrf_token}
            <div class="row">
              <div class="required field-10${' error' if form.current_password.errors else ''}">
                <label class="label" for="current_password">Current password</label>
                ${form.current_password(class_='')}
                ${render_error_message(form.current_password)}
              </div>

              <div class="required field-10${' error' if form.new_password.errors else ''}">
                <label class="label" for="new_password">New password</label>
                ${form.new_password(class_='')}
                ${render_error_message(form.new_password)}
              </div>

              <div class="required field-10${' error' if form.new_password_confirmation.errors else ''}">
                <label class="label" for="new_password_confirmation">New password confirmation</label>
                ${form.new_password_confirmation(class_='')}
                ${render_error_message(form.new_password_confirmation)}
              </div>
            </div>
            ${form.submit(class_='primary button')}
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
