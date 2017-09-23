import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import { number, text } from '@storybook/addon-knobs';

import { Button, Welcome } from '@storybook/react/demo';

import Shares from '../web/js/components/shares';

storiesOf('Shares', module)
  .add('simple', () => {
    const values = [
      { name: 'investedSharesValue', value: number('Invested Shares Value', 700.00) },
      { name: 'earnedSharesValue', value: number('Earned Shares Value', 74.93) },
      { name: 'bonusSharesValue', value: number('Bonus Shares Value', 0.0) },
      { name: 'reinvestedSharesValue', value: number('Reinvested Shares Value', 0.0) },
    ];
    return (<Shares values={values} currency={text('Currency sign', '$')} />);
  });
