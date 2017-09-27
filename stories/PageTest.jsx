import React from 'react';
import { GridList, GridTile } from 'material-ui/GridList';

import Saldo from '../web/js/components/Saldo';
import HighlightBox from '../web/js/components/HighlightBox/HighlightBox';

class PageTest extends React.Component {
  render() {
    return (
      <GridList cellHeight={'auto'} cols={3}>
        <GridTile rows={1} cols={1}>
          <HighlightBox title={'Title 1'} value={'1'} />
        </GridTile>
        <GridTile rows={2} cols={2}>
          <HighlightBox title={'Title 3'} value={'3'} />
        </GridTile>
        <GridTile rows={1} cols={1}>
          <HighlightBox title={'Title 2'} value={'2'} />
        </GridTile>
        <GridTile rows={1} cols={1}>
          <HighlightBox title={'Title 4'} value={'2'} />
        </GridTile>
        <GridTile rows={1} cols={1}>
          <HighlightBox title={'Title 5'} value={'2'} />
        </GridTile>
      </GridList>
    );
  }
}

export default PageTest;
