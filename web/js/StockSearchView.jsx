import React from 'react';
import { graphql, createRefetchContainer } from 'react-relay';
import { Chart } from 'react-google-charts';
import { DateRangePicker } from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';


class StockGraph extends React.Component {
  makeDate(date) {
    const dateParts = date.split("-")
    return new Date(dateParts[0], dateParts[1], dateParts[2])
  }
  render() {
    const data = this.props.quotes.map(q => [this.makeDate(q.date), q.value])
    if(data.length === 0) {
      return <div>No data</div>
    }
    return (
      <div className={'my-pretty-chart-container'}>
        <Chart
          chartType="LineChart"
          data={[['Date', 'Value'], ...data]}
          options={{}}
          graph_id={this.props.id}
          width="400px"
          height="400px"
          legend_toggle
        />
      </div>
    );
  }
}


class StockSearchView extends React.Component {
  constructor() {
    super();
    this.state = { text: 'Google', startDate: null, startDate: null, focusedInput: null };
  }
  setStateCallback = () => {
    this.props.relay.refetch(vars => {
      if(this.state.startDate == null || this.state.endDate == null) {
        return vars;
      }
      return {
        ...vars,
        text: this.state.text,
        start: this.state.startDate.format('YYYY-MM-DD'),
        end: this.state.endDate.format('YYYY-MM-DD'),
      }
    });
  }
  handleChange = (fieldName) => (e) => {
    e.preventDefault()
    let state = this.state;
    state[fieldName] = e.target.value;
    this.setState(state, this.setStateCallback);
  }
  render() {
    return (
      <div>
        <table style={{border: "1px solid black"}}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Average</th>
              <th>Chart</th>
            </tr>
          </thead>
          <tbody>
            {
              this.props.user.profile.stockFind.map(
                stock => (
                  <tr key={stock.id}>
                    <td>{stock.name}</td>
                    <td>{(stock.quoteInRange.map(d => d.value).reduce((s, v) => s + v, 0)/stock.quoteInRange.length).toFixed(2)}</td>
                    <td><StockGraph id={stock.id} quotes={stock.quoteInRange} /></td>
                  </tr>
                )
              )
            }
          </tbody>
        </table>
        <label>
          Name:
          <input type="text" value={this.state.text} onChange={this.handleChange('text')} />
        </label>
        <DateRangePicker
          startDate={this.state.startDate}
          endDate={this.state.endDate}
          onDatesChange={({ startDate, endDate }) => {
            this.setState({ startDate, endDate }, this.setStateCallback);
          }}
          focusedInput={this.state.focusedInput}
          onFocusChange={focusedInput => this.setState({ focusedInput })}
          isOutsideRange={() => false}
        />
      </div>
    );
  }
}

export default createRefetchContainer(StockSearchView, {
  user: graphql.experimental`
    fragment StockSearchView_user on GUser
    @argumentDefinitions(
      text: {type: "String!", defaultValue: "Google"},
      start: {type: "String!", defaultValue: "2016-08-20"},
      end: {type: "String!", defaultValue: "2016-09-20"},
    ) {
      profile {
        stockFind(text: $text) {
          id
          name
          quoteInRange(start: $start, end: $end) {
            date
            value
          }
        }
      }
    }
  `,
},
graphql.experimental`
  query StockSearchViewQuery($text: String!, $start: String!, $end: String!) {
    viewer {
      ...StockSearchView_user @arguments(text: $text, start: $start, end: $end)
    }
  }
`,
);
