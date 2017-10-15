import React from 'react';
import { MuiThemeProvider } from 'material-ui/styles';

import AppBar from './AppBar';
import theme from '../theme/muiTheme';


function layout(props) {
  return (
    <MuiThemeProvider theme={theme}>
      <div>
        <AppBar />
        {props.children}
      </div>
    </MuiThemeProvider>
  );
}

export default layout;
