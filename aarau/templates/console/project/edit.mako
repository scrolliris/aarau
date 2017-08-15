<%inherit file='../_layout.mako'/>

<%block name='title'>
  Edit Project | Scrolliris
</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <a class="item" href="${req.route_path('console.top')}">Projects</a>
  <span class="divider">/</span>
  <a class="item" href="${req.route_url('console.project.view', id=project.id)}">${project.name}</a>
  <span class="divider">/</span>
  <span class="active item">Edit</span>
</div>
</%block>

<div id="project" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-8">
        <%namespace name='msg' file='../../shared/_message.mako'/>
        ${msg.form()}
        <%
          act = req.route_path('console.project.edit', id=project.id)
          ctx = 'edit'
          # FIXME
          err = ''
          obj = project
        %>
        <%include file="_form.mako" args="f=form, act=act, ctx=ctx, err=err, obj=obj"/>
      </div>
    </div>
  </div>
</div>
