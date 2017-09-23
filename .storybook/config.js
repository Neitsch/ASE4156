import {configure} from '@storybook/react';
import {addDecorator} from '@storybook/react';
import {muiTheme} from 'storybook-addon-material-ui';
import {withKnobs, number, text,} from '@storybook/addon-knobs';
import React from 'react';
import i18nEn from '../web/i18n/en';
import {I18nextProvider} from 'react-i18next';
import appTheme from '../web/js/theme/muiTheme'

const i18nDecorator = children => <I18nextProvider i18n={i18nEn}>{children()}</I18nextProvider>;
function loadStories() {
  require('../stories');
}

addDecorator(muiTheme(appTheme))
addDecorator(withKnobs)
addDecorator(i18nDecorator)

configure(loadStories, module);
