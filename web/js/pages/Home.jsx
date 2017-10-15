// @flow

import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import Grid from 'material-ui/Grid';
import { MuiThemeProvider } from 'material-ui/styles';


import PersonalStatusRelay from '../components/PersonalStatus/PersonalStatusRelay';
import BankAccountRelay from '../components/StockGraph/BankAccountRelay';
import InvestBucketGridRelay from '../components/InvestBucket/InvestBucketGridRelay';
import AppBar from '../components/AppBar';
import theme from '../theme/muiTheme';
import { withStyles } from 'material-ui/styles';


import type { Home_user }
  from './__generated__/Home_user.graphql';

type Props = {
  user: Home_user,
}

const styles = theme => ({
  grid: {
    marginLeft: 5,
    justify: 'space-around',
  },
});

class Home extends React.Component < Props > {
  render() {
    if (!this.props.user.userbank || this.props.user.userbank.edges.length === 0) {
      return null;
    }
    return (
      <MuiThemeProvider theme={theme}>
      <div>
        <AppBar />
        <div style={{margin:10}}>
          <Grid container spacing={16} className={this.props.grid}>
            <Grid item xs={12} sm={6}>
              {this.props.user.userbank.edges[0]
                ? <PersonalStatusRelay bank={this.props.user.userbank.edges[0].node} />
                : null}
            </Grid>
            <Grid item xs={12} sm={6}>
              {this.props.user.userbank.edges[0]
                ? <BankAccountRelay bank={this.props.user.userbank.edges[0].node} />
                : null}
            </Grid>
            <Grid item xs={12} sm={6}>
              <InvestBucketGridRelay profile={this.props.user.profile} />
            </Grid>
          </Grid>
          </div>
          </div>
        </MuiThemeProvider>
    );
  }
}
const homeStyled = withStyles(styles)(Home);

export default createFragmentContainer(homeStyled, { user: graphql `
    fragment Home_user on GUser {
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
