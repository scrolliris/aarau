<%namespace file='aarau:templates/macro/_error_message.mako' import='render_error_message'/>

<%page args="f, act, ctx, err, obj"/>

<form id="${ctx}_application_site" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}
  <h4 class="header">${ctx.upper()}</h4>
  <p><span class="secondary line label">${obj.hosting_type}</span></p>

  <div class="row">
    <div class="required field-5${' error' if f.domain.errors else ''}">
      <label class="label" for="domain">Domain</label>
      ${f.domain(class_='', placeholder='e.g. example.org')}
      ${render_error_message(f.domain)}
    </div>
  </div>

  <div class="row">
    <% _f = f.application.form %>
    <div class="required field-5${' error' if _f.name.errors else ''}">
      <label class="label" for="application-name">Name</label>
      ${_f.name(class_='', placeholder='e.g. My Science Notes')}
      ${render_error_message(_f.name)}
    </div>
  </div>

  <div class="row">
    <div class="optional field-10${' error' if _f.description.errors else ''}">
      <label class="label" for="application-description">Description</label>
      ${_f.description(class_='', rows=1, cols=30, placeholder='Science notes from my daily thoughts.')}
      ${render_error_message(_f.description)}
    </div>
  </div>

  ${f.submit(class_='primary button')}
</form>
