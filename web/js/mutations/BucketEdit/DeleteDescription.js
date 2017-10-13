// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation DeleteDescriptionMutation($id: ID!) {
    deleteAttribute(idValue: $id) {
      isOk
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
  id: string,
) => {
  const variables = {
    id,
  };
  const optimisticResponse = {
    deleteAttribute: {
      ok: true,
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
