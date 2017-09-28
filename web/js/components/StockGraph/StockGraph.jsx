import React from 'react';
import PropTypes from 'prop-types';
import {Chart} from 'react-google-charts';

class StockGraph extends React.Component {
  static defaultProps = {
    id: 'line-chart'
  }
  static propTypes = {
    quotes: PropTypes.arrayOf(PropTypes.shape({
      name: PropTypes.string.isRequired,
      data: PropTypes.arrayOf(PropTypes.shape({date: PropTypes.instanceOf(Date).isRequired, value: PropTypes.number.isRequired}).isRequired).isRequired,
    }).isRequired).isRequired,
    id: PropTypes.string
  }
  render() {
    let chartData = this.props.quotes.map((quote, i) => ({
      index: i,
      ...quote,
    })).reduce((result, quote) => {
      result.names.push(quote.name);
      result.data = quote.data.reduce((result, datapoint) => {
        if (!(datapoint.date in result)) {
          result[datapoint.date] = []
        }
        while (result[datapoint.date].length < quote.index) {
          result[datapoint.date].push(null)
        }
        result[datapoint.date].push(datapoint.value);
        return result
      }, result.data);
      return result;
    }, {
      names: [],
      data: {},
    });
    chartData.data = Object.keys(chartData.data).map(k => [
      k, ...chartData.data[k],
    ]).map(v => {
      while (v.length < chartData.names.length + 1) {
        v = [
          ...v,
          null,
        ]
      }
      return v;
    })

    if (chartData.data.length === 0) {
      return <div>No data</div>;
    }
    return (
      <div className={'my-pretty-chart-container'}>
        <Chart
          chartType="LineChart"
          data={[
          [
            'Date', ...chartData.names,
          ],
          ...chartData.data,
        ]}
          options={{
          curveType: 'function',
          interpolateNulls: true
        }}
          graph_id={this.props.id}
          legend_toggle/>
      </div>
    );
  }
}

export default StockGraph
