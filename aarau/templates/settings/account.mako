<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/_layout.mako'/>

<%block name='title'>${render_title('Settings - Account')}</%block>

<div class="content">
  <div id="settings">
    <div class="grid">

      <div class="row">
        <div class="offset-2 column-3 offset-v-1 column-v-4 column-l-16">
          <%include file='aarau:templates/settings/_menu.mako'/>
        </div>

        <div class="column-8 column-v-10 column-l-16">
          <div class="attached header"><h6>Account</h6></div>
          <div class="attached box">
            <form class="form">
              <div class="row">
                <div class="field-10 field-n-16">
                  <label class="label" for="language">Language</label>
                  <select id="language">
                    <option value="0">English</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="field-10 field-n-16">
                  <label for="username" class="label">Username (optional)</label>
                  <input type="text" id="username" name="username" placeholder="e.g. scrolliris">
                </div>
              </div>
              <button class="primary disabled button">Change</button>
            </form>
          </div>

          <div class="attached header"><h6>Deactivation</h6></div>
          <div class="attached box">
            <form class="form">
              <div class="field">
                <p>Once you delete your account, there is no going back. Please be certain.</p>
              </div>
              <button class="negative disabled button">Delete your account</button>
            </form>
          </div>
        </div>

      </div>

    </div>
  </div>
</div>
