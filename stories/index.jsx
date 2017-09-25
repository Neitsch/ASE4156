import React from 'react';

import { storiesOf, addDecorator } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import { number, text } from '@storybook/addon-knobs';

import AppBar from '../web/js/components/AppBar';
import { CardWF, MediaCardWF } from '../web/js/components/Cards';

storiesOf('AppBar', module).add('Main app bar', () => <AppBar />);

storiesOf('Cards', module).add('Simple card', () => <CardWF title="Title" subtitle="sub" cardText="fdsa" />).add('Content card', () => <MediaCardWF content={<h1 > Content </h1>} />);
