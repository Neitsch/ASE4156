import React from 'react';
import { Text, View } from 'react-native';
import { graphql, QueryRenderer } from 'react-relay';
import environment from '../relay/environment.js';

export default class Root extends React.Component {
  render() {
    return (<QueryRenderer
      environment={environment}
      query={graphql ` query RootQuery { viewer { username } } `}
      render={({ error, props }) => {
        if (error) {
          return (
            <View>
              <Text>{error.message}</Text>
              <Text>{error.message}</Text>
              <Text>{error.message}</Text>
            </View>
          );
        } else if (props) {
          if (props.viewer != null) {
            return (
              <View>
                <Text>{props.viewer.username}
                is great!</Text>
                <a href="/logout">
                  <Text>Logout</Text>
                </a>
              </View>
            );
          }
          return <Text>Plz log in</Text>;
        }
        return <Text>Loading</Text>;
      }}
    />);
  }
}
