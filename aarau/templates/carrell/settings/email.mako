<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/carrell/_layout.mako'/>

<%block name='title'>${render_title('Email - Settings')}</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/carrell/settings/_sidebar.mako'/>
</%block>

<%
  is_failure = (len(req.session.peek_flash('failure')) > 0)
  is_success = (len(req.session.peek_flash('success')) > 0)
%>

<%def name="delete_email_form(f, ue)">
% if f:
  <form id="delete_email_${ue.id}" class="delete-email form" action="${req.route_url('carrell.settings.email_delete')}" method="post">
    ${f.csrf_token}
    ${f.email(value=ue.email)}
    <button type="submit" name="submit" class="flat petit button" data-tooltip="Cannot undo this action">Delete</button>
  </form>
% endif
</%def>

<%def name="change_email_form(f, ue)">
  % if f:
    <form id="change_email_${ue.id}" class="change-email form" action="${req.route_url('carrell.settings.email_change')}" method="post">
      ${f.csrf_token}
      ${f.email(value=ue.email)}
      <button type="submit" name="submit" class="flat petit button">Set as primary</button>
    </form>
  % endif
</%def>

<div class="content">
  <div id="settings">
    <div class="grid">
      <div class="row">
        <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16">
          ${render_notice()}

          <div class="attached header"><h6>Email</h6></div>
          <div class="attached box">
            <table class="table">
              <tbody>
                % for ue in user_emails:
                <%
                  email = req.util.truncate(ue.email, length=35)
                  email_form = email_forms[ue.id]
                %>
                <tr>
                  <td>
                  % if ue.type == 'primary':
                    <span class="small text">${email}</span>
                    <span class="primary rounded label">Primary</span>
                    <div class="action right">
                      <button class="disabled flat petit button">Delete</button>
                    </div>
                  % elif ue.activation_state != 'pending':
                    <span class="small text">${email}</span>
                    <div class="action right">
                      ${change_email_form(email_form['change'], ue)}
                      ${delete_email_form(email_form['delete'], ue)}
                    </div>
                  % else:
                    <span class="small text">${email}</span>
                    <span class="negative rounded label">Pending</span>
                    <div class="action right">
                      ${delete_email_form(email_form['delete'], ue)}
                      <button class="flat petit button">Resend confirmation email</button>
                    </div>
                  % endif
                  </td>
                </tr>
                % endfor
              </tbody>
            </table>

            <form id="add_new_email" class="form${' error' if is_failure else ' success' if is_success else ''}" action="${req.route_url('carrell.settings.section', section='email')}" method="post">
              ${form.csrf_token}
              <div class="row">
                <div class="required field-10 field-n-16${' error' if form.new_email.errors else ''}">
                  <label class="label" for="new_email">New email address</label>

                  ${form.new_email(class_='', placeholder='new@example.org')}
                  ${render_error_message(form.new_email)}
                </div>
              </div>
              ${form.submit(class_='primary button')}
            </form>
          </div>
          <div class="attached message">
            <div class="header"><h6>Note</h6></div>
            <p><label class="rounded primary label">Primary</label> email address will be used for login to your account.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
