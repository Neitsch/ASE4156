// @flow
import React from 'react';
import Card, {CardHeader, CardMedia, CardContent, CardActions,} from 'material-ui/Card';
import Table, {TableBody, TableCell, TableHead, TableRow,} from 'material-ui/Table';
import Button from 'material-ui/Button';
import PropTypes from 'prop-types';
import numeral from 'numeral';
import {withStyles} from 'material-ui/styles';

const formatMoney : (string, number) => string = function(currency : string, num : number) : string {
  return currency + numeral(num).format('0,0.00');
}

type valueShape = {
  name: string,
  value: number,
}

const MyTableCell = withStyles(theme => ({
  root: {
    borderBottom: `0px`
  }
}))(TableCell);

class Saldo extends React.Component <*> {
  static defaultProps = {
    currency: "$",
    values: [],
    t: w => w,
    showTotal: true,
  };
  static propTypes = {
    t: PropTypes.func,
    currency: PropTypes.string,
    values: PropTypes.arrayOf(PropTypes.shape({name: PropTypes.string.isRequired, value: PropTypes.number.isRequired})),
    showTotal: PropTypes.bool,
  };
  constructor() : void {
    super();
    // this.collectRow = this.collectRow.bind(this); this.valueRow =
    // this.valueRow.bind(this); this.valueRows = this.valueRows.bind(this);
    // this.renderCard = this.renderCard.bind(this);
  }
  collectRow = () => {
    return (
      <TableRow>
        <MyTableCell>{this.props.t('totalSharesValue')}</MyTableCell>
        <MyTableCell style={{
          textAlign: 'right'
        }}>
          {formatMoney(this.props.currency, this.props.values.reduce((sum, o) => sum + o.value, 0))}
        </MyTableCell>
      </TableRow>
    );
  }
  valueRow = (value : valueShape, i : number, a : Array < valueShape >) => {
    const Comp = i == a.length - 1
      ? TableCell
      : MyTableCell;
    return (
      <TableRow key={i}>
        <Comp>{this.props.t(value.name)}</Comp>
        <Comp style={{
          textAlign: 'right'
        }}>{formatMoney(this.props.currency, value.value)}</Comp>
      </TableRow>
    );
  }
  valueRows = (values : Array < valueShape >) => {
    return values.map(this.valueRow);
  }
  renderCard = (values : Array < React$Element < *>>, bottom :
    ? React$Element < * >, button : React$Element <*>) => {
    return (
      <Card>
        <CardHeader title="Saldo"/>
        <CardContent>
          <Table>
            <TableBody>
              {values}
              {bottom}
            </TableBody>
          </Table>
          {button}
        </CardContent>
      </Card>
    )
  }
  render() : React$Element < * > {
    let collectRow = null;
    if (this.props.showTotal) {
      collectRow = this.collectRow();
    }
    const button = <Button raised>
      Sell Shares
    </Button>;
    return this.renderCard(this.valueRows(this.props.values), collectRow, button);
  }
}

export default Saldo;
