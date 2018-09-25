<%def name="render_title(title, separator='-')">
  <%
    if isinstance(title, list):
      title = ' {} '.format(separator).join(title)
  %>
  % if len(title) > 0:
    ${title} ${separator} Scrolliris
  % else:
    Scrolliris
  % endif
</%def>
