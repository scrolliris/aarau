import i18next from 'i18next.js';
import XHRBackend from 'i18next-xhr-backend.js';
import BrowserLanguageDetector from 'i18next-browser-languagedetector.js';


exports.i18n = i18next;

exports.loadI18n = function(callback, loadPath) {
  i18next
    .use(XHRBackend)
    .use(BrowserLanguageDetector)
    .init({
      fallbackLng: 'en'
    , debug: false
    , ns: ['console']
    , defaultNS: 'console'
    , fallbackNS: false
    , whitelist: ['en']
    , load: 'languageOnly'
    , lowerCaseLng: true
    , keySeparator: false
    , pluralSeparator: '__'
    , contextSeparator: '__'
    , interpolationPrefix: '${'
    , interpolationSuffix: '}'
    , backend: {
        loadPath: loadPath
      , crossDomain: true
      }
    }, callback);
};
