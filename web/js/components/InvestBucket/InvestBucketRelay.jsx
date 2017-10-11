import React from 'react';
import {createFragmentContainer, grahpql} from 'react-relay';
import InvestBucket from './InvestBucket';

import type {InvestBucketRelay_bucket} from './__generated__/InvestBucketRelay_bucket.graphql';

type Props = {
  bucket: InvestBucketRelay_bucket,
}

class InvestBucketRelay extends React.Component<Props> {
  render() {
    const attributes = this.props.bucket.description.edges.reduce((all, item) => {
      all[item.node.isGood ? 'good' : 'bad'].push({shortDesc: item.node.text});
      return all;
    }, {
      good: [],
      bad: [],
    })
    return (
      <InvestBucket title={this.props.bucket.name} attributes={attributes} />
    );
  }
}

export default createFragmentContainer(InvestBucketRelay, {
  bucket: graphql`
    fragment InvestBucketRelay_bucket on GInvestmentBucket {
      name
      description {
        edges {
          node {
            text
            isGood
          }
        }
      }
    }
  `,
})
