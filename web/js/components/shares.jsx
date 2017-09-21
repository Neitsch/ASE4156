import React from 'react';
import { Card, CardText, CardHeader } from 'material-ui/Card';
import { Table, TableBody, TableRow, TableRowColumn } from 'material-ui/Table';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import FlatButton from 'material-ui/FlatButton';
import muiTheme from '../theme/muiTheme';


export default class Shares extends React.Component {
  render() {
    return (
      <Card>
        <CardHeader title="Shares" />
        <CardText>
          <Table>
            <TableBody displayRowCheckbox={false}>
              <TableRow displayBorder={false}>
                <TableRowColumn>Invested Shares</TableRowColumn>
                <TableRowColumn style={{ textAlign: 'right' }}>700.00</TableRowColumn>
              </TableRow>
              <TableRow displayBorder={false}>
                <TableRowColumn>Earned Shares</TableRowColumn>
                <TableRowColumn style={{ textAlign: 'right' }}>74.934</TableRowColumn>
              </TableRow>
              <TableRow displayBorder={false}>
                <TableRowColumn>Bonus Shares</TableRowColumn>
                <TableRowColumn style={{ textAlign: 'right' }}>0.00</TableRowColumn>
              </TableRow>
              <TableRow>
                <TableRowColumn>Reinvested Shares</TableRowColumn>
                <TableRowColumn style={{ textAlign: 'right' }}>0.00</TableRowColumn>
              </TableRow>
              <TableRow>
                <TableRowColumn>Total Shares</TableRowColumn>
                <TableRowColumn style={{ textAlign: 'right' }}>774.934</TableRowColumn>
              </TableRow>
            </TableBody>
          </Table>
          <FlatButton backgroundColor="#a4c639" label="Sell Shares" fullWidth />
        </CardText>
      </Card>
    );
  }
}
