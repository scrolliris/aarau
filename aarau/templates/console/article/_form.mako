<%namespace file='aarau:templates/macro/_error_message.mako' import='render_error_message'/>

<%page args="f, act, ctx, err, obj"/>

<form id="${ctx}_article" class="form${' error' if err is not None else ''}" action="${act}" method="post">
  ${f.csrf_token}

  <div class="row">
    <div class="required field-16${' error' if f.title.errors else ''}">
      <label class="label" for="title">Title</label>
      <p class="description">It must be 3-128 characters long.</p>
      ${f.title(class_='', placeholder='Awesome article title')}
      ${render_error_message(f.title)}
    </div>
  </div>

  <div class="row">
    % if ctx == 'new':
    <div class="required field-16${' error' if f.path.errors else ''}">
      <label class="label" for="path">Path</label>
      <p class="description">It must be unique in your publication.
        You can use <code>a-z0-9</code> and <code>-</code> in 6-32 characters length.</p>
      ${f.path(class_='', placeholder='article-001')}
      ${render_error_message(f.path)}
    </div>
    % endif
  </div>

  ${f.submit(class_='primary flat button')}
</form>
