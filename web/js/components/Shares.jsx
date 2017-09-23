// @flow
import React from 'react';
import {Card, CardText, CardHeader} from 'material-ui/Card';
import {Table, TableBody, TableRow, TableRowColumn} from 'material-ui/Table';
import FlatButton from 'material-ui/FlatButton';
import {translate} from 'react-i18next';
import PropTypes from 'prop-types';
import numeral from 'numeral';

const formatMoney : (string, number) => string = function(currency : string, num : number) : string {
  return currency + numeral(num).format('0,0.00');
}

type valueShape = {
  name: string,
  value: number
}

class Shares extends React.Component {
  static defaultProps = {
    currency: "$",
    values: [],
  }
  static propTypes = {
    currency: PropTypes.string,
    values: PropTypes.arrayOf(PropTypes.shape({name: PropTypes.string.isRequired, value: PropTypes.number.isRequired,})),
  };
  constructor() : void {
    super();
    this.collectRow = this.collectRow.bind(this);
    this.valueRow = this.valueRow.bind(this);
    this.valueRows = this.valueRows.bind(this);
    this.renderCard = this.renderCard.bind(this);
  }
  collectRow() : React$Element < {} > {
    return(
      <TableRow>
        <TableRowColumn>{this.props.t('totalSharesValue')}</TableRowColumn>
        <TableRowColumn style={{
          textAlign: 'right'
        }}>
          {formatMoney(this.props.currency, this.props.values.reduce((sum, o) => sum + o.value, 0))}
        </TableRowColumn>
      </TableRow>
    );
  }
  valueRow(value : valueShape, i : number, a : Array < valueShape >) : React$Element <*> {
    return(
      <TableRow displayBorder={i == a.length - 1} key={i}>
        <TableRowColumn>{this.props.t(value.name)}</TableRowColumn>
        <TableRowColumn style={{
          textAlign: 'right'
        }}>{formatMoney(this.props.currency, value.value)}</TableRowColumn>
      </TableRow>
    );
  }
  valueRows(values : Array < valueShape >) : Array < React$Element < {} >> {
    return values.map(this.valueRow);
  }
  renderCard(values : Array < React$Element < {} >>, bottom : React$Element < {} >, button : React$Element <*>) : React$Element < {} > {
    return(
      <Card>
        <CardHeader title="Shares"/>
        <CardText>
          <Table>
            <TableBody displayRowCheckbox={false}>
              {values}
              {bottom}
            </TableBody>
          </Table>
          {button}
        </CardText>
      </Card>
    )
  }
  render() : React$Element < {} > {
    return this.renderCard(this.valueRows(this.props.values), this.collectRow(this.props.values), < FlatButton backgroundColor = "#a4c639" label = "Sell Shares" fullWidth />);
  }
}

export default translate()(Shares);
