// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation AddDescriptionMutation($text: String!, $bucketId: ID!, $isGood: Boolean!) {
    addAttributeToBucket(desc: $text, bucketId: $bucketId, isGood: $isGood) {
       bucketAttr {
         text
         isGood
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
  text: string, bucketId: string, isGood: bool,
) => {
  const variables = {
    text,
    bucketId,
    isGood,
  };
  const optimisticResponse = {
    addAttributeToBucket: {
      bucketAttr: {
        text,
        isGood,
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
