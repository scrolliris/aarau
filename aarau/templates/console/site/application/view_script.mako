<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Site | Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="item active">${application.name}</span>
</div>
</%block>

<%block name='footer'>
</%block>

<div id ="project" class="content">
  ${render_notice()}
  <div class="grid">

    <div class="row">
      <div class="column-16">
        <h3>${application.name}</h3>
        <label class="primary label">${site.domain}</label>
      </div>
    </div>

    <div class="row">

      <div class="column-16">
        <div class="tab menu">
          <a class="item" href="${req.route_path('console.site.application.view.result', project_id=project.id, id=site.id, _query={'type': 'application'})}">Results</a>
          <a class="active item">Scripts</a>
          <a class="item" href="${req.route_path('console.site.application.view.badge', project_id=project.id, id=site.id, _query={'type': 'application'})}">Badges</a>
        </div>
      </div>

      <div class="column-16">
      % if replication_state:
        <label class="positive line label">ready</label>
      % else:
        <label class="negative line label">preparing...</label>
      % endif

        <div class="flat box">
          <div class="row">
            <div class="column-8 column-v-16">
              <h6>Project ID</h6>
              <p class="text">This is unique key for the project. All sites in your project use same value.</p>
            </div>
            <div class="column-8 column-v-16">
              <br>
              <pre>PROJECT_ID: ${project.access_key_id}</pre>
            </div>
          </div>

          <div class="row">
            <div class="column-8 column-v-16">
              <h6>API KEYs</h6>
              <p class="text">These keys are needed to put/fetch data via our API.</p>
            </div>
            <div class="column-8 column-v-16">
              <br>
              <p><label class="negative label">WRITE_KEY</label><code>${site.write_key}</code></p>
              <p><label class="positive label">READ_KEY</label><code>${site.read_key}</code></p>
            </div>
          </div>
        </div>

        <div class="primary flat box">

          <div class="row">
            <div class="column-16">
              <h5>Readability Analysis Tracker</h5>
              <p class="description">Set <code>PROJECT_ID</code> and configure <label class="negative label">WRITE_KEY</label> as `apiKey` with yours. You can just paste this snippet at the bottom of body of your article. The script will work based on user&apos;s scroll. At least, you need to include this for readability analysis of your texts.</p>
              <p class="description">The source code is available from also <a href="https://gitlab.com/lupine-software/siret" target="_blank">our repository</a>. (codename: siret)</p>
              <pre class="inverted">(function(d, w) {
  var config = {
      projectId: '${project.access_key_id}'
    , apiKey: '${site.write_key}'
    }
  , settings = {
      endpointURL: 'https://api.scrolliris.io/v1.0/projects/'+config.projectId+'/events/read'
    }
  , options = {}
  ;
  var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://script.scrolliris.io/projects/'+c.projectId+'/tracker.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityTracker,t=(new r.Client(c,settings));t.ready(['body'],function(){t.record(options);});}catch(_){}};s.parentNode.insertBefore(k,s);
})(document, window);</pre>
            </div>
          </div>

          <div class="row">
            <div class="column-16">
              <h5>Readability Analysis Reflector</h5>
              <p class="description">Set <code>PROJECT_ID</code> and configure <label class="positive label">READ_KEY</label> as `apiKey` with yours. You can just paste this snippet at the bottom of body of your article. A small browser viewer widget will appear on your site. If you don't share the result as public, it's recommended to include it for your admin user.</p>
              <p class="description">The source code is available from also <a href="https://gitlab.com/lupine-software/sihl" target="_blank">our repository</a>. (codename: sihl)</p>
              <pre class="inverted">(function(d, w) {
  var config = {
      projectId: '${project.access_key_id}'
    , apiKey: '${site.read_key}'
    }
  , settings = {
      endpointURL: 'https://api.scrolliris.io/v1.0/projects/'+config.projectId+'/results/read?api_key='+config.apiKey
    }
  , options = {}
  ;
  var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://widget.scrolliris.io/projects/'+c.projectId+'/reflector.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityReflector,t=(new r.Widget(c,{settings:settings,options:options}));t.render();}catch(_){}};s.parentNode.insertBefore(k,s);
})(document, window);</pre>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</div>
