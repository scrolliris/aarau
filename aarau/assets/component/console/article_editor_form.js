import {linkEvent, Component} from 'inferno.js';
import {h} from 'inferno-hyperscript.js';
import {Editor, setPlaceholder} from 'vergil.js';

import {i18n} from '../../js/console/i18n.js';


function handleOnInput(instance, event) {
  const name = 'content'
      , value = event.target.innerText
      ;

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

function handleOnSubmit(instance, event) {
  instance.setState({message: i18n.t('message.sending')});

  if (event !== null) {
    event.preventDefault();
  }

  let data = {
    csrf_token: instance.state.csrfToken.value
  , context: 'editor'
  , code: instance.state.code.value
  , content: instance.state.content.value
  };

  let client = new XMLHttpRequest();
  client.onreadystatechange = () => {
    if (client.readyState === 4) { // DONE
      let res = JSON.parse(client.responseText);
      let newState = {message: res.message};

      let errors = res.errors;
      if (client.status === 200 && res.status === 'ok') {
        if (Object.keys(errors).length === 0) { // created/updated
          newState['code'] = {errors: [], value: res.code};
          // update config form
          const form = document.getElementById('article_config_form');
          let code = form.querySelector('#config_form_code');
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

function handleOnFocusIn(instance, event) {
  event.stopImmediatePropagation();
  event.preventDefault();

  const name = 'content';

  if (instance.state.hasOwnProperty(name)) {
    const form = document.getElementById('article_editor_form');

    form.setAttribute('style', 'background-color: #f1f1f1;');
    setTimeout(() => {
      form.setAttribute('style', 'background-color: #ffffff;');
    }, 900);
  }
}

function handleOnFocusOut(instance, event) {
  event.stopImmediatePropagation();
  event.preventDefault();

  const name = 'content';

  if (instance.state.hasOwnProperty(name)) {
    const form = document.getElementById('article_editor_form');
    const editor = form.querySelector('.vergil').firstChild;

    // TODO: save in local
  }
}

// called via update by config form
function notifyCodeOnChange(instance) {
  const form = document.getElementById('article_editor_form');
  let code = form.querySelector('#editor_form_code');

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

class ArticleEditorForm extends Component {
  constructor(props) {
    super(props);

    this.props['action'] = '/api/' + this.props.namespace + '/' +
      this.props.slug + '/article/editor.json';

    this.props['validations'] = {
      content: {
        minLength: 0
      , maxLength: 9999
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
    , content: {
        errors: []
      , value: ''
      }
    };
  }

  render() {
    return h('form#article_editor_form.form', {
      action: this.props.action || ''
    , method: 'POST'
    , onSubmit: linkEvent(this, handleOnSubmit)
    }, [
      h('input', {
        type: 'hidden', name: 'csrf_token', value: this.state.csrfToken.value})
    , h('input#editor_form_code', {
        type: 'hidden'
      , name: 'code'
      , value: this.state.code.value
      , onChange: linkEvent(this, notifyCodeOnChange)
      })
    , h('input', {type: 'hidden', name: 'context', value: 'editor'})
    , h('.row', [
        h('.field-16', [
          h('.wrapper.editor', [
            h(Editor, {
              name: 'content'
            , config: {
                className: '.vergil'
              , content: document.querySelector('#content')
              , plugins: [
                  setPlaceholder('Write something here...')
                ]
              }
            , onFocusIn: linkEvent(this, handleOnFocusIn)
            , onFocusOut: linkEvent(this, handleOnFocusOut)
            , onInput: linkEvent(this, handleOnInput)
            })
          ])
        , buildErrorMessage(this.state.content)
        ])
      ])
    , h('.row', [
        h('.field-16', [
          h('.wrapper.action', [
            h('.action-bar', [
              h('button.flat.button', 'Save')
            , h('span.message', this.state.message)
            ])
          ])
        ])
      ])
    ]);
  }
}

module.exports = ArticleEditorForm;
