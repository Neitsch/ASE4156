import React from 'react';
import {graphql, createRefetchContainer} from 'react-relay';
import {Chart} from 'react-google-charts';
import {DateRangePicker} from 'react-dates';
import StockGraph from './components/StockGraph/StockGraph'
import 'react-dates/lib/css/_datepicker.css';

class StockSearchView extends React.Component {
  constructor() {
    super();
    this.state = {
      text: 'Google',
      startDate: null,
      startDate: null,
      focusedInput: null
    };
  }
  setStateCallback = () => {
    this.props.relay.refetch(vars => {
      if (this.state.startDate == null || this.state.endDate == null) {
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
  makeDate(date) {
    const dateParts = date.split("-")
    const dateResult = new Date(dateParts[0], dateParts[1] - 1, dateParts[2])
    return dateResult
  }
  render() {
    const quotes = this.props.user.profile.stockFind.map(stock => ({
      name: stock.name,
      data: stock.quoteInRange.map(quote => ({
        ...quote,
        date: this.makeDate(quote.date),
      })),
    }))
    return (
      <div>
        <StockGraph quotes={quotes} compare={'PERCENT'}/>
        <table style={{
          border: "1px solid black"
        }}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Average</th>
              <th>Chart</th>
            </tr>
          </thead>
          <tbody>
            {this.props.user.profile.stockFind.map(stock => (
              <tr key={stock.id}>
                <td>{stock.name}</td>
                <td>{(stock.quoteInRange.map(d => d.value).reduce((s, v) => s + v, 0) / stock.quoteInRange.length).toFixed(2)}</td>
                <td><StockGraph
                  id={stock.id}
                  quotes={[{
                  name: stock.name,
                  data: stock.quoteInRange.map(quote => ({
                    ...quote,
                    date: this.makeDate(quote.date)
                  }))
                }
              ]}/></td>
              </tr>
            ))
}
          </tbody>
        </table>
        <label>
          Name:
          <input
            type="text"
            value={this.state.text}
            onChange={this.handleChange('text')}/>
        </label>
        <DateRangePicker
          startDate={this.state.startDate}
          endDate={this.state.endDate}
          onDatesChange={({startDate, endDate}) => {
          this.setState({
            startDate,
            endDate
          }, this.setStateCallback);
        }}
          focusedInput={this.state.focusedInput}
          onFocusChange={focusedInput => this.setState({focusedInput})}
          isOutsideRange={() => false}/>
      </div>
    );
  }
}

export default createRefetchContainer(StockSearchView, {
  user: graphql.experimental `
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
  `
}, graphql.experimental `
  query StockSearchViewQuery($text: String!, $start: String!, $end: String!) {
    viewer {
      ...StockSearchView_user @arguments(text: $text, start: $start, end: $end)
    }
  }
`,);
