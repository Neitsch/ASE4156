// @flow
import React from 'react';
import Dialog, {
  DialogContent,
  DialogTitle,
  DialogActions,
} from 'material-ui/Dialog';
import Button from 'material-ui/Button';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Slider from 'rc-slider';

import StockGraph from '../StockGraph/StockGraph';

type Props = {
  available: number,
  bucket: {
    name: string,
    value: number,
    ownedAmount: number,
  },
  investFunc: number => void,
  closeFunc: () => void,
}
type State = {
  investedAmount: number,
}

class InvestComposition extends React.Component<Props, State> {
  constructor() {
    super();
    this.state = {
      investedAmount: 0,
    };
  }
  render() {
    const values = [{
      name: 'Chart 2',
      data: [
        {
          date: new Date(2007, 1),
          value: 5,
        }, {
          date: new Date(2008, 1),
          value: 2,
        }, {
          date: new Date(2009, 1),
          value: 1,
        }, {
          date: new Date(2010, 1),
          value: 7,
        },
      ],
    }];
    const ownedQuantity = this.props.bucket.ownedAmount;
    const additionalQuantity = this.state.investedAmount / this.props.bucket.value;
    const ownedValue = this.props.bucket.ownedAmount * this.props.bucket.value;
    const additionalValue = this.state.investedAmount;
    const totalValue = ownedValue + additionalValue;

    return (
      <Dialog open>
        <DialogTitle>Invest into bucket</DialogTitle>
        <DialogContent>
          <StockGraph
            id="chart"
            title="Test Chart"
            quotes={values}
          />
          <Slider
            value={totalValue}
            onChange={investedAmount => this.setState(() => ({
              investedAmount: investedAmount - ownedValue,
            }))}
            max={this.props.available + ownedValue}
            step={0.01}
          />
          <Table>
            <TableHead>
              <TableRow>
                <TableCell padding="dense">Name</TableCell>
                <TableCell padding="dense">Quantity</TableCell>
                <TableCell padding="dense">Value</TableCell>
                <TableCell padding="dense">Total Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell padding="dense">{this.props.bucket.name} (Owned)</TableCell>
                <TableCell padding="dense">{ownedQuantity.toFixed(2)}</TableCell>
                <TableCell padding="dense">{this.props.bucket.value}</TableCell>
                <TableCell padding="dense">{ownedValue.toFixed(2)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell padding="dense">{this.props.bucket.name} {additionalValue !== 0 ? <span>({additionalValue > 0 ? 'Buy' : 'Sell'})</span> : null}</TableCell>
                <TableCell padding="dense">{additionalQuantity.toFixed(2)}</TableCell>
                <TableCell padding="dense">{this.props.bucket.value}</TableCell>
                <TableCell padding="dense">{additionalValue.toFixed(2)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell padding="dense">Available</TableCell>
                <TableCell padding="dense" />
                <TableCell padding="dense" />
                <TableCell padding="dense">{(this.props.available - this.state.investedAmount).toFixed(2)}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={this.props.cancelFunc}>Cancel</Button>
          <Button onClick={() => this.props.investFunc(additionalQuantity)}>
            Invest
          </Button>
        </DialogActions>
      </Dialog>);
  }
}

export default InvestComposition;
