import React from 'react';
import PropTypes from 'prop-types';
import Card, {CardHeader, CardMedia, CardContent, CardActions} from 'material-ui/Card';

export class CardWF extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    cardText: PropTypes.any.isRequired,
    subtitle: PropTypes.string,
  }
  render() {
    return (
      <Card>
        <CardHeader title={this.props.title}/>
        <CardContent>
          {this.props.cardText}
        </CardContent>
      </Card>
    );
  }
}

export class MediaCardWF extends React.Component {
  static propTypes = {
    content: PropTypes.any.isRequired
  }
  render() {
    return (
      <Card>
        <div>
          {this.props.content}
        </div>
      </Card>
    );
  }
}
