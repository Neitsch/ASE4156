// @flow
import React from 'react';
import { createRefetchContainer, graphql } from 'react-relay';
import InvestComposition from './InvestComposition';

import type { InvestCompositionRelay_bucket } from './__generated__/InvestCompositionRelay_bucket.graphql';

type ChunkList = Array<{
  id: string,
  name: string,
  quantity: number,
  value: number,
}>;

type Props = {
  bucket: InvestCompositionRelay_bucket,
  save: ChunkList => void,
  close: () => void,
}
type State = {
  chunks: ChunkList,
}

class InvestCompositionRelay extends React.Component<Props, State> {
  constructor(props) {
    super();
    this.state = {
      chunks: props.bucket.stocks.edges.map(s => ({
        id: s.node.id,
        quantity: s.node.quantity,
        value: s.node.stock.latestQuote.value,
        name: s.node.stock.name,
      })),
    };
  }
  save = () => {
    this.props.save(this.state.chunks);
    this.props.close();
  }
  cancel = () => {
    this.props.close();
  }
  updateChunks = chunks => this.setState(state => ({ chunks }))
  render() {
    return (
      <InvestComposition
        chunks={this.state.chunks}
        total={this.props.bucket.total}
        chunkUpdate={this.updateChunks}
        suggestionFieldChange={(text) => {}}
        suggestions={[{ id: '1', name: 'GOOGL', value: 50 }]}
        saveFunc={this.save}
        cancelFunc={this.cancel}
      />
    );
  }
}

export default createRefetchContainer(InvestCompositionRelay, {
  bucket: graphql`
    fragment InvestCompositionRelay_bucket on GInvestmentBucket {
      total
      stocks {
        edges {
          node {
            id
            quantity
            stock {
              name
              latestQuote {
                value
              }
            }
          }
        }
      }
    }
  `,
});
