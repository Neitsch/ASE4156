// @flow
import React from 'react';
import { createRefetchContainer, graphql } from 'react-relay';
import { ConnectionHandler } from 'relay-runtime';
import InvestBucket from './InvestBucket';
import InvestCompositionRelay from './InvestCompositionRelay';
import addDescription from '../../mutations/BucketEdit/AddDescription';

import type { InvestBucketRelay_bucket } from './__generated__/InvestBucketRelay_bucket.graphql';
import type { RelayContext } from 'react-relay';

type State = {
  itemCount: number,
  compositionDialog: bool,
}
type Props = {
  bucket: InvestBucketRelay_bucket,
  relay: RelayContext,
}

class InvestBucketRelay extends React.Component<Props, State> {
  constructor() {
    super();
    this.state = {
      itemCount: 2,
      compositionDialog: false,
    };
  }
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
    let seeMoreFunc = null;
    if (this.props.bucket.description && this.props.bucket.description.pageInfo.hasNextPage) {
      seeMoreFunc = () => {
        this.setState(
          state => ({ itemCount: state.itemCount + 2 }),
          () => this.props.relay.refetch(() => ({
            id: this.props.bucket.id,
            first: this.state.itemCount,
          })))
        ;
      };
    }
    return (
      <div>
        {
          this.state.compositionDialog ?
            <InvestCompositionRelay
              close={() => this.setState(() => ({ compositionDialog: false }))}
              bucket={this.props.bucket}
              save={chunks => console.log(chunks)}
            /> :
            null
        }
        <InvestBucket
          title={this.props.bucket.name}
          attributes={attributes}
          editFunc={editFunc}
          seeMoreFunc={seeMoreFunc}
          editCompositionFunc={() => this.setState(() => ({ compositionDialog: true }))}
        />
      </div>
    );
  }
}

export default createRefetchContainer(InvestBucketRelay, {
  bucket: graphql`
    fragment InvestBucketRelay_bucket on GInvestmentBucket
    @argumentDefinitions(
      first: {type: "Int!", defaultValue: 2}
    ) {
      id
      name
      isOwner
      description(first: $first) @connection(key: "InvestBucketRelay_description") {
        edges {
          node {
            text
            isGood
          }
        }
        pageInfo {
          hasNextPage
        }
      }
      ...InvestCompositionRelay_bucket
    }
  `,
}, graphql`
  query InvestBucketRelayQuery($id: ID!, $first: Int!) {
    investBucket(id: $id) {
      ...InvestBucketRelay_bucket @arguments(first: $first)
    }
  }
`);
