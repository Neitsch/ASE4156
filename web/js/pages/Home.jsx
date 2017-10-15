// @flow

import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import Grid from 'material-ui/Grid';
import { MuiThemeProvider, withStyles } from 'material-ui/styles';
import Paper from 'material-ui/Paper';
import theme from '../theme/muiTheme';


import PersonalStatusRelay from '../components/PersonalStatus/PersonalStatusRelay';
import BankAccountRelay from '../components/StockGraph/BankAccountRelay';
import InvestBucketGridRelay from '../components/InvestBucket/InvestBucketGridRelay';
import SnackbarErrorContext from '../components/ErrorReporting/SnackbarErrorContext';
import AppBar from '../components/AppBar';

import type { Home_viewer }
  from './__generated__/Home_viewer.graphql';

type Props = {
  viewer: Home_viewer,
}

const styles = ({
  grid: {
    marginLeft: 5,
    justify: 'space-around',
  },
});

class Home extends React.Component < Props > {
  componentWillMount() {
    document.body.style.margin = 0;
    document.body.style.backgroundColor = '#F5F5F5';
  }

  render() {
    if (!this.props.viewer.userbank || this.props.viewer.userbank.edges.length === 0) {
      return null;
    }
    return (
      <MuiThemeProvider theme={theme}>
        <div>
          <AppBar />
          <div style={{ margin: 10 }}>
            <SnackbarErrorContext>
              <Grid container spacing={16} className={this.props.grid}>
                <Grid item xs={12} sm={6}>
                  {this.props.viewer.userbank.edges[0]
                    ? <PersonalStatusRelay bank={this.props.viewer.userbank.edges[0].node} />
                    : null}
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper>
                    {this.props.viewer.userbank.edges[0]
                      ? <BankAccountRelay bank={this.props.viewer.userbank.edges[0].node} />
                      : null}
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <InvestBucketGridRelay profile={this.props.viewer.profile} />
                </Grid>
              </Grid>
            </SnackbarErrorContext>
          </div>
        </div>
      </MuiThemeProvider>
    );
  }
}
const homeStyled = withStyles(styles)(Home);

export default createFragmentContainer(homeStyled, { viewer: graphql `
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
