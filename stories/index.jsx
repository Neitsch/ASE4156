import React from 'react';

import { storiesOf, addDecorator } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import { muiTheme } from 'storybook-addon-material-ui';
import appTheme from '../web/js/theme/muiTheme'
import { Button, Welcome } from '@storybook/react/demo';

import Shares from '../web/js/components/shares';
import AppBar from '../web/js/components/appbar';
import {CardWF, MediaCardWF} from '../web/js/components/card_wf';


addDecorator(muiTheme(appTheme));

storiesOf('Shares', module)
  .add('simple', () => <Shares />);


storiesOf('AppBar', module)
.add('Main app bar', () => <AppBar/>);

storiesOf('Cards', module)
  .add('Simple card', () => <CardWF title="Title" subtitle="sub" cardText="fdsa"/>)
  .add('Content card', () => <MediaCardWF content = {<h1>Content</h1>}/>);
