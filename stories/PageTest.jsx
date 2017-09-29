import React from 'react';
import Grid from 'material-ui/Grid';

import Saldo from '../web/js/components/Saldo';
import HighlightBox from '../web/js/components/HighlightBox/HighlightBox';

class PageTest extends React.Component {
  render() {
    return (
      <Grid container spacing={16}>
        <Grid item xs={4}>
          <HighlightBox title={'Title 1'} value={'1'} />
        </Grid>
        <Grid item xs={4}>
          <HighlightBox title={'Title 3'} value={'3'} />
        </Grid>
        <Grid item xs={4}>
          <HighlightBox title={'Title 2'} value={'2'} />
        </Grid>
        <Grid item xs={4}>
          <HighlightBox title={'Title 4'} value={'2'} />
        </Grid>
        <Grid item xs={4}>
          <HighlightBox title={'Title 5'} value={'2'} />
        </Grid>
      </Grid>
    );
  }
}

export default PageTest;
