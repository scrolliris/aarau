<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('New Project')}</%block>

<%
  is_failure = (len(req.session.peek_flash('failure')) > 0)
%>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-5 offset-3 column-v-10 column-l-16">
        ${render_notice()}

        <%
          act = req.route_path('project.new')
          ctx = 'new'
          err = is_failure
          obj = None
        %>
        <%include file="aarau:templates/project/_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>

      <div class="column-4 offset-1 column-v-6 column-l-16">
        <div class="primary message">
          <h5 class="header">Thank you.</h5>
          <p class="description">Scrolliris is currently beta. We are now working on the enhancement, but some features are still missing. If you need something, please feedback to us, anytime!</p>
        </div>
        <div class="flat box">
          <strong>NOTE</strong>
          <ul class="list">
            <li class="item">"Project" is your workspace for writing. You can create publications under the project.</li>
            <li class="item">Our main application server is located in west-europe for now. If you are not it there, the network connectivity is a little bad... We&apos;re preparing more endpoints for other regions. (like australia, us, and east-asia)</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
