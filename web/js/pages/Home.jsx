import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import Grid from 'material-ui/Grid';

import HighlightBox from '../components/HighlightBox/HighlightBox';

class Home extends React.Component {
  render() {
    if (this.props.user.userbank.edges.length === 0) {
      return null;
    }
    return (
      <Grid container spacing={16}>
        <Grid item xs={12} sm={6}>
          <Grid container spacing={16} align="stretch">
            <Grid item xs={12} sm={6}>
              <HighlightBox
                title={'Current balance'}
                value={this.props.user.userbank.edges[0].node.balance}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Total Income'} value={'$300'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Total Expenditures'} value={'$250'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Another box'} value={'$1000'} />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default createFragmentContainer(Home, { user: graphql `
    fragment Home_user on GUser {
      userbank {
        edges {
          node {
            balance
          }
        }
      }
    }
` });
