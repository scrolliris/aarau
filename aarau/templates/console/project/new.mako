<%inherit file='../_layout.mako'/>

<%block name='title'>
  New Project | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <span class="active item">New</span>
</div>
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-8">
        <%namespace name='msg' file='../../shared/_message.mako'/>
        ${msg.form()}
        <%
          act = req.route_path('console.project.new')
          ctx = 'new'
          # FIXME
          err = ''
          obj = None
        %>
        <%include file="_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
