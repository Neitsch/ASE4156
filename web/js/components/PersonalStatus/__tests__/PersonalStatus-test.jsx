import React from 'react';
import { shallow } from 'enzyme';
import PersonalStatus from '../PersonalStatus';

describe('PersonalStatus', () => {
  it('exists', () => {
    expect(PersonalStatus).toBeTruthy();
  });
  it('renders', () => {
    const comp = shallow((
      <PersonalStatus
        bank={{ balance: 1.0, income: 2.0, outcome: 4.0 }}
        account={{ availableCash: 200.0, totalValue: 100.0, accountName: 'test' }}
      />
    ));
    expect(comp).toMatchSnapshot();
  });
});
