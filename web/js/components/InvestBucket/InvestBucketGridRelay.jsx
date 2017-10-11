import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import Grid from 'material-ui/Grid';
import InvestBucketRelay from './InvestBucketRelay';

import type {InvestBucketGridRelay_profile} from './__generated__/InvestBucketGridRelay_profile.graphql';

type Props = {
  profile: InvestBucketGridRelay_profile,
}

class InvestBucketGridRelay extends React.Component<Props> {
  render() {
    return (
      <Grid container spacing={16} align="stretch">
        {
          this.props.profile.investSuggestions.edges.map(b => (
            <Grid item xs={12} sm={8} lg={4} key={b.node.id}>
              <InvestBucketRelay bucket={b.node} />
            </Grid>
          ))
        }
      </Grid>
    )
  }
}

export default createFragmentContainer(InvestBucketGridRelay, {
  profile: graphql`
    fragment InvestBucketGridRelay_profile on GProfile {
      investSuggestions(first: 3) {
        edges {
          node {
            id
            ...InvestBucketRelay_bucket
          }
        }
      }
    }
  `,
})
