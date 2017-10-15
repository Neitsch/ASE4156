// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation CreateBucketMutation($name: String!, $public: Boolean!, $investment: Float!) {
    addBucket(name: $name, public: $public, investment: $investment) {
       bucket {
         id
         ...InvestBucketRelay_bucket
      }
    }
  }
`;

export default (
  updater?: ?(store: RecordSourceSelectorProxy, data: SelectorData) => void,
  optimisticUpdater?: ?(store: RecordSourceSelectorProxy) => void,
  onCompleted?: ?(response: ?Object, errors: ?[Error]) => void,
) => (
  environment: RelayEnvironment,
) => (
  text: string, publicBucket: bool, investment: number,
) => {
  const variables = {
    name: text,
    public: publicBucket,
    investment,
  };
  const optimisticResponse = {
    addBucket: {
      bucket: {
        name: text,
        available: investment,
        description: {
          edges: [],
        },
      },
    },
  };
  commitMutation(environment, {
    mutation,
    variables,
    updater,
    optimisticResponse,
    optimisticUpdater,
    onCompleted,
  });
};
