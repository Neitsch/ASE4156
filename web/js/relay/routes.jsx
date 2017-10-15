import makeRouteConfig from 'found/lib/makeRouteConfig';
import Route from 'found/lib/Route';
import React from 'react';
import { graphql } from 'react-relay';

import Home from '../pages/Home';

export default makeRouteConfig(
  <Route
    path="/home"
    Component={Home}
    query={graphql`
      query routesQuery {
        viewer {
          ...Home_viewer
        }
      }
    `}
  />,
);
