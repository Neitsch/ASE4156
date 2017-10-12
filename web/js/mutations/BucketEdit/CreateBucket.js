// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation CreateBucketMutation($name: String!, $public: Boolean!) {
    addBucket(name: $name, public: $public) {
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
  text: string, publicBucket: bool,
) => {
  const variables = {
    name: text,
    public: publicBucket,
  };
  const optimisticResponse = {
    addBucket: {
      bucket: {
        name: text,
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
