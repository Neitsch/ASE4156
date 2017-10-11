// @flow
import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import { ConnectionHandler } from 'relay-runtime';
import InvestBucket from './InvestBucket';
import addDescription from '../../mutations/BucketEdit/AddDescription';

import type { InvestBucketRelay_bucket } from './__generated__/InvestBucketRelay_bucket.graphql';
import type { RelayContext } from 'react-relay';

type Props = {
  bucket: InvestBucketRelay_bucket,
  relay: RelayContext,
}

class InvestBucketRelay extends React.Component<Props> {
  render() {
    let data;
    if (!this.props.bucket.description) {
      data = [];
    } else {
      data = this.props.bucket.description.edges;
    }
    const attributes = data.reduce((all, item) => {
      if (!item || !item.node) {
        return all;
      }
      all[item.node.isGood ? 'good' : 'bad'].push({ shortDesc: item.node.text });
      return all;
    }, {
      good: [],
      bad: [],
    });
    let editFunc = null;
    if (this.props.bucket.isOwner) {
      const updater = (store) => {
        const connection = ConnectionHandler.getConnection(
          store.get(this.props.bucket.id),
          'InvestBucketRelay_description',
        );
        const newEdge = ConnectionHandler.createEdge(
          store,
          connection,
          store.getRootField('addAttributeToBucket').getLinkedRecord('bucketAttr'),
          'GInvestmentBucketAttributeConnection',
        );
        ConnectionHandler.insertEdgeAfter(connection, newEdge);
      };
      editFunc = (text, isGood) => addDescription(
        updater, updater,
      )(
        this.props.relay.environment,
      )(
        text, this.props.bucket.name, isGood,
      );
    }
    return (
      <InvestBucket
        title={this.props.bucket.name}
        attributes={attributes}
        editFunc={editFunc}
      />
    );
  }
}

export default createFragmentContainer(InvestBucketRelay, {
  bucket: graphql`
    fragment InvestBucketRelay_bucket on GInvestmentBucket {
      id
      name
      isOwner
      description(first: 3) @connection(key: "InvestBucketRelay_description") {
        edges {
          node {
            text
            isGood
          }
        }
      }
    }
  `,
});
