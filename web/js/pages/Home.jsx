// @flow

import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import Grid from 'material-ui/Grid';

import PersonalStatusRelay from '../components/PersonalStatus/PersonalStatusRelay';
import BankAccountRelay from '../components/StockGraph/BankAccountRelay';
import InvestBucketGridRelay from '../components/InvestBucket/InvestBucketGridRelay';
import SnackbarErrorContext from '../components/ErrorReporting/SnackbarErrorContext';

import type { Home_viewer }
  from './__generated__/Home_viewer.graphql';

type Props = {
  viewer: Home_viewer,
}

class Home extends React.Component < Props > {
  render() {
    if (!this.props.viewer.userbank || this.props.viewer.userbank.edges.length === 0) {
      return null;
    }
    return (<SnackbarErrorContext>
      <Grid container spacing={16}>
        <Grid item xs={12} sm={6}>
          {this.props.viewer.userbank.edges[0]
            ? <PersonalStatusRelay bank={this.props.viewer.userbank.edges[0].node} />
            : null}
        </Grid>
        <Grid item xs={12} sm={6}>
          {this.props.viewer.userbank.edges[0]
            ? <BankAccountRelay bank={this.props.viewer.userbank.edges[0].node} />
            : null}
        </Grid>
        <Grid item xs={12} sm={6}>
          <InvestBucketGridRelay profile={this.props.viewer.profile} />
        </Grid>
      </Grid></SnackbarErrorContext>
    );
  }
}

export default createFragmentContainer(Home, { viewer: graphql `
    fragment Home_viewer on GUser {
      profile {
        ...InvestBucketGridRelay_profile
      }
      userbank {
        edges {
          node {
            ...BankAccountRelay_bank
            ...PersonalStatusRelay_bank
          }
        }
      }
    }
` });
