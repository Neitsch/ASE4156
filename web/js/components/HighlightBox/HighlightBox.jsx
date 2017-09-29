import React from 'react';
import PropTypes from 'prop-types';
import Card, {CardHeader, CardMedia, CardContent, CardActions} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import List, {ListItem, ListItemText,} from 'material-ui/List';

class HighlightBox extends React.Component {
  static propTypes = {
    title: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
    secondaryInfo: PropTypes.arrayOf(PropTypes.shape({value: PropTypes.any.isRequired, text: PropTypes.any.isRequired,})),
  }
  render() {
    console.log("Render");
    return (
      <Card>
        <CardHeader title={this.props.title}/>
        <CardContent>
          <h1>{this.props.value}</h1>
          <Divider/>
          <List>
            {this.props.secondaryInfo
              ? this.props.secondaryInfo.map(secondary => {
                return (
                  <ListItem>
                    <ListItemText>{secondary.value + " " + secondary.text}</ListItemText>
                  </ListItem>
                );
              })
              : null
}</List>
        </CardContent>
      </Card>
    );
  }
}

export default HighlightBox;
