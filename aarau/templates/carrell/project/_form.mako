<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>

<%page args="f, act, ctx, err, obj"/>

<form id="${ctx}_project" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}
  <div class="row">
    <div class="field-16">
      <h4 class="header">${ctx.upper()} PROJECT</h4>
    </div>
  </div>

  <div class="row">
    <div class="required field-16${' error' if f.name.errors else ''}">
      <label class="label" for="name">Name</label>
      <p class="description">It must be 6-32 characters long.</p>
      ${f.name(class_='', placeholder='My Project')}
      ${render_error_message(f.name)}
    </div>
  </div>

  <div class="row">
    <div class="required field-16${' error' if f.namespace.errors else ''}">
      <label class="label" for="namespace">Namespace</label>
      <p class="description">It must be unique in our system.
        You can use <code>a-z0-9</code> and <code>-</code> in 6-32 characters length. Start with alphabet.</p>
      ${f.namespace(class_='', placeholder='sample-project')}
      ${render_error_message(f.namespace)}
    </div>
  </div>

  <div class="row">
    <div class="field-16${' error' if f.description.errors else ''}">
      <label class="label" for="description">Description</label>
      ${f.description(class_='', rows=2, cols=50, placeholder='A note for subscribers, collaborators and new readers...')}
      ${render_error_message(f.description)}
    </div>
  </div>

  <div class="row">
    <div class="field-16">
      ${f.submit(class_='primary button')}
    </div>
  </div>
</form>
