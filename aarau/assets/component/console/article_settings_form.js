import { linkEvent, Component } from 'inferno.js';
import { h } from 'inferno-hyperscript.js';

import { i18n } from '../../js/console/i18n.js';

import './article_settings_form.styl';


function handleOnInput(instance, event) {
  const name = event.target.name;
  const value = event.target.value;

  let newState = {};
  newState[name] = {};

  // value
  newState[name]['value'] = value;

  // length check
  let errors = instance.state[name].errors.slice();
  if (instance.props['validations'].hasOwnProperty(name)) {
    let v = instance.props['validations'][name];
    let minLengthError = i18n.t(
      'validation.error.min_length', {min: v.minLength});
    if (value.length < v.minLength) {
      errors.push(minLengthError);
    } else {
      errors = errors.filter((v) => {
        return v !== minLengthError;
      });
    }
    let maxLengthError = i18n.t(
      'validation.error.max_length', {max: v.maxLength});
    if (value.length > v.maxLength) {
      errors.push(maxLengthError);
    } else {
      errors = errors.filter((v) => {
        return v !== maxLengthError
      });
    }
  }
  newState[name]['errors'] = errors.filter((v, i, self) => {
    return self.indexOf(v) === i;
  });

  instance.setState(newState);
}

function handleOnChange(instance, event) {
  const name = event.target.name;
  const value = event.target.checked;

  let newState = {};
  newState[name] = {'value': value};
  instance.setState(newState);
}

function handleOnSubmit(instance, event) {
  instance.setState({message: i18n.t('message.sending')});

  if (event !== null) {
    event.preventDefault();
  }

  let data = {
    csrf_token: instance.state.csrfToken.value
  , context: 'settings'
  , code: instance.state.code.value
  , path: instance.state.path.value
  , scope: instance.state.scope.value
  , title: instance.state.title.value
  };
  console.log(data);

  let client = new XMLHttpRequest();
  client.onreadystatechange = () => {
    if (client.readyState === 4) { // DONE
      let res = JSON.parse(client.responseText);
      let newState = {message: res.message};

      let errors = res.errors;
      if (client.status === 200 && res.status === 'ok') {
        if (Object.keys(errors).length === 0) { // created/updated
          newState['code'] = {errors: [], value: res.code};
          // update editor form
          const form = document.getElementById('article_editor_form');
          let code = form.querySelector('#editor_form_code');
          if (code.value === null || code.value === "") {
            code.value = res.code;
            // notify
            if (code.onchange && typeof code.onchange === 'function') {
              code.onchange();
            }
          }
        } else { // validation error
          for (let f in errors) {
            if (errors.hasOwnProperty(f)) {
              newState[f] = {
                errors: errors[f]
              , value: instance.state[f].value
              };
            }
          }
        }
      }
      instance.setState(newState);
    }
  };
  client.open('POST', instance.props.action || '', true);
  client.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  client.send(buildQueryString(data));
  return false;
}

function handleOnFocusOut(instance, event) {
  event.stopImmediatePropagation();
  event.preventDefault();

  const name = event.target.name;
  if (instance.state.hasOwnProperty(name)) {
    const form = document.getElementById('article_settings_form');

    // TODO: save in local
  }
}

// called via update by editor form
function notifyCodeOnChange(instance) {
  const form = document.getElementById('article_settings_form');
  let code = form.querySelector('#settings_form_code');

  instance.state.code.value = code.value;
}

/**
 * Builds error message elements.
 *
 * @return {Array} error messages.
 */
function buildErrorMessage(prop) {
  let elements = [];
  const errors = prop.errors;
  if (Array.isArray(errors) && errors.length) {
    for (let i in errors) {
      if (Object.prototype.hasOwnProperty.call(errors, i)) {
        elements.push(h('p.error.text', null, errors[i]));
      }
    }
  }
  return elements;
}

/**
 *
 *
 * @return String query string
 */
function buildQueryString(data) {
  let params = [];
  for (let d in data) {
    if (data.hasOwnProperty(d)) {
      params.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    }
  }
  return params.join('&');
}

class ArticleSettingsForm extends Component {
  constructor(props) {
    super(props);

    this.props['action'] = '/api/' + this.props.namespace + '/' +
      this.props.slug + '/article/settings.json';

    this.props['validations'] = {
      path: {
        minLength: 6
      , maxLength: 64
      }
    , title: {
        minLength: 0
      , maxLength: 128
      }
    };

    this.state = {
      message: '' // progress message
    , csrfToken: {
        errors: []
      , value: props.csrfToken
      }
    , code: {
        errors: []
      , value: props.code
      }
    , path: {
        errors: []
      , value: props.path || props.code
      }
    , scope: {
        errors: []
      , value: props.scope === 'public'
      }
    , title: {
        errors: []
      , value: props.title
      }
    };
  }

  render() {
    return h('form#article_settings_form.form', {
      action: this.props.action || ''
    , method: 'POST'
    , onSubmit: linkEvent(this, handleOnSubmit)
    }, [
      h('input', {
        type: 'hidden', name: 'csrf_token', value: this.state.csrfToken.value})
    , h('input#settings_form_code', {
        type: 'hidden'
      , name: 'code'
      , value: this.state.code.value
      , onChange: linkEvent(this, notifyCodeOnChange)
      })
    , h('input', {type: 'hidden', name: 'context', value: 'settings'})
    , h('.row', [
        h('.field-16', [
          h('label.label', {for: 'path'}, i18n.t('article.path.label'))
        , h('p.description', {dangerouslySetInnerHTML: {
            __html: i18n.t('article.path.description', {
              code0: '<code>a-z0-9</code>'
            , code1: '<code>-</code>'
            , length: '6-64'
            })
          }})
        , h('input', {
            type: 'text'
          , name: 'path'
          , value: this.state.path.value
          , placeholder: 'chapter-001'
          , autocomplete: 'off'
          , onInput: linkEvent(this, handleOnInput)
          , onFocusOut: linkEvent(this, handleOnFocusOut)
          })
        , buildErrorMessage(this.state.path)
        ])
      ])
    , h('.row', [
        h('.field-16', [
          h('label.label', {for: 'title'}, i18n.t('article.title.label'))
        , h('p.description', {dangerouslySetInnerHTML: {
            __html: i18n.t('article.title.description', {
              length: '3-128'
            })
          }})
        , h('input', {
            type: 'text'
          , name: 'title'
          , value: this.state.title.value
          , placeholder: 'Title'
          , autocomplete: 'off'
          , onInput: linkEvent(this, handleOnInput)
          , onFocusOut: linkEvent(this, handleOnFocusOut)
          })
        , buildErrorMessage(this.state.title)
        ])
      ])
    , h('.row', [
        h('.field-16', [
          h('label.label', {for: 'scope'}, 'Scope')
        , h('span.description', 'Public Access')
        , h('.checkbox.right', [
            h('span.value', this.state.scope.value ? 'On' : 'Off')
          , h('input#scope', {
              type: 'checkbox'
            , name: 'scope'
            , defaultChecked: this.state.scope.value
            , onChange: linkEvent(this, handleOnChange)
            })
          , h('label.label.scope', {for: 'scope'}, '')
          ])
        ])
      ])
    , h('.row', [
        h('.field-16', [
          h('button.flat.button', 'Save')
        , h('span.message', this.state.message)
        ])
      ])
    ]);
  }
}

module.exports = ArticleSettingsForm;
