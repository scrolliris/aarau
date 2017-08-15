<%inherit file='../_layout.mako'/>

<%block name='title'>
  Settings - Email | Scrolliris
</%block>

<%
  err_msg = (req.session.pop_flash('error') or [None])[0]
  wrn_msg = (req.session.pop_flash('warning') or [None])[0]
  suc_msg = (req.session.pop_flash('success') or [None])[0]

  def render_errors(field):
      return ''.join(['<span class="small text">{}</span>'.format(e) for e in field.errors])


  def t(text, length=25, suffix='...'):
      txt = str(text)
      if len(txt) <= length:
          return txt
      else:
          return txt[:length - len(suffix)] + suffix
%>

<%def name="delete_email_form(f, ue)">
  % if f:
    <form id="delete_email_${ue.id}" class="delete-email form" action="${req.route_url('settings.email_delete')}" method="post">
    ${f.csrf_token}
    ${f.email(value=ue.email)}
    <button type="submit" name="submit" class="flat button" data-tooltip="Cannot undo this action" data-inverted="" data-position="top center" data-variation="small">
      Delete
    </button>
  </form>
  % endif
</%def>

<%def name="change_email_form(f, ue)">
  % if f:
    <form id="change_email_${ue.id}" class="change-email form" action="${req.route_url('settings.email_change')}" method="post">
    ${f.csrf_token}
    ${f.email(value=ue.email)}
    <button type="submit" name="submit" class="button">
      Set as primary
    </button>
  </form>
  % endif
</%def>

<div class="content">
  <div id="settings">
    <div class="grid">
      <div class="row">
        <div class="column-3 offset-2 column-v-4 offset-v-1 column-l-16">
          <%include file='_menu.mako'/>
        </div>

        <div class="column-8 column-v-10 column-l-16">

          % if err_msg:
          <div class="error message" role="alert">${err_msg}</div>
          % elif wrn_msg:
          <div class="warning message" role="alert">${wrn_msg}</div>
          % elif suc_msg:
          <div class="success message" role="alert">${suc_msg}</div>
          % endif

          <div class="attached header"><h6>Email</h6></div>
          <div class="attached box">
            <table class="table">
              <tbody>
                % for ue in user_emails:
                  <%
                    email = t(ue.email, length=35)
                    email_form = email_forms[ue.id]
                  %>
                  <tr>
                    % if ue.type == 'primary':
                      <td>
                        <span class="small text">${email}</span>
                        <span class="primary rounded label">Primary</span>
                      </td>
                      <td class="action">
                        <button class="disabled flat button">
                          Delete
                        </button>
                      </td>
                    % else:
                      % if ue.activation_state != 'pending':
                        <td>
                          <span class="small text">${email}</span>
                        </td>
                        <td class="action">
                          ${change_email_form(email_form['change'], ue)}
                          ${delete_email_form(email_form['delete'], ue)}
                        </td>
                      % else:
                        <td>
                          <span class="small text">${email}</span>
                          <span class="negative rounded label">Pending</span>
                        </td>
                        <td class="action">
                          <button class="flat button">
                            Resend confirmation email
                          </button>

                          ${delete_email_form(email_form['delete'], ue)}
                        </td>
                      % endif
                    % endif
                  </tr>
                % endfor
              </tbody>
            </table>

            <form id="add_new_email" class="form${' error' if err_msg else ' success' if suc_msg else ''}" action="${req.route_url('settings.section', section='email')}" method="post">
              ${form.csrf_token}
              <div class="row">
                <div class="required field-10 ${' error' if form.new_email.errors else ''}">
                  <label class="label" for="new_email">New email address</label>

                  ${form.new_email(class_='', placeholder='new@example.org')}
                  ${render_errors(form.new_email)|n}
                </div>
              </div>
              ${form.submit(class_='primary button')}
            </form>
          </div>
          <div class="attached message">
            <div class=header"><h6>Note</h6></div>
            <p><label class="rounded primary label">Primary</label> email address will be used for login to your account.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
