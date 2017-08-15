<%page args="f, act, ctx, err"/>

<%
  def render_errors(field):
      return ''.join(['<p class="error text">{}</p>'.format(e) for e in field.errors])
%>

<form id="${ctx}_application_site" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}

  <div class="header"><h6>Site</h6></div>
  <div class="row">
    <div class="required field-5${' error' if f.domain.errors else ''}">
      <label class="label" for="domain">Domain</label>
      ${f.domain(class_='', placeholder='e.g. example.org')}
      ${render_errors(f.domain)|n}
    </div>
  </div>

  <div class="row">
    <div class="field-12">
      <div class="header"><h6>Application</h6></div>
    </div>
  </div>

  <div class="row">
    <% _f = f.application.form %>
    <div class="required field-5${' error' if _f.name.errors else ''}">
      <label class="label" for="application-name">Name</label>
      ${_f.name(class_='', placeholder='e.g. My Science Notes')}
      ${render_errors(_f.name)|n}
    </div>
  </div>

  <div class="row">
    <div class="optional field-10${' error' if _f.description.errors else ''}">
      <label class="label" for="application-description">Description</label>
      ${_f.description(class_='', rows=1, cols=30, placeholder='Science notes from my daily thoughts.')}
      ${render_errors(_f.description)|n}
    </div>
  </div>

  ${f.submit(class_='primary button')}
</form>
