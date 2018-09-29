<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Email - Settings')}</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/_sidebar.mako'/>
</%block>

<%
  is_failure = (len(req.session.peek_flash('failure')) > 0)
  is_success = (len(req.session.peek_flash('success')) > 0)
%>

<%def name="delete_email_form(f, ue)">
% if f:
  <form id="delete_email_${ue.id}" class="delete-email form" action="${req.route_url('console.settings.email_delete')}" method="post">
    ${f.csrf_token}
    ${f.email(value=ue.email)}
    <button type="submit" name="submit" class="flat petit secondary button" data-tooltip="Cannot undo this action">Delete</button>
  </form>
% endif
</%def>

<%def name="change_email_form(f, ue)">
  % if f:
    <form id="change_email_${ue.id}" class="change-email form" action="${req.route_url('console.settings.email_change')}" method="post">
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
        <div class="column-16">
          ${render_notice()}
        </div>
      </div>

      <div class="row">
        <div class="column-16">
          <div class="attached header"><h5>Email</h5></div>
          <div class="attached box">
            <div class="row">
              <div class="column-9 column-v-12 column-l-16">
                <table class="emails table">
                  <tbody>
                    % for ue in user_emails:
                    <%
                      email = util.truncate(ue.email, length=35)
                      email_form = email_forms[ue.id]
                    %>
                    <tr>
                      <td>
                      % if ue.type == 'primary':
                        <span class="small text">${email}</span>
                        <span class="primary label">Primary</span>
                        <div class="action right">
                          <button class="disabled flat petit secondary button">Delete</button>
                        </div>
                      % elif ue.activation_state != 'pending':
                        <span class="small text">${email}</span>
                        <div class="action right">
                          ${change_email_form(email_form['change'], ue)}
                          ${delete_email_form(email_form['delete'], ue)}
                        </div>
                      % else:
                        <span class="small text">${email}</span>
                        <span class="negative label">Pending</span>
                        <div class="action right">
                          <button class="flat petit button">Resend confirmation</button>
                          ${delete_email_form(email_form['delete'], ue)}
                        </div>
                      % endif
                      </td>
                    </tr>
                    % endfor
                  </tbody>
                </table>
              </div>
            </div>

            <form id="add_new_email" class="form${' error' if is_failure else ' success' if is_success else ''}" action="${req.route_url('console.settings.section', section='email')}" method="post">
              ${form.csrf_token}
              <div class="row">
                <div class="required field-8 field-v-12 field-l-16${' error' if form.new_email.errors else ''}">
                  <label class="label" for="new_email">New email address</label>

                  ${form.new_email(class_='', placeholder='new@example.org')}
                  ${render_error_message(form.new_email)}
                </div>
              </div>
              ${form.submit(class_='primary flat button')}
            </form>
          </div>
          <div class="attached message">
            <div class="header"><h6>Note</h6></div>
            <p>Primary email address will be used for login to your account.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
