<%inherit file='../_layout.mako'/>

<%block name='title'>
 Sign up | Scrolliris
</%block>

<%
  err_msg = (req.session.pop_flash('error') or [None])[0]
  suc_msg = (req.session.pop_flash('success') or [None])[0]

  def render_errors(field):
      return ''.join(['<p class="error text">{}</p>'.format(e) for e in field.errors])
%>

<div class="content">
  <div class="signup grid">
    <div class="row">
      <div class="column-6 offset-3 column-v-8 offset-v-1 column-l-16">
        <form id="signup" class="form${' error' if err_msg is not None else ''}" action="${req.route_path('signup')}" method="post">
          ${form.csrf_token}
          <h2 class="header">Create your user account</h2>

        % if err_msg or suc_msg:
          % if err_msg:
            <div class="error message" role="alert">
            <p>${err_msg}</p>
          </div>
          % elif suc_msg:
            <div class="succsess message" role="alert">${suc_msg}</div>
          % endif
        % endif

          <div class="required field-13${' error' if form.email.errors else ''}">
            <label class="label" for="email">${__(form.email.label.text)}</label>
            <p class="description">${_('signup.email.description')}</p>

            ${form.email(class_='', placeholder=_('signup.email.placeholder'))}
            ${render_errors(form.email)|n}
          </div>

          <div class="field-11${' error' if form.name.errors else ''}">
            <label class="label" for="name">${__(form.name.label.text)}</label>
            <p class="description">${_('signup.name.description')}</p>

            ${form.name(class_='', placeholder=_('signup.name.placeholder'))}
            ${render_errors(form.name)|n}
          </div>

          <div class="field-8${' error' if form.username.errors else ''}">
            <label class="label" for="username">${__(form.username.label.text)}</label>
            <p class="description">${_('signup.username.description')}</p>

            ${form.username(class_='', placeholder=_('signup.username.placeholder'))}
            ${render_errors(form.username)|n}
          </div>

          <div class="required field-16${' error' if form.password.errors else ''}">
            <label class="label" for="password">${__(form.password.label.text)}</label>
            <p class="description">${_('signup.password.description', mapping={
              'letters': '<code>{}</code>'.format(_('misc.letters')),
              'numbers': '<code>{}</code>'.format(_('misc.numbers'))
            })|n,trim,clean(tags=['code'])}</p>
            <div class="field-11">
              ${form.password(class_='', placeholder=_('signup.password.placeholder'))}
              ${render_errors(form.password)|n}
            </div>
          </div>

          <div class="field-16">
            <div class="petit info message">
              <p class="content">${_('signup.agreement', mapping={
                'button': __(form.submit.label.text),
                'tos': '<a href="{}">{}</a>'.format('/', _('link.text.tos')),
                'pp': '<a href="{}">{}</a>'.format('/', _('link.text.pp'))})|n,trim,clean(tags=['a'], attributes=['href'])}</p>
            </div>
          </div>

          <div class="field-13">
            ${form.submit(class_='ui large primary button', value=__(form.submit.label.text))}
          </div>
        </form>
      </div>

      <div class="column-4 offset-1 column-v-5 offset-v-1 column-l-16">
        <div class="primary box">
          <h6>You'll love Scrolliris</h6>
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
