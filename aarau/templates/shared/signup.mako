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
        <form id="signup" class="form${' error' if err_msg is not None else ''}" action="${req.route_url('signup')}" method="post">
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
            <label class="label" for="email">Email address</label>
            <p class="description">You need this to log in to your account.</p>

            ${form.email(class_='', placeholder='william.shakespeare@scrolliris.com')}
            ${render_errors(form.email)|n}
          </div>

          <div class="field-11${' error' if form.name.errors else ''}">
            <label class="label" for="name">Name</label>
            <p class="description">This is your fullname.</p>

            ${form.name(class_='', placeholder='William Shakespeare (optional)')}
            ${render_errors(form.name)|n}
          </div>

          <div class="field-8${' error' if form.username.errors else ''}">
            <label class="label" for="username">Username</label>
            <p class="description">This is your personal username.</p>

            ${form.username(class_='', placeholder='william (optional)')}
            ${render_errors(form.username)|n}
          </div>

          <div class="required field-16${' error' if form.password.errors else ''}">
            <label class="label" for="password">Password</label>
            <p class="description">At least, use one lower and one UPPER letter <code>A-z</code>, and one digit from: <code>0-9</code>. 8 characters are minimum length. Make it strong.</p>
            <div class="field-11">
              ${form.password(class_='', placeholder='Keep it secret :)')}
              ${render_errors(form.password)|n}
            </div>
          </div>

          <div class="field-16">
            <div class="petit info message">
              <p class="content">
              By clicking on <code>Create an account</code> below, you are agreeing to the <a href="#">Terms of Service</a> and the <a href="#">Privacy Policy</a>.
              </p>
            </div>
          </div>

          <div class="field-13">
            ${form.submit(class_='ui large primary button')}
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
