// @flow
import React from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from 'material-ui/Dialog';
import Checkbox from 'material-ui/Checkbox';
import { FormGroup, FormControlLabel } from 'material-ui/Form';

type Props = {
  cancel: () => void,
  save: (string, bool) => void,
  errors?: ?Array<Error>,
}
type State = {
  public: bool,
  bucketName: string,
}

export default class EditBucket extends React.Component<Props, State> {
  static propTypes = {
    cancel: PropTypes.func.isRequired,
    save: PropTypes.func.isRequired,
  }
  constructor() {
    super();
    this.state = {
      public: false,
      bucketName: '',
    };
  }
  clickCheckbox = () => this.setState((state, props) => ({
    ...state,
    public: !state.public,
  }))
  bucketNameChange = (e: SyntheticInputEvent<>) => {
    const text = e.target.value;
    this.setState((state, props) => ({
      bucketName: text,
    }));
  }
  save = () => {
    this.props.save(this.state.bucketName, this.state.public);
  }
  render() {
    return (
      <Dialog open onRequestClose={this.props.cancel}>
        <DialogTitle>Subscribe</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Create a new risk bucket that people can invest in
          </DialogContentText>
          {
            this.props.errors ? this.props.errors.map(e => (
              <DialogContentText key={e.message}>{e.message}</DialogContentText>
            )) : null
          }
          <FormGroup row>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Bucket name"
              type="text"
              value={this.state.bucketName}
              onChange={this.bucketNameChange}
              fullWidth
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={this.state.public}
                  onChange={this.clickCheckbox}
                />
              }
              label="Public"
            />
          </FormGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={this.props.cancel} color="primary">
            Cancel
          </Button>
          <Button onClick={this.save} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    );
  }
}
