import React from 'react';
import { shallow } from 'enzyme';
import EditBucket from '../EditBucket.jsx';

describe('EditBucket', () => {
  it('exists', () => {
    expect(EditBucket).toBeTruthy();
  });

  it('renders', () => {
    const cancelFn = jest.fn();
    const saveFn = jest.fn();
    const editBucket = shallow(<EditBucket cancel={cancelFn} save={saveFn} />);
    expect(editBucket).toMatchSnapshot();
    expect(cancelFn.mock.calls.length).toBe(0);
    editBucket.find('#cancel').simulate('click');
    expect(cancelFn.mock.calls.length).toBe(1);
    editBucket.find('#name').simulate('change', { target: { value: 'bucket' } });
    editBucket.find('#investment').simulate('change', { target: { value: '200.00' } });
    expect(editBucket).toMatchSnapshot();
    expect(saveFn.mock.calls.length).toBe(0);
    editBucket.find('#save').simulate('click');
    expect(saveFn.mock.calls.length).toBe(1);
    expect(saveFn.mock.calls[0]).toEqual(['bucket', false, 200.0]);
  });

  it('displays error', () => {
    const cancelFn = jest.fn();
    const saveFn = jest.fn();
    const editBucket = shallow(<EditBucket cancel={cancelFn} save={saveFn} errors={[Error('messed up')]} />);
    expect(editBucket).toMatchSnapshot();
  });
});
