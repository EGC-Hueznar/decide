import React from 'react';
import { shallow, configure, mount, render } from 'enzyme';
import App from '../App';
import Adapter from 'enzyme-adapter-react-16';
import AsyncStorage from '@react-native-community/async-storage'
import 'jsdom-global/register';
import Login from '../components/Login';
import { Alert, Button, FlatList, Text, TextInput, View } from 'react-native';
import Barra from '../components/Barra';
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";
import config from '../config.json'
import { postData } from '../utils';

// Hide warning
console.error = () => {}

describe('Testing App component',() => {

    let wrapper;
    
    configure({adapter: new Adapter()});

    it('Correct render Login component', () => {
        wrapper = mount(<App />);
        const wrapperLogin = wrapper.find(Login);

        expect(wrapperLogin).toHaveLength(1);
    });

    it('Correct render TextInput component', () => {
        wrapper = mount(<App />);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapperLogin.find(TextInput);

        expect(wrapperUsernameTextInput).toHaveLength(2);
    });

    it('Correct render input username', () => {
        wrapper = mount(<App />);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapperLogin.find(TextInput);
        const wrapperUsername = wrapperUsernameTextInput.first();

        expect(wrapperUsername).toHaveLength(1);
        expect(wrapperUsername.prop('id')).toBe('username');
    });

    it('Correct render input password', () => {
        wrapper = mount(<App />);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapperLogin.find(TextInput);
        const wrapperUsername = wrapperUsernameTextInput.first();
        const wrapperPassword = wrapperUsernameTextInput.at(1);

        expect(wrapperPassword).toHaveLength(1);
        expect(wrapperPassword.prop('id')).toBe('password');
    });
    
    it('Correct render submit button', () => {
        wrapper = mount(<App />);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapperLogin.find(TextInput);
        const wrapperUsername = wrapperUsernameTextInput.first();
        const wrapperPassword = wrapperUsernameTextInput.at(1);
        const wrapperWithButton = wrapperLogin.find(Button);

        expect(wrapperWithButton).toHaveLength(1);
        expect(wrapperWithButton.prop('id')).toBe('button');
    });

    it('Full integration Login test Incorrect', async () => {
        wrapper = mount(<App/>);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapper.find(TextInput)
        const wrapperUsername = wrapper.find(TextInput).first()
        const wrapperPassword = wrapper.find(TextInput).at(1)
        const wrapperWithButton = wrapperLogin.find(Button)

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("contrasenna_erronea");
        
        wrapperLogin.find(Button).simulate('click')

        await new Promise((r) => setTimeout(r, 1000));

        expect(wrapperLogin).toHaveLength(1);
        expect(wrapperUsernameTextInput).toHaveLength(2);
        expect(wrapperUsername).toHaveLength(1);
        expect(wrapperPassword).toHaveLength(1);
        expect(wrapperWithButton).toHaveLength(1);
        
        expect(wrapperLogin.state('form').username).toBe('decidehueznar');
        expect(wrapperLogin.state('form').password).toBe('contrasenna_erronea');
        expect(wrapper.state('signup')).toBe(true);
        expect(wrapperLogin.state('error')).toBe(true);
        expect(wrapper.state('user')).toBeUndefined();
    });  
    
    it('Full integration Login test Correct', async () => {
        wrapper = mount(<App/>);
        const wrapperLogin = wrapper.find(Login);
        const wrapperUsernameTextInput = wrapper.find(TextInput)
        const wrapperUsername = wrapper.find(TextInput).first()
        const wrapperPassword = wrapper.find(TextInput).at(1)
        const wrapperWithButton = wrapperLogin.find(Button)

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");
        
        wrapperLogin.find(Button).simulate('click')

        await new Promise((r) => setTimeout(r, 250));

        expect(wrapperLogin).toHaveLength(1);
        expect(wrapperUsernameTextInput).toHaveLength(2);
        expect(wrapperUsername).toHaveLength(1);
        expect(wrapperPassword).toHaveLength(1);
        expect(wrapperWithButton).toHaveLength(1);

        expect(wrapperLogin.state('form').username).toBe('decidehueznar');
        expect(wrapper.state('signup')).toBe(false);
        expect(wrapperLogin.state('error')).toBe(false);
        expect(wrapper.state('user')).toBeDefined();
    });
})

describe('Testing App methods',() => {

    it('Correct setUser',() => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('user')).toBe(undefined);
        instance.setUser('test');
        expect(wrapper.state('user')).toBe('test');

    });

    it('Correct setToken',() => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('token')).toBe(undefined);
        instance.setToken('AjhdjahDahdjahdajAj');
        expect(wrapper.state('token')).toBe('AjhdjahDahdjahdajAj');

    });

    it('Correct setSignup',() => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('signup')).toBe(true);
        instance.setSignup(false);
        expect(wrapper.state('signup')).toBe(false);

    });

    it('Correct setSelectedVoting', () => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('selectedVoting')).toBe(undefined);
        instance.setSelectedVoting('qwerty');
        expect(wrapper.state('selectedVoting')).toBe('qwerty');
    });

    it('Correct setDone', () => {
        const wrapper = shallow(<App />);

        const instance = wrapper.instance();
        expect(wrapper.state('done')).toBe(false);
        instance.setDone(true);
        expect(wrapper.state('done')).toBe(true);
    });

})

describe('Testing App style',() => {
    
    
    it('Correct "Votaciones disponibles" text style', async () => {
        const correctUser = {
            id: 1,
            email: "",
            first_name: "",
            last_name: "",
            username: "decidehueznar",
            is_staff: true
        }

        const data = {token: 100}
        const mockAxios =  new MockAdapter(axios);
        mockAxios.onPost(config.LOGIN_URL).reply(200, data);
        mockAxios.onPost(config.GETUSER_URL).reply(200, correctUser);

        wrapper = mount(<App/>);
        const wrapperLogin = wrapper.find(Login);

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");

        wrapperLogin.find(Button).simulate('click')
        wrapperText = wrapper.find(Text).at(2).get(0);
        expect(wrapperText.props.style).toHaveProperty('fontSize', 24);
    });


    it('Correct Button style', async () => {
        const correctUser = {
            id: 1,
            email: "",
            first_name: "",
            last_name: "",
            username: "decidehueznar",
            is_staff: true
        }

        const data = {token: 100}
        const mockAxios =  new MockAdapter(axios);
        mockAxios.onPost(config.LOGIN_URL).reply(200, data);
        mockAxios.onPost(config.GETUSER_URL).reply(200, correctUser);

        wrapper = mount(<App/>);
        const wrapperLogin = wrapper.find(Login);

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");

        wrapperLogin.find(Button).simulate('click')
        wrapperButton = wrapper.find(Button);
        expect(wrapperButton.prop('color')).toBe('linear-gradient(top, #049cdb, #0064cd)');
    });
    
    /*
    it('Correct "Votación enviada" font weight', async () => {
        wrapper = mount(<App/>);
        wrapper.instance().setState({signup:false});
        wrapper.instance().setState({selectedVoting:false})
        wrapper.instance().render();
        wrapperText = wrapper.find(Text).at(0);
        expect(wrapper.state('signup')).toBe(false);
        expect(wrapper.state('selectedVoting')).toBe(false);
        expect(wrapperText.props).toBe("500");
    });
    */

    


})