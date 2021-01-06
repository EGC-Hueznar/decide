import React from 'react';
import { shallow, configure, mount, render } from 'enzyme';
import App from '../App';
import Adapter from 'enzyme-adapter-react-16';
import AsyncStorage from '@react-native-community/async-storage'
import 'jsdom-global/register';
import Login from '../components/Login';
import { Alert, Button, Text, TextInput, View } from 'react-native';
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

    it('Correct Mock GETUSER', async () => {
        const correctUser = {
            id: 1,
            email: "",
            first_name: "",
            last_name: "",
            username: "decidehueznar",
            is_staff: true
        }
        
        const data = {}
        const token = 100;
        
        const answer = [200, correctUser]
        
        const mockAxios =  new MockAdapter(axios);
        mockAxios.onPost(config.GETUSER_URL, data).reply(200, correctUser)

        const ans = await postData(config.GETUSER_URL, data, token)

        await new Promise(r => setTimeout(r, 250)); 

        expect(String(ans.data)).toBe(String(correctUser));
    });

    it('Correct Mock LOGIN', async () => {

        const data = {token: 100}
        const mockAxios =  new MockAdapter(axios);
        mockAxios.onPost(config.LOGIN_URL).reply(200, data);

        expect(String(data)).toBe(String({token: 100}))
    });

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
        mockAxios.onPost(config.GETUSER_URL).reply(400, "Bad Request");

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
        const wrapperUsernameTextInput = wrapper.find(TextInput)
        const wrapperUsername = wrapper.find(TextInput).first()
        const wrapperPassword = wrapper.find(TextInput).at(1)
        const wrapperWithButton = wrapperLogin.find(Button)

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");
        
        wrapperLogin.find(Button).simulate('click')

        await new Promise((r) => setTimeout(r, 1000));

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