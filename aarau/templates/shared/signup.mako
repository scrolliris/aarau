<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('Sign up')}</%block>

<%
  is_failure = (len(req.session.peek_flash('failure')) > 0)
  is_success = (len(req.session.peek_flash('success')) > 0)
%>

<div class="content">
  <div class="signup grid">
    <div class="row">
      <div class="column-6 offset-3 column-v-8 offset-v-1 column-l-16">
        <form id="signup" class="form${' error' if is_failure is not None else ''}" action="${req.route_path('signup')}" method="post">
          ${form.csrf_token}
          <h2 class="header">Create your user account</h2>

          ${render_notice()}

        % if is_success:
          <div class="note">
            <p>We sent an instruction email to you.
               Please check your inbox for the account activation!</p>
             After that, go to <a class="link" href="${req.route_url('login')}">Log in</a>
          </div>
        % else:
          <div class="required field-16${' error' if form.email.errors else ''}">
            <label class="label" for="email">${__(form.email.label.text)}</label>
            <p class="description">${_('signup.email.description')}</p>

            <div class="field-13 field-n-16">
              ${form.email(class_='', placeholder=_('signup.email.placeholder'))}
              ${render_error_message(form.email)}
            </div>
          </div>

          <div class="field-16${' error' if form.name.errors else ''}">
            <label class="label" for="name">${__(form.name.label.text)}</label>
            <p class="description">${_('signup.name.description')}</p>

            <div class="field-11 field-n-13">
              ${form.name(class_='', placeholder=_('signup.name.placeholder'))}
              ${render_error_message(form.name)}
            </div>
          </div>

          <div class="field-16${' error' if form.username.errors else ''}">
            <label class="label" for="username">${__(form.username.label.text)}</label>
            <p class="description">${_('signup.username.description')}</p>

            <div class="field-8 field-n-11">
              ${form.username(class_='', placeholder=_('signup.username.placeholder'))}
              ${render_error_message(form.username)}
            </div>
          </div>

          <div class="required field-16${' error' if form.password.errors else ''}">
            <label class="label" for="password">${__(form.password.label.text)}</label>
            <p class="description">${_('signup.password.description', mapping={
              'letters': '<code>{}</code>'.format(_('misc.letters')),
              'numbers': '<code>{}</code>'.format(_('misc.numbers'))
            })|n,trim,clean(tags=['code'])}</p>

            <div class="field-8 field-n-11">
              ${form.password(class_='', placeholder=_('signup.password.placeholder'))}
              ${render_error_message(form.password)}
            </div>
          </div>

          <div class="field-16">
            <div class="petit info message">
              <p class="content">${_('signup.agreement', mapping={
                'button': __(form.submit.label.text),
                'tos': '<a href="{}" target="_blank">{}</a>'.format('https://doc.scrolliris.com/terms.html', _('link.text.tos')),
                'pp': '<a href="{}" target="_blank">{}</a>'.format('https://doc.scrolliris.com/policy.html', _('link.text.pp'))})|n,trim,clean(tags=['a'], attributes=['href', 'target'])}</p>
            </div>
          </div>

          <div class="field-13">
            ${form.submit(class_='ui large primary flat button', value=__(form.submit.label.text))}
          </div>
        % endif
        </form>
      </div>

      <div class="mobile hidden column-4 offset-1 column-v-5 offset-v-1 column-l-16">
        <div class="primary box">
          <h6>You&apos;ll love Scrolliris</h6>
          <div class="list">
            <div class="item">
              <div class="content">
                <div class="header">Readability Analysis</div>
                <div class="description">You can know which part of your text is read eagerly by readers</div>
              </div>
            </div>
            <div class="item">
              <div class="content">
                <div class="header">Publishing your scroll</div>
                <div class="description">Create owned scroll in minutes, publish your articles to the world.</div>
              </div>
            </div>
          </div>
          <p class="text">Scrolliris is currentyl public <code>BETA</code></p>
        </div>

        <p class="text">
          Already have an account?
          <a class="link" href="${req.route_url('login')}">Log in</a>
        </p>
      </div>
    </div>
  </div>
</div>
