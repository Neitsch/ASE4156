import React from 'react';
import { graphql, createRefetchContainer } from 'react-relay';

class StockSearchView extends React.Component {
  constructor() {
    super();
    this.state = { text: 'Google', start: '2016-08-20', end: '2016-09-20' };
  }
  handleChange = (fieldName) => (e) => {
    e.preventDefault()
    let state = this.state;
    state[fieldName] = e.target.value;
    this.setState(state);
    this.props.relay.refetch(vars => {
      vars[fieldName] = e.target.value;
      return vars;
    }, null);
  }
  render() {
    console.log(this.props);
    return (
      <div>
        <table style={{border: "1px solid black"}}>
          <tbody>
            <th>Name</th>
            <th>Average</th>
            {
              this.props.user.profile.stockFind.map(
                stock => (
                  <tr>
                    <td>{stock.name}</td>
                    <td>{(stock.quoteInRange.map(d => d.value).reduce((s, v) => s + v, 0)/stock.quoteInRange.length).toFixed(2)}</td>
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
        <label>
          Start:
          <input type="text" value={this.state.start} onChange={this.handleChange('start')} />
        </label>
        <label>
          End:
          <input type="text" value={this.state.end} onChange={this.handleChange('end')} />
        </label>
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
          name
          quoteInRange(start: $start, end: $end) {
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
