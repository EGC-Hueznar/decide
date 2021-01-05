import React from 'react';
import { shallow, configure, mount } from 'enzyme';
import Login from '../components/Login';
import Adapter from 'enzyme-adapter-react-16';
import config from '../config.json';
import * as myFile from '../utils';
import 'jsdom-global/register';
import { onSubmitLogin } from '../components/Login';
jest.useFakeTimers()


describe('Test case for testing login',() => {

    let wrapper;
    
    configure({adapter: new Adapter()});
    it('username check',() => {
        wrapper = shallow(<Login/>);
        const container = wrapper.find('#username');
        wrapper.find('#username').simulate('changeText', 'decidehueznar');


        expect(container.length).toBe(1);
        expect(wrapper.state('form').username).toEqual('decidehueznar');
    });

    it('password check',() => {
        wrapper = shallow(<Login/>);
        wrapper.find('#password').simulate('changeText', 'decidehueznar');

        expect(wrapper.state('form').password).toEqual('decidehueznar');
    })

    it('handleChange check',() => {
        const wrapper = shallow(<Login />)

        const instance = wrapper.instance();
        expect(wrapper.state('form').username).toBe('');
        instance.handleChange('username','user');
        expect(wrapper.state('form').username).toBe('user');
   })

   
})