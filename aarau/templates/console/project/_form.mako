<%namespace file='aarau:templates/macro/_error_message.mako' import='render_error_message'/>

<%page args="f, act, ctx, err, obj"/>

<form id="${ctx}_project" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}
  <h4 class="header">${ctx.upper()}</h4>

  <div class="row">
    <div class="required field-12${' error' if f.name.errors else ''}">
      <label class="label" for="name">Name</label>
      <p class="description">It must be 6-32 characters long.</p>
      ${f.name(class_='', placeholder='My Project')}
      ${render_error_message(f.name)}
    </div>
  </div>

  <div class="row">
    <div class="required field-12${' error' if f.namespace.errors else ''}">
      <label class="label" for="namespace">Namespace</label>
      <p class="description">It must be unique in our system.
        You can use <code>a-z0-9</code> and <code>-</code> in 4-16 characters length. Start with alphabet.</p>
      ${f.namespace(class_='', placeholder='my-project')}
      ${render_error_message(f.namespace)}
    </div>
  </div>

  % if ctx == 'edit':
  <div class="row">
    <div class="required field-5${' error' if f.plan.errors else ''}">
      <label class="label" for="plan">Plan</label>
      <select id="plan" name="plan">
      % for p in f.plan:
        <% p.label.text = _(p.label.text) %>
        <% p.checked = True if p.data == str(obj.plan_id) else False %>
        ${p()}
      % endfor
      </select>
      ${render_error_message(f.plan)}
    </div>
  </div>

  % endif
  <div class="row">
    <div class="field-12${' error' if f.description.errors else ''}">
      <label class="label" for="description">Description</label>
      ${f.description(class_='', rows=2, cols=50, placeholder='A note for subscribers, collaborators and new readers...')}
      ${render_error_message(f.description)}
    </div>
  </div>

  ${f.submit(class_='primary flat button')}
</form>
