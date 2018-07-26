<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout-basic.mako'/>

<%block name='title'>${render_title('Log in')}</%block>

<div class="content">
  <div class="login grid">
    <div class="row">
      <div class="column-6 offset-5 column-v-8 offset-v-4 column-l-10 offset-l-3 column-m-16">
        <div class="embeded box">
          <div class="header">
            <a href="${req.route_url('top', subdomain=None)}"><img class="logo" width="32" height="32" src="${util.static_url('img/scrolliris-logo-64x64.png')}"></a>
          </div>

          <form id="login" class="form${' error' if err_msg  else ' success' if suc_msg else ''}" action="${req.route_url('login')}" method="post">
            <h4 class="header">Log in to Scrolliris</h4>
            ${render_notice()}
            <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
            <input type="hidden" name="next_path" value="${next_path}">

            <div class="field">
              <label class="label" for="emai">Email</label>
              <input type="text" id="email" name="email" value="${email}" title="Email address" placeholder="Email address" autocomplete="email">
            </div>

            <div class="field">
              <label class="label" for="password">Password</label>
              <input type="password" id="password" name="password" title="Secret password" placeholder="Secret password" autocomplete="off">
            </div>
            <button class="primary flat button" type="submit" name="submit" value="1">Log in</button>
          </form>
          <p><a href="${req.route_url('reset_password.request')}">Fogot your password?</a>&nbsp;or new to Scrolliris?&nbsp;<a class="link" href="${req.route_url('signup')}">Sign up</a></p>
        </div>
      </div>
    </div>
  </div>
</div>
