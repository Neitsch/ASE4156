// @flow

import React from 'react';
import {createFragmentContainer, graphql} from 'react-relay';
import Grid from 'material-ui/Grid';

import PersonalStatusRelay from '../components/PersonalStatus/PersonalStatusRelay';

import type {Home_user}
from './__generated__/Home_user.graphql';

type Props = {
  user: Home_user
}

class Home extends React.Component < Props > {
  render() {
    if (!this.props.user.userbank || this.props.user.userbank.edges.length === 0) {
      return null;
    }
    return (
      <Grid container spacing={16}>
        <Grid item xs={12} sm={6}>
          {this.props.user.userbank.edges[0]
            ? <PersonalStatusRelay bank={this.props.user.userbank.edges[0].node}/>
            : null}
        </Grid>
      </Grid>
    );
  }
}

export default createFragmentContainer(Home, {user: graphql `
    fragment Home_user on GUser {
      userbank {
        edges {
          node {
            ...PersonalStatusRelay_bank
          }
        }
      }
    }
`});
