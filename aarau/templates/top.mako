<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="content">
  <div class="grid">
    <div class="row landscape">
      <div class="column-16" align="center">
        ${render_notice()}

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
          <div class="header"><h3>Our Updates</h3></div>
          <div class="description">
            <p>Scrolliris is currently under the development as public BETA.</p>
            <a class="flat secondary button" href="https://log.scrolliris.com/" target="_blank">Check the Log</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
