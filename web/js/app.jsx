import React from 'react';
import environment from './relay/environment';
import { graphql, QueryRenderer } from 'react-relay';
import StockSearchView from './StockSearchView';
import Home from './pages/Home';

export default class App extends React.Component {
  render() {
    return (
      <QueryRenderer
        environment={environment}
        query={graphql ` query appQuery { viewer { username ...StockSearchView_user ...Home_user } } `}
        render={({ error, props }) => {
          if (error) {
            return <div>{error.message}</div>;
          } else if (props) {
            if (props.viewer != null) {
              return (
                <div>
                  {props.viewer.username}
                is great!
                  <Home user={props.viewer} />
                  <StockSearchView user={props.viewer} />
                  <a href="/logout">Logout</a>
                </div>
              );
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
