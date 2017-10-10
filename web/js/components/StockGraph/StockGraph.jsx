// @flow
import React from 'react';
import PropTypes from 'prop-types';
import {Chart} from 'react-google-charts';

class StockGraph extends React.Component <*> {
  static defaultProps = {
    id: 'line-chart',
    compare: 'ABSOLUTE',
    height: '400px'
  }
  static propTypes = {
    quotes: PropTypes.arrayOf(PropTypes.shape({
      name: PropTypes.string.isRequired,
      data: PropTypes.arrayOf(PropTypes.shape({date: PropTypes.instanceOf(Date).isRequired, value: PropTypes.number.isRequired}).isRequired).isRequired,
    }).isRequired).isRequired,
    id: PropTypes.string,
    compare: PropTypes.oneOf(['ABSOLUTE', 'PERCENT',]),
    height: PropTypes.string,
    title: PropTypes.string,
  }
  render() {
    let chartData = this.props.quotes.map((quote, i) => ({
      index: i,
      ...quote,
    })).reduce((result, quote) => {
      const scale = this.props.compare === 'ABSOLUTE'
        ? 1
        : (1.0 / quote.data[0].value)
      result.names.push(quote.name);
      result.data = quote.data.reduce((result, datapoint) => {
        const datetime = datapoint.date.getTime()
        if (!(datetime in result)) {
          result[datetime] = []
        }
        while (result[datetime].length < quote.index) {
          result[datetime].push(null)
        }
        result[datetime].push(datapoint.value * scale);
        return result
      }, result.data);
      return result;
    }, {
      names: [],
      data: {}
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
    }).sort((a, b) => a[0] - b[0]).map(d => {
      d[0] = new Date(parseInt(d[0]));
      return d;
    })

    if (chartData.data.length === 0) {
      return <div>No data</div>;
    }
    let extraOptions = {}
    if (this.props.compare === 'PERCENT') {
      extraOptions = {
        vAxis: {
          format: 'percent' //'#,%'
        }
      }
    }
    return (
      <div className={'my-pretty-chart-container'}>
        <Chart
          width="100%"
          height={this.props.height}
          chartType="LineChart"
          data={[
          [
            'Date', ...chartData.names,
          ],
          ...chartData.data,
        ]}
          options={{
          curveType: 'function',
          interpolateNulls: true,
          title: this.props.title,
          ...extraOptions
        }}
          graph_id={this.props.id}
          legend_toggle/>
      </div>
    );
  }
}

export default StockGraph
