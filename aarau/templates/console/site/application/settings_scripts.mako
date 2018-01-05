<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Site | Project')}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_path('console.site.application.overview', project_id=project.id, id=site.id, _query={'type': 'application'})}">${application.name}</a>
  <span class="divider">/</span>
  <span class="item active">Measure Scripts</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/application/_sidebar_settings.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id ="project" class="content">
  ${render_notice()}
  <div class="grid">

    <div class="row">
      <div class="column-16">
        <h4>${application.name}</h4>
        <label class="primary rounded label">${site.domain}</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="attached header">
          <h5>Readability Measure Scripts</h5>
        </div>

        <div class="attached box">
          <div class="row">
            <div class="column-16">
              <p class="description">Set <code>PROJECT_ID</code> and configure <label class="negative label">WRITE_KEY</label> as `apiKey` with yours. You can just paste this snippet at the bottom of body of your article. The script will work based on user&apos;s scroll. At least, you need to include this for readability analysis of your texts.</p>
              <p class="description">The source code is available from also <a href="https://gitlab.com/scrolliris/staefa" target="_blank">our repository</a>. (codename: Stäfa)</p>

              <h6>Position</h6>
              <pre class="inverted">(function(d, w) {
  var config = {
      projectId: '${project.access_key_id}'
    , apiKey: '${site.write_key}'
    }
  , settings = {
      endpointURL: 'https://api.scrolliris.com/v1.0/projects/'+config.projectId+'/events/read'
    }
  , options = {}
  ;
  var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://lib.scrolliris.com/script/v1.0/projects/'+c.projectId+'/measure.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityTracker,t=(new r.Client(c,settings));t.ready(['body'],function(){t.record(options);});}catch(_){}};s.parentNode.insertBefore(k,s);
})(document, window);</pre>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
