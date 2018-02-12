<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/carrell/_layout.mako'/>

<%block name='title'>${render_title('Reader')}</%block>

<div class="site content">
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
      <div class="offset-3 column-10 offset-v-2 column-v-12 column-l-16" align="left">
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
