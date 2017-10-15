import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

function LinearIndeterminate() {
  return (
    <div>
      <CircularProgress size={100} color="primary" />
    </div>
  );
}

export default LinearIndeterminate;
