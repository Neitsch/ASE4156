/* @lazyspec (remove to manage manually) */
/* eslint-disable */
import PersonalStatus from '../PersonalStatus.jsx';

import React from 'react';
import { shallow } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';
import fakeProps from 'react-fake-props';

describe('PersonalStatus', () => {
  it('exists', () => {
    expect(PersonalStatus).toBeTruthy();
  });

  it('renders', () => {
    const props = fakeProps('web/js/components/PersonalStatus/PersonalStatus.jsx');
    console.log(props);
    const comp = <PersonalStatus {...props} />;
    const wrapper = shallow(comp);
    expect(shallowToJson(wrapper)).toMatchSnapshot();
  });
});
