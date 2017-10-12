// @flow
import React from 'react';
import { storiesOf } from '@storybook/react';
import { text } from '@storybook/addon-knobs';
import InvestBucket from './InvestBucket';
import { action } from '@storybook/addon-actions';

storiesOf('InvestBucket', module).add('Playground', () => {
  const title = text('Title of the risk section', 'Risk 1');
  const riskList = {
    good: [
      {
        id: '1',
        shortDesc: 'Good to get started',
        editMode: false,
        text: {
          onClick: action('click1'),
        },
        icon: {
          onClick: action('click3'),
        },
      }, {
        id: '2',
        shortDesc: 'Low risk',
        editMode: true,
        text: {
          onClick: action('click2'),
        },
        icon: {
          onClick: action('click3'),
        },
      },
    ],
    bad: [
      {
        id: '3',
        shortDesc: 'Low reward',
        editMode: false,
        text: {
          onClick: action('click3'),
        },
        icon: {
          onClick: action('click3'),
        },
      },
    ],
  };
  return (<InvestBucket title={title} attributes={riskList} editFunc={action('edit')} />);
});
