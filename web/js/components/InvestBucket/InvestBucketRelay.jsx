// @flow
import React from 'react';
import { createRefetchContainer, graphql } from 'react-relay';
import { ConnectionHandler } from 'relay-runtime';
import InvestBucket from './InvestBucket';
import InvestCompositionRelay from './InvestCompositionRelay';
import addDescription from '../../mutations/BucketEdit/AddDescription';
import editDescription from '../../mutations/BucketEdit/EditDescription';
import deleteDescription from '../../mutations/BucketEdit/DeleteDescription';
import changeBucketComposition from '../../mutations/BucketEdit/ChangeBucketComposition';
import LockIcon from 'material-ui-icons/Lock';

import type { InvestBucketRelay_bucket } from './__generated__/InvestBucketRelay_bucket.graphql';
import type { InvestBucketRelay_profile } from './__generated__/InvestBucketRelay_profile.graphql';
import type { RelayContext } from 'react-relay';

type EditObj = {
  shortDesc: string,
}
type State = {
  itemCount: number,
  compositionDialog: bool,
  editMode: ?string,
  editState: EditObj,
}
type Props = {
  bucket: InvestBucketRelay_bucket,
  profile: InvestBucketRelay_profile,
  relay: RelayContext,
}

class InvestBucketRelay extends React.Component<Props, State> {
  constructor() {
    super();
    this.state = {
      itemCount: 2,
      compositionDialog: false,
      editMode: null,
      editState: { shortDesc: '' },
    };
  }
  launchEdit = id => () => {
    this.setState((state, props) => {
      if (!props.bucket.description || !props.bucket.description.edges) {
        return;
      }
      const item = props.bucket.description.edges.find(x => x && x.node && x.node.id == id);
      if (!item || !item.node || !item.node.text) {
        return;
      }
      return {
        editMode: id,
        editState: {
          shortDesc: item.node.text,
        },
      };
    });
  }
  saveChunks = (chunks) => {
    changeBucketComposition(
      null, null, null,
    )(
      this.props.relay.environment,
    )(
      chunks.map(c => ({ id: c.id, quantity: c.quantity })),
      this.props.bucket.id,
    );
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
      const textAttr = {};
      const iconAttr = {};
      let extra = {};
      if (!item || !item.node || !item.node.id) {
        return all;
      }
      const id = item.node.id;
      if (this.props.bucket.isOwner) {
        if (id == this.state.editMode) {
          textAttr.onKeyPress = (e) => {
            if (e.charCode == 13) {
              this.setState(() => ({
                editMode: null,
              }), () => {
                editDescription(
                  null, null, null,
                )(
                  this.props.relay.environment,
                )(
                  this.state.editState.shortDesc, id,
                );
              });
            }
          };
          textAttr.onChange = (e: SyntheticInputEvent<>) => {
            const text = e.target.value;
            this.setState(state => ({
              editState: {
                shortDesc: text,
              },
            }));
          };
          textAttr.autoFocus = true;
          iconAttr.onClick = () => {
            this.setState(() => ({
              editMode: null,
            }), () => {
              const updater = (store) => {
                store.delete(id);
              };
              deleteDescription(
                updater, updater, null,
              )(
                this.props.relay.environment,
              )(
                id,
              );
            });
          };
          extra = this.state.editState;
        } else {
          const edit = this.launchEdit(id);
          textAttr.onClick = edit;
          iconAttr.onClick = edit;
        }
      }
      all[item.node.isGood ? 'good' : 'bad'].push({
        ...item.node,
        text: textAttr,
        icon: iconAttr,
        editMode: (id === this.state.editMode),
        shortDesc: item.node.text,
        ...extra,
      });
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
    let title = this.props.bucket.name;
    if (!this.props.bucket.public) {
      title = <div>{title}<LockIcon /></div>;
    }
    return (
      <div>
        {
          this.state.compositionDialog ?
            <InvestCompositionRelay
              close={() => this.setState(() => ({ compositionDialog: false }))}
              bucket={this.props.bucket}
              save={this.saveChunks}
              profile={this.props.profile}
            /> :
            null
        }
        <InvestBucket
          title={title}
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
      public
      isOwner
      description(first: $first) @connection(key: "InvestBucketRelay_description") {
        edges {
          node {
            id
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
  profile: graphql`
    fragment InvestBucketRelay_profile on GProfile {
      ...InvestCompositionRelay_profile
    }
  `,
}, {
  bucket: graphql`
  query InvestBucketRelayQuery($id: ID!, $first: Int!) {
    investBucket(id: $id) {
      ...InvestBucketRelay_bucket @arguments(first: $first)
    }
  }
`,
});
