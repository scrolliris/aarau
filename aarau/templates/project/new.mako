<%inherit file='../_layout.mako'/>

<%block name='title'>
  New Project | Scrolliris
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-6 offset-2 column-v-10 column-l-16">
        <%namespace name='msg' file='../shared/_message.mako'/>
        ${msg.form()}
        <%
          act = req.route_path('project.new')
          ctx = 'new'
          # FIXME
          err = ''
          obj = None
        %>
        <%include file="_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>

      <div class="column-4 offset-1 column-v-6 column-l-16">
        <div class="primary message">
          <h5 class="header">Thank you.</h5>
          <p class="description">Scrolliris is currently beta. We are now working on the enhancement, but some features are still missing. If you need something, please feedback to us, anytime!</p>
        </div>
        <div class="flat box">
          <strong>NOTE</strong>
          <ul class="list">
            <li class="item">Server is only in west-europe for now. If you are not it there, the network connectivity is a little bad... We're preparing more endpoints for other regions. (like australia, us, and east-asia)</li>
            <li class="item">You can create only one project for now.</li>
            <li class="item">The publication on Scrolliris is under development. You can integrate our scripts in your existing external application such as blog.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
