import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

const styles = {
  root: {
    width: '100%',
    marginTop: '23%',
    marginLeft: '45%',
  },
  loading: {
    color: '#FFFF00',
  },
};

function LinearIndeterminate(props) {
  const { classes } = props;
  return (
    <div className={classes.root} >
      <CircularProgress size={100} color="primary" />
    </div>
  );
}

LinearIndeterminate.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(LinearIndeterminate);
