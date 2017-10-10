import React from 'react';
import { storiesOf } from '@storybook/react';
import { number, text } from '@storybook/addon-knobs';
import InvestBucket from './InvestBucket';

storiesOf('InvestBucket', module).add('Playground', () => {
  const title = text('Title of the risk section', 'Risk 1');
  const riskList = {
    good: [
      {
        shortDesc: 'Good to get started',
      }, {
        shortDesc: 'Low risk',
      },
    ],
    bad: [
      {
        shortDesc: 'Low reward',
      },
    ],
  };
  return (<InvestBucket title={title} attributes={riskList} />);
});
