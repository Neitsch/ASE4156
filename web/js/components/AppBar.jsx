import React from 'react';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';

export default class App_Bar extends React.Component {
  render() {
    return (
      <AppBar position="static" color="default">
        <Toolbar>
          <Typography>
            Wells Fargo
          </Typography>
        </Toolbar>
      </AppBar>
    );
  }
}
