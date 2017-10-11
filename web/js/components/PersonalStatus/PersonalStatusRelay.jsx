// @flow
import PersonalStatus from './PersonalStatus';
import { createFragmentContainer, graphql } from 'react-relay';

export default createFragmentContainer(PersonalStatus, {
  bank: graphql`
    fragment PersonalStatusRelay_bank on GUserBank {
      balance
      income
      outcome
    }
` });
