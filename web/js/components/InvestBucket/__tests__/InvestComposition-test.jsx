import React from 'react';
import { shallow } from 'enzyme';
import InvestComposition from '../InvestComposition';

describe('InvestComposition', () => {
  it('exists', () => {
    expect(InvestComposition).toBeTruthy();
  });

  it('render', () => {
    const comp = shallow(<InvestComposition
      chunks={[]}
      total={0.0}
      chunkUpdate={jest.fn()}
      suggestionFieldChange={jest.fn()}
      suggestions={[]}
      saveFunc={jest.fn()}
      cancelFunc={jest.fn()}
    />);
    expect(comp).toMatchSnapshot();
  });

  it('add stock', () => {
    const suggestionFieldChange = jest.fn();
    const comp = shallow(<InvestComposition
      chunks={[]}
      total={0.0}
      chunkUpdate={jest.fn()}
      suggestionFieldChange={suggestionFieldChange}
      suggestions={[{ id: 1, name: 'AAA', value: 3 }]}
      saveFunc={jest.fn()}
      cancelFunc={jest.fn()}
    />);
    expect(suggestionFieldChange.mock.calls.length).toEqual(0);
    comp.find('#select-stock').simulate('change', { target: { value: 'AAA' } });
    expect(suggestionFieldChange.mock.calls.length).toEqual(1);
    expect(comp).toMatchSnapshot();
    comp.find('#add-stock').simulate('click');
    expect(comp).toMatchSnapshot();
  });
});
