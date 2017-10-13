// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation EditDescriptionMutation($id: ID!, $text: String!) {
    editAttribute(desc: $text, idValue: $id) {
       bucketAttr {
         text
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
  text: string, id: string,
) => {
  const variables = {
    text,
    id,
  };
  const optimisticResponse = {
    editAttribute: {
      bucketAttr: {
        text,
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
