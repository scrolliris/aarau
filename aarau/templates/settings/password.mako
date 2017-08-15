<%inherit file='../_layout.mako'/>

<%block name='title'>
  Settings - Password | Scrolliris
</%block>

<%
  err_msg = (req.session.pop_flash('error') or [None])[0]
  suc_msg = (req.session.pop_flash('success') or [None])[0]

  def render_errors(field):
      return ''.join(['<span class="small text">{}</span>'.format(e) for e in field.errors])
%>

<div class="content">
  <div id="settings">
    <div class="grid">
      <div class="column-3 offset-2 column-v-4 offset-v-1 column-l-16">
        <%include file='_menu.mako'/>
      </div>

      <div class="column-8 column-v-10 column-l-16">

        % if err_msg:
        <div class="error message" role="alert">${err_msg}</div>
        % elif suc_msg:
        <div class="success message">${suc_msg}</div>
        % endif

        <div class="attached header"><h6>Password</h6></div>
        <div class="attached box">

          <form id="change_password" class="form${' error' if err_msg else ' success' if suc_msg else ''}" action="${req.route_url('settings.section', section='password', subdomain='')}" method="post">
            ${form.csrf_token}
            <div class="row">
              <div class="required field-10${' error' if form.current_password.errors else ''}">
                <label class="label" for="current_password">Current password</label>
                ${form.current_password(class_='')}
                ${render_errors(form.current_password)|n}
              </div>

              <div class="required field-10${' error' if form.new_password.errors else ''}">
                <label class="label" for="new_password">New password</label>
                ${form.new_password(class_='')}
                ${render_errors(form.new_password)|n}
              </div>

              <div class="required field-10${' error' if form.new_password_confirmation.errors else ''}">
                <label class="label" for="new_password_confirmation">New password confirmation</label>
                ${form.new_password_confirmation(class_='')}
                ${render_errors(form.new_password_confirmation)|n}
              </div>
            </div>
            ${form.submit(class_='primary button')}
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
