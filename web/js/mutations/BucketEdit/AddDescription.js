// @flow
import { graphql, commitMutation } from 'react-relay';

import type {
  RecordSourceSelectorProxy,
  RelayEnvironment,
  SelectorData,
} from 'react-relay';

const mutation = graphql`
  mutation AddDescriptionMutation($text: String!, $bucketName: String!, $isGood: Boolean!) {
    addAttributeToBucket(desc: $text, bucket: $bucketName, isGood: $isGood) {
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
  text: string, bucketName: string, isGood: bool,
) => {
  const variables = {
    text,
    bucketName,
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
