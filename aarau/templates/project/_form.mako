<%page args="f, act, ctx, err, obj"/>

<%
  def render_errors(field):
      return ''.join(['<p class="error text">{}</p>'.format(e) for e in field.errors])
%>

<form id="${ctx}_project" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}
  <h4 class="header">${ctx.upper()}</h4>

  <div class="row">
    <div class="required field-9${' error' if f.name.errors else ''}">
      <label class="label" for="name">Name</label>
      ${f.name(class_='', placeholder='My Project')}
      ${render_errors(f.name)|n}
    </div>
  </div>

  <div class="row">
    <div class="required field-7${' error' if f.namespace.errors else ''}">
      <label class="label" for="namespace">Namespace</label>
      <p class="description">It must be unique in our system.</p>
      ${f.namespace(class_='', placeholder='sample-project')}
      ${render_errors(f.namespace)|n}
    </div>
  </div>

  <div class="row">
    <div class="field-16${' error' if f.description.errors else ''}">
      <label class="label" for="description">Description</label>
      ${f.description(class_='', rows=2, cols=50, placeholder='A note for collaborators...')}
      ${render_errors(f.description)|n}
    </div>
  </div>

  ${f.submit(class_='primary button')}
</form>
