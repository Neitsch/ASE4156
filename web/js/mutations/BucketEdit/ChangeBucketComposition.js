// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation ChangeBucketCompositionMutation($id: ID!, $config: [GInvestmentBucketConfigurationUpdate]!) {
    editConfiguration(config: $config, idValue: $id) {
       bucket {
         id
         ...InvestCompositionRelay_bucket
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
  config: Array<{id: string, quantity: number}>, id: string,
) => {
  const variables = {
    config: config.map(c => ({ idValue: c.id, quantity: c.quantity })),
    id,
  };
  const optimisticResponse = {
    editConfiguration: {
      bucket: {
        id,
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
