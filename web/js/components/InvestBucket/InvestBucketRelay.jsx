// @flow
import React from 'react';
import {createFragmentContainer, graphql} from 'react-relay';
import InvestBucket from './InvestBucket';

import type {InvestBucketRelay_bucket} from './__generated__/InvestBucketRelay_bucket.graphql';

type Props = {
  bucket: InvestBucketRelay_bucket,
}

class InvestBucketRelay extends React.Component<Props> {
  render() {
    let data;
    if(!this.props.bucket.description) {
      data = []
    } else {
      data = this.props.bucket.description.edges;
    }
    const attributes = data.reduce((all, item) => {
      if(!item || !item.node) {
        return all;
      }
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
