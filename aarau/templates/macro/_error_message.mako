<%def name="render_error_message(field)">
  <%
    def error_messages(_field):
        return ''.join(['<p class="error text">{}</p>'.format(e) for e in set(_field.errors)])
  %>
  ${error_messages(field)|n,trim,clean(tags=['p'], attributes={'p': ['class']})}
</%def>
