// @flow
import React from 'react';
import { storiesOf } from '@storybook/react';
import { text } from '@storybook/addon-knobs';
import InvestBucket from './InvestBucket';
import InvestComposition from './InvestComposition';
import { action } from '@storybook/addon-actions';

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
  return (<InvestBucket title={title} attributes={riskList} editFunc={action('edit')} />);
});

storiesOf('InvestCompositionDontTest', module).add('Playground', () => {
  const chunks = [{
    name: 'Google',
    value: 150,
    quantity: 0.5,
    id: '1',
  }, {
    name: 'IBM',
    value: 100,
    quantity: 0.75,
    id: '2',
  }, {
    name: 'Palantir',
    value: 50,
    quantity: 2,
    id: '3',
  }, {
    name: 'Facebook',
    value: 100,
    quantity: 1,
    id: '4',
  }];
  const suggestions = [{
    name: 'GOOGL',
    value: 60,
    id: '5',
  }];
  return (
    <InvestComposition
      suggestions={suggestions}
      suggestionFieldChange={action('suggestionFieldChange')}
      total={400}
      chunks={chunks}
      chunkUpdate={action('chunkUpdate')}
      saveFunc={action('save')}
      cancelFunc={action('cancel')}
    />
  );
});
