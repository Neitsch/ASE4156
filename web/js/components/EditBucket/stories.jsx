// @flow
import React from 'react';
import { storiesOf } from '@storybook/react';
import EditBucket from './EditBucket';
import { action } from '@storybook/addon-actions';

storiesOf('EditBucketDontTest', module).add('Playground', () => (
  <EditBucket save={action('save')} cancel={action('cancel')} />
));
