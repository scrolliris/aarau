<%namespace file='aarau:templates/macro/_error_message.mako' import='render_error_message'/>

<%page args="f, act, ctx, err, obj"/>

<form id="${ctx}_publication_site" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}
  <h4 class="header">${ctx.upper()}</h4>
  <p><span class="primary rounded label">${obj.instance_type}</span></p>

  <div class="row">
    <div class="field-8">
      <label class="label" for="domain">Domain</label>
      <p class="description">Custom domain or subdomain support is still TBD.</p>
      <span class="secondary line label">scrolliris.com</span>
    </div>
  </div>

  <div class="row">
    <div class="required field-16${' error' if f.slug.errors else ''}">
      <label class="label" for="slug">Slug</label>
      <p class="description">
        This is a short name. You can use <em>A-z0-9</em> and <em>-</em>. It must be <strong>6-32</strong> characters length.<br>
        It will be a part of url for your publication, like: <code>https://scrolliris.com/&lt;namespace&gt;/&lt;slug&gt;</code></p>

      ${f.slug(class_='control', placeholder='e.g. example-pub-name')}
      ${render_error_message(f.slug)}
    </div>
  </div>

  <% _f = f.publication.form %>

  <div class="row">
    <div class="required field-12${' error' if _f.classification.errors else ''}">
      <label class="label" for="publication-classification">Classification</label>
      ${_f.classification(class_='control')}
      ${render_error_message(_f.classification)}
    </div>
  </div>

  <div class="row">
    <div class="required field-8${' error' if _f.name.errors else ''}">
      <label class="label" for="publication-name">Name</label>
      <span class="description">Name must be 3-64 characters length.</span>
      ${_f.name(class_='control', placeholder='e.g. My Science Notes')}
      ${render_error_message(_f.name)}
    </div>
  </div>

  <div class="row">
    <div class="required field-12${' error' if _f.license.errors else ''}">
      <label class="label" for="publication-license">License</label>
      ${_f.license(class_='control')}
      ${render_error_message(_f.license)}
    </div>
  </div>

  <div class="row">
    <div class="required field-8${' error' if _f.copyright.errors else ''}">
      <label class="label" for="publication-copyright">Copyright</label>
      ${_f.copyright(class_='control', placeholder='e.g. 2017 Albrecht Dürer')}
      ${render_error_message(_f.copyright)}
    </div>
  </div>

  <div class="row">
    <div class="optional field-16${' error' if _f.description.errors else ''}">
      <label class="label" for="publication-description">Description</label>
      <p class="description">Describe the <strong>theme</strong> of your new publication.</p>
      ${_f.description(class_='control', rows=2, placeholder='Science notes from my daily thoughts.')}
      ${render_error_message(_f.description)}
    </div>
  </div>

  ${f.submit(class_='primary button')}
</form>
