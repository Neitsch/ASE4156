import BrowserProtocol from 'farce/lib/BrowserProtocol';
import queryMiddleware from 'farce/lib/queryMiddleware';
import createFarceRouter from 'found/lib/createFarceRouter';
import createRender from 'found/lib/createRender';
import { Resolver } from 'found-relay';
import { CircularProgress } from 'material-ui/Progress';
import { MuiThemeProvider } from 'material-ui/styles';


import React from 'react';
import ReactDOM from 'react-dom';
import environment from './relay/environment';
import routes from './relay/routes';
import '../css/styles.css';
import theme from './theme/muiTheme';


const Router = createFarceRouter({
  historyProtocol: new BrowserProtocol(),
  historyMiddlewares: [queryMiddleware],
  routeConfig: routes,
  render: createRender({
    renderPending: () => (
      <MuiThemeProvider theme={theme}>
        <div style={{
          position: 'absolute',
          top: '50%',
          marginTop: '-100px',
          textAlign: 'center',
          width: '100%',
        }}
        >
          <div style={{
            marginLeft: 'auto',
            marginRight: 'auto',
          }}
          >
            <CircularProgress size={200} />
          </div>
        </div>
      </MuiThemeProvider>

    ),
  }),
  renderError: () => {
    window.location.href = '/login/google-oauth2';
  },
});

ReactDOM.render(
  <Router resolver={new Resolver(environment)} />,
  document.getElementById('react-app'),
);
