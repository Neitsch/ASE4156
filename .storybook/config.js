import { configure } from '@storybook/react';
import 'storybook-addon-material-ui';

function loadStories() {
  require('../stories');
}

configure(loadStories, module);
