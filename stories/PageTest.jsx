// @flow
import React from 'react';
import Grid from 'material-ui/Grid';
import { MuiThemeProvider, withStyles } from 'material-ui/styles';

import HighlightBox from '../web/js/components/HighlightBox/HighlightBox';
import StockGraph from '../web/js/components/StockGraph/StockGraph';
import InvestBucket from '../web/js/components/InvestBucket/InvestBucket';
import AppBar from '../web/js/components/AppBar';
import theme from '../web/js/theme/muiTheme';

const styles = ({
  root: {
    flexGrow: 3,
    marginTop: 100,
  },
  appBar: {
    marginBottom: theme.spacing.unit * 100,
  },
});

class PageTest extends React.Component<{}> {
  render() {
    const values = [
      {
        name: 'Your current net worth',
        data: [
          {
            date: new Date(2007, 1),
            value: 1000,
          }, {
            date: new Date(2008, 1),
            value: 1500,
          }, {
            date: new Date(2009, 1),
            value: 1600,
          }, {
            date: new Date(2011, 1),
            value: 1300,
          },
        ],
      }, {
        name: 'If you would have invested',
        data: [
          {
            date: new Date(2007, 1),
            value: 1000,
          }, {
            date: new Date(2008, 1),
            value: 1200,
          }, {
            date: new Date(2009, 1),
            value: 1800,
          }, {
            date: new Date(2010, 1),
            value: 2000,
          }, {
            date: new Date(2011, 1),
            value: 2100,
          },
        ],
      },
    ];
    return (
      <MuiThemeProvider theme={theme}>
      <div>
      <AppBar/>
      <div style={{margin:10}}>
      <Grid container spacing={16}>
        <Grid item xs={12} sm={6}>
          <Grid container spacing={16} align="stretch">
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Current balance'} value={'$1300'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Total Income'} value={'$300'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Total Expenditures'} value={'$250'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Another box'} value={'$1000'} />
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} sm={6}>
          <StockGraph
            title="Portfolio Growth"
            height="450px"
            id={'chart'}
            compare={'ABSOLUTE'}
            quotes={values}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Grid container spacing={16} align="stretch">
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Pumpkin'} value={'$13'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Fixed monthly'} value={'$200'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Invest Income'} value={'10%'} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <HighlightBox title={'Expendable cash'} value={'5%'} />
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Grid container spacing={16} align="stretch">
            <Grid item xs={12} sm={8} lg={4}>
              <InvestBucket
                title={'Risk 1'}
                attributes={{
                  good: [{
                    id: '1',
                    shortDesc: 'Good to get started',
                    editMode: false,
                  }, {
                    id: '2',
                    shortDesc: 'Low risk',
                    editMode: false,
                  }],
                  bad: [{
                    id: '3',
                    shortDesc: 'Low reward',
                    editMode: false,
                  }],
                }}
              />
            </Grid>
            <Grid item xs={12} sm={8} lg={4}>
              <InvestBucket
                title={'Risk 2'}
                attributes={{
                  good: [{
                    id: '1',
                    shortDesc: 'Allows you to take more risk',
                    editMode: false,
                  }, {
                    id: '2',
                    shortDesc: 'Pays significant rewards',
                    editMode: false,
                  }],
                  bad: [{
                    id: '3',
                    shortDesc: 'You might lose some money',
                    editMode: false,
                  }],
                }}
              />
            </Grid>
            <Grid item xs={12} sm={8} lg={4}>
              <InvestBucket
                title={'Risk 3'}
                attributes={{
                  good: [{
                    id: '1',
                    shortDesc: '$$$',
                    editMode: false,
                  }, {
                    id: '2',
                    shortDesc: 'More $$$',
                    editMode: false,
                  }],
                  bad: [{
                    id: '3',
                    shortDesc: 'You\'re fucking insane of you invest in this',
                    editMode: false,
                  }],
                }}
              />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
      </div>
      </div>
      </MuiThemeProvider>
    );
  }
}
export default withStyles(styles)(PageTest);
