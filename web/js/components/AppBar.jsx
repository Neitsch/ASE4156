import React from 'react';
import AppBar from 'material-ui/AppBar';
import muiTheme from '../theme/muiTheme.js'
import { appTheme }  from '../theme/muiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';



export default class App_Bar extends React.Component {
  render() {
    return (
    <AppBar title="Wells Fargo"
      iconClassNameRight="muidocs-icon-navigation-expand-more"
    />
    );
  }
}
