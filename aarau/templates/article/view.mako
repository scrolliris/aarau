<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout-plain.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="article content">
  <div class="site grid">

    <div class="row">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="center">
        ${render_notice()}
      </div>
    </div>

    <div class="content row">
      ## TODO
      <%
        def author_names(contributions):
            for c in contributions:
                a = c.user
                yield '<span title="{}">{}</span>'.format(c.role, a.username)
      %>
      <div class="offset-2 column-10 offset-v-2 column-v-12 column-l-16" align="left">
        <article>
          <h1>${article.title}</h1>
          <div class="extra_info">
            <p class="url">${req.route_url('article', namespace=site.project.namespace, slug=site.slug, path=article.path)}</p>
            <p class="authors">${',&nbsp;'.join(author_names(article.contributions))|n,trim}</p>
            <p class="classification">${publication.classification.name}</p>
            <p class="published_at">${article.published_at}</a>
            <p class="badge">
              <a href="https://about.scrolliris.com/"><img src="https://img.scrolliris.com/badge/tracking/on.svg" alt="tracking status"></a>
            </p>
          </div>
          <p class="outline">OUTLINE/ABSTRACT</p>
          <div id="content" class="body">
            ARTICLE BODY
          </div>
          <div class="meta">
            <p class="license" title="${article.license.fullname}"><span class="rounded primary label">${article.license.identifier}</span></p>
            <p class="copyright">&copy;&nbsp;${article.copyright}</p>
          </div>
        </article>
      </div>
    </div>

  </div>
</div>

<%block name='script'>
  ## TODO
  ## <script>
  ## // script - tracker (measure)
  ## (function(d, w) {
  ##   var config = {
  ##         projectId: '${site.project.access_key_id}'
  ##       , apiKey: '${site.write_key}'
  ##       }
  ##     , settings = {
  ##         endpointURL: 'https://api.scrolliris.com/v1.0/projects/'+config.projectId+'/events/read'
  ##       }
  ##     , options = {}
  ##     ;
  ##     var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://lib.scrolliris.com/script/v1.0/projects/'+c.projectId+'/measure.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityTracker,t=(new r.Client(c,settings));t.ready(['body'],function(){t.record(options);});}catch(_){}};s.parentNode.insertBefore(k,s);
  ## }(document, window));
  ## 
  ## // widget - reflector (heatmap:overlay)
  ## (function(d, w) {
  ##   var config = {
  ##         projectId: '${site.project.access_key_id}'
  ##       , apiKey: '${site.read_key}'
  ##       }
  ##     , settings = {
  ##         endpointURL: 'https://api.scrolliris.com/v1.0/projects/'+config.projectId+'/results/read?api_key='+config.apiKey
  ##       }
  ##     , options = {
  ##         widget: {
  ##           extension: 'overlay'
  ##         , initialState: 'inactive'
  ##         }
  ##       }
  ##     ;
  ##     var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://lib.scrolliris.com/widget/v1.0/projects/'+c.projectId+'/heatmap.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityReflector,t=(new r.Widget(c,{settings:settings,options:options}));t.render();}catch(_){}};s.parentNode.insertBefore(k,s);
  ## })(document, window);
  ## </script>
</%block>
