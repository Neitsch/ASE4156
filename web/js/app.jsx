import React from 'react';
import environment from './relay/environment';
import { graphql, QueryRenderer } from 'react-relay';

export default class App extends React.Component {
  render() {
    return (
      <QueryRenderer
        environment={environment}
        query={graphql`
          query appQuery {
            viewer {
              username
            }
          }
        `}
        render={({ error, props }) => {
          if (error) {
            return <div>{error.message}</div>;
          } else if (props) {
            if (props.viewer != null) {
              return (<div>
                <span>{props.viewer.username} is great!</span>
                <a href="/logout">Logout</a>
              </div>);
            }
            window.location.href = '/auth';
            return <h1>Plz log in</h1>;
          }
          return <div>Loading</div>;
        }}
      />
    );
  }
}
