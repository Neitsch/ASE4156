// @flow
import React from 'react';
import PropTypes from 'prop-types';
import TextField from 'material-ui/TextField';
import Card, { CardHeader, CardMedia, CardContent, CardActions } from 'material-ui/Card';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import TrendingUpIcon from 'material-ui-icons/TrendingUp';
import TrendingDownIcon from 'material-ui-icons/TrendingDown';
import Button from 'material-ui/Button';
import AddIcon from 'material-ui-icons/Add';

const propAttrShape = PropTypes.shape({ shortDesc: PropTypes.string.isRequired });

type State = {
  editMode: bool,
  editText: string,
  editGood: bool,
}
type ItemObj = {
  shortDesc: string,
}
type Props = {
  title: string,
  attributes: {
    good: Array<ItemObj>,
    bad: Array<ItemObj>,
  },
  editFunc?: ?(text: string, isGood: bool) => void,
  seeMoreFunc?: ?() => void,
}

class InvestBucket extends React.Component <Props, State> {
  static propTypes = {
    title: PropTypes.string.isRequired,
    attributes: PropTypes.shape({
      good: PropTypes.arrayOf(propAttrShape.isRequired),
      bad: PropTypes.arrayOf(propAttrShape.isRequired),
    }),
    editFunc: PropTypes.func,
    seeMoreFunc: PropTypes.func,
  }
  static defaultProps = {
    attributes: {
      good: [],
      bad: [],
    },
    editFunc: null,
    seeMoreFunc: null,
  }
  constructor() {
    super();
    this.state = {
      editMode: false,
      editText: '',
      editGood: true,
    };
  }
  updateText = (e: SyntheticInputEvent<>) => {
    const text = e.target.value;
    this.setState(() => ({
      editText: text,
    }));
  }
  onEnterPress = (e: SyntheticEvent<>) => {
    if (e.charCode == 13 && this.props.editFunc) {
      this.props.editFunc(this.state.editText, this.state.editGood);
      this.setState(() => ({
        editMode: false,
        editText: '',
        editGood: true,
      }));
    }
  }
  launchEdit = (mode: bool) => () => this.setState(() => ({ editMode: mode }))
  editField = () => (
    <ListItem>
      <ListItemIcon onClick={() => this.setState(state => ({ editGood: !state.editGood }))}>
        {this.state.editGood ? <TrendingUpIcon /> : <TrendingDownIcon />}
      </ListItemIcon>
      <TextField
        autoFocus
        margin="dense"
        id="name"
        label="New Attribute"
        type="text"
        value={this.state.editText}
        onChange={this.updateText}
        onKeyPress={this.onEnterPress}
        fullWidth
      />
    </ListItem>
  )
  renderAttr(attr : {
            shortDesc: string
          }, isGood : bool) {
    let indicator = null;
    if (isGood) {
      indicator = <TrendingUpIcon />;
    } else {
      indicator = <TrendingDownIcon />;
    }
    return (
      <ListItem key={attr.shortDesc}>
        <ListItemIcon>
          {indicator}
        </ListItemIcon>
        <ListItemText primary={attr.shortDesc} />
      </ListItem>
    );
  }
  render() {
    return (
      <Card>
        <CardHeader title={this.props.title} />
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
            {
              this.props.seeMoreFunc ?
                <ListItem>
                  <Button onClick={this.props.seeMoreFunc}>More</Button>
                </ListItem>
                : null
            }
            {
              this.state.editMode ?
                this.editField()
                : null
            }
          </List>
          {
            this.props.editFunc && !this.state.editMode ? (
              <Button fab color="primary" aria-label="add" onClick={this.launchEdit(true)}>
                <AddIcon />
              </Button>
            ) : null
          }
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
