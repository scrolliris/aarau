<%inherit file='_layout.mako'/>

<%block name='title'>
  Scrolliris
</%block>

<div class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16" align="center">
        <%namespace name='msg' file='./shared/_message.mako'/>
        ${msg.form()}
        <div class="banner">
          <h1 class="header">Beyond the Scroll</h1>
          <p>Extend your publication readability beyond the scroll with Scrolliris</p>
        % if req.user and req.user.projects:
          <a class="flat button" href="${req.route_url('console.top')}">Go to Console</a>
        % else:
          <a class="primary button" href="${req.route_url('project.new', namespace=None)}">Create a Project</a>
        % endif
        </div>
        <div id="ticker" class="pride"></div>
      </div>
    </div>

    <div class="row">
      <div class="column-3 offset-3 column-v-8 column-l-16" align="center">
        <div class="box">
          <div class="header"><h3>How it works</h3></div>
          <div class="description">
            <p>Learn how our readability analysis works.</p>
            <a class="flat button" href="https://doc.scrolliris.com/how_it_works/overview.html" target="_blank">Read the Doc</a>
          </div>
        </div>
      </div>
      <div class="column-4 column-v-8 column-l-16" align="center">
        <div class="box">
          <div class="header"><h3>Demo</h3></div>
          <div class="description">
            <p>Check our concept draft document on online. It works as demo.</p>
            <a class="flat primary button" href="https://try.scrolliris.com" target="_blank">Try Demo</a>
          </div>
        </div>
      </div>
      <div class="column-3 column-v-8 offset-v-4 column-l-16" align="center">
        <div class="box">
          <div class="header"><h3>Release Note</h3></div>
          <div class="description">
            <p>Scrolliris is currently under the development as public BETA.</p>
            <a class="flat disabled button" href="">Check the Note</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
