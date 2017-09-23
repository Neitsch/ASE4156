/* @lazyspec (remove to manage manually) */
/* eslint-disable */
import AppBar from '../AppBar.jsx';

import React from 'react';
import { shallow } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

describe('AppBar', () => {
  it('exists', () => {
    expect(AppBar).toBeTruthy();
  });

  it('renders', () => {
    const comp = <AppBar  />;
    const wrapper = shallow(comp);
    expect(shallowToJson(wrapper)).toMatchSnapshot();
  });
});
