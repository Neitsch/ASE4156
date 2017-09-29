import React from 'react';
import PropTypes from 'prop-types';
import {Card, CardHeader, CardText,} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import {List, ListItem} from 'material-ui/List';

class HighlightBox extends React.Component {
  static propTypes = {
    title: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
    secondaryInfo: PropTypes.arrayOf(PropTypes.shape({value: PropTypes.any.isRequired, text: PropTypes.any.isRequired}))
  }
  render() {
    console.log("Render");
    return (
      <Card containerStyle={{
        border: "1px solid black"
      }}>
        <CardHeader title={this.props.title}/>
        <CardText>
          <h1>{this.props.value}</h1>
          <Divider/>
          <List>
            {this.props.secondaryInfo
              ? this.props.secondaryInfo.map(secondary => {
                return (<ListItem
                  key={secondary.text}
                  primaryText={secondary.value + " " + secondary.text}/>);
              })
              : null
}</List>
        </CardText>
      </Card>
    );
  }
}

export default HighlightBox;
