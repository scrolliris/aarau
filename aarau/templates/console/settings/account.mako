<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Settings - Account')}</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/_sidebar.mako'/>
</%block>

<div class="content">
  <div id="settings">
    <div class="grid">
      <div class="row">
        <div class="column-16">
          ${render_notice()}
        </div>
      </div>

      <div class="row">
        <div class="column-16">
          <div class="attached header"><h5>Account</h5></div>

          <div class="attached box">
            <form class="form">
              <div class="row">
                <div class="field-8 field-v-12 field-l-16">
                  <label class="label" for="language">Language</label>
                  <select id="language">
                    <option value="0">English</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="field-8 field-v-12 field-l-16">
                  <label for="username" class="label">Username (optional)</label>
                  <input type="text" id="username" name="username" placeholder="e.g. scrolliris">
                </div>
              </div>
              <button class="primary disabled flat button">Change</button>
            </form>
          </div>

          <div class="attached header"><h5>Deactivation</h5></div>
          <div class="attached box">
            <form class="form">
              <div class="field">
                <p>Once you delete your account, there is no going back. Please be certain.</p>
              </div>
              <button class="negative disabled flat button">Delete your account</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
