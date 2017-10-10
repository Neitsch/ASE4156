// @flow
import React from 'react';
import PropTypes from 'prop-types';
import Grid from 'material-ui/Grid';
import HighlightBox from '../HighlightBox';

import type {PersonalStatusRelay_bank}
from './__generated__/PersonalStatusRelay_bank.graphql';

type Props = {
  bank: PersonalStatusRelay_bank
}

export default class PersonalStatus extends React.Component < Props > {
  static propTypes = {
    bank: PropTypes.shape({balance: PropTypes.number.isRequired, income: PropTypes.number.isRequired, outcome: PropTypes.number.isRequired}).isRequired
  }
  render() {
    return (
      <Grid container spacing={16} align="stretch">
        <Grid item xs={12} sm={6}>
          <HighlightBox title={'Current balance'} value={this.props.bank.balance}/>
        </Grid>
        <Grid item xs={12} sm={6}>
          <HighlightBox title={'Total Income'} value={this.props.bank.income}/>
        </Grid>
        <Grid item xs={12} sm={6}>
          <HighlightBox title={'Total Expenditures'} value={this.props.bank.outcome}/>
        </Grid>
        <Grid item xs={12} sm={6}>
          <HighlightBox
            title={'Available money'}
            value={this.props.bank.income + this.props.bank.outcome}/>
        </Grid>
      </Grid>
    );
  }
}
