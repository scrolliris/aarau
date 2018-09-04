<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout-plain.mako'/>

<%block name='title'>${render_title('')}</%block>

<div class="site content">
  <div class="site grid">

    <div class="row">
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="center">
        ${render_notice()}
      </div>
    </div>

    <div class="content row">
      <div class="offset-2 column-12 offset-v-2 column-v-12 column-l-16" align="center">
        <h1>${publication.name}</h1>
        <p>${publication.description}</p>

        <div>
          <span class="flat rounded primary label">${site.project.name}</span>
          ## TODO
          <% members_count = len(site.project.memberships) %>
          % if members_count == 1:
            <p>${members_count} member</p>
          % else:
            <p>${members_count} members</p>
          % endif
        </div>

        <span class="license">${publication.license.fullname}</span>
        <p class="copyright">&copy;&nbsp;${publication.copyright}</p>

        <hr>
        <section>
          % for article in articles:
            <article>
              <h5>
                <a href="${req.route_url('article', namespace=site.project.namespace, slug=site.slug, path=article.path)}">${article.title}</a>
              </h5>
            </article>
          % endfor
        </section>
      </div>
    </div>

  </div>
</div>
