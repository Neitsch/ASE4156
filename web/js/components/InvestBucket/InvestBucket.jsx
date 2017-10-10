import React from 'react';
import PropTypes from 'prop-types'
import Card, {CardHeader, CardMedia, CardContent, CardActions} from 'material-ui/Card';
import List, {ListItem, ListItemIcon, ListItemText} from 'material-ui/List';
import TrendingUpIcon from 'material-ui-icons/TrendingUp';
import TrendingDownIcon from 'material-ui-icons/TrendingDown';
import Button from 'material-ui/Button';

const propAttrShape = PropTypes.shape({shortDesc: PropTypes.string.isRequired})

class InvestBucket extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    attributes: PropTypes.shape({
      good: PropTypes.arrayOf(propAttrShape.isRequired),
      bad: PropTypes.arrayOf(propAttrShape.isRequired)
    })
  }
  static defaultProps = {
    attributes: {
      good: [],
      bad: [],
    }
  }
  renderAttr(attr, isGood) {
    let indicator = null;
    if (isGood) {
      indicator = <TrendingUpIcon/>;
    } else {
      indicator = <TrendingDownIcon/>
    }
    return (
      <ListItem key={attr.shortDesc}>
        <ListItemIcon>
          {indicator}
        </ListItemIcon>
        <ListItemText primary={attr.shortDesc}/>
      </ListItem>
    )
  }
  render() {
    return (
      <Card>
        <CardHeader title={this.props.title}/>
        <CardContent>
          <List>
            {this.props.attributes
              ? (this.props.attributes.good
                ? this.props.attributes.good.map(g => this.renderAttr(g, true))
                : []).concat(this.props.attributes.bad
                ? this.props.attributes.bad.map(b => this.renderAttr(b, false))
                : [])
              : null
}
          </List>
        </CardContent>
        <CardActions>
          <Button dense color="primary">
            Invest
          </Button>
          <Button dense color="primary">
            Learn More
          </Button>
        </CardActions>
      </Card>
    );
  }
}

export default InvestBucket;
