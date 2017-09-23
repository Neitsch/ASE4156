import React from 'react';
import PropTypes from 'prop-types';
import {Card, CardTitle, CardText,} from 'material-ui/Card';

export class CardWF extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    cardText: PropTypes.any.isRequired,
    subtitle: PropTypes.string,
  }
  render() {
    return (
      <Card zDepth={3}>
        <CardTitle title={this.props.title} subtitle={this.props.subtitle}/>
        <CardText>
          {this.props.cardText}
        </CardText>
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
      <Card zDepth={3}>
        <div>
          {this.props.content}
        </div>
      </Card>
    );
  }
}
