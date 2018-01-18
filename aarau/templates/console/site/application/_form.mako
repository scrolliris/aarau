<%namespace file='aarau:templates/macro/_error_message.mako' import='render_error_message'/>

<%page args="f, act, ctx, err, obj"/>

<form id="${ctx}_application_site" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}
  <h4 class="header">${ctx.upper()}</h4>
  <p><span class="secondary rounded label">${obj.instance_type}</span></p>

  <div class="row">
    <div class="required field-8${' error' if f.domain.errors else ''}">
      <label class="label" for="domain">Domain</label>
      ${f.domain(class_='', placeholder='e.g. example.org')}
      ${render_error_message(f.domain)}
    </div>
  </div>

  <div class="row">
    <div class="required field-16${' error' if f.slug.errors else ''}">
      <label class="label" for="slug">Slug</label>
      <p class="description">
        This is a short name. You can use <em>A-z0-9</em> and <em>-</em>. It must be <strong>6-32</strong> characters length.<br>
        It will be a part of url path like: <code>https://scrolliris.com/publications/&lt;slug&gt;</code></p>

      ${f.slug(class_='control', placeholder='e.g. example-pub-name')}
      ${render_error_message(f.slug)}
    </div>
  </div>

  <% _f = f.application.form %>

  <div class="row">
    <div class="required field-8${' error' if _f.name.errors else ''}">
      <label class="label" for="application-name">Name</label>
      ${_f.name(class_='', placeholder='e.g. My Science Notes')}
      ${render_error_message(_f.name)}
    </div>
  </div>

  <div class="row">
    <div class="optional field-16${' error' if _f.description.errors else ''}">
      <label class="label" for="application-description">Description</label>
      ${_f.description(class_='', rows=1, cols=30, placeholder='Science notes from my daily thoughts.')}
      ${render_error_message(_f.description)}
    </div>
  </div>

  ${f.submit(class_='primary button')}
</form>
