import React from 'react';
import { shallow, configure } from 'enzyme';
import { View, Text, TextInput } from 'react-native';
import Login from '../components/Login';
import Adapter from 'enzyme-adapter-react-16';
import config from '../config.json';
import {postData} from '../utils';
import 'jsdom-global/register';
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";
import { light, dark } from "../styles";

//Hide warning
console.error = () => {}




describe('Test case for testing login',() => {

    let wrapper;
    
    configure({adapter: new Adapter()});
    it('username check',() => {
        wrapper = shallow(<Login styles={light}/>);
        const container = wrapper.find('#username');
        wrapper.find('#username').simulate('changeText', 'decidehueznar');


        expect(container.length).toBe(1);
        expect(wrapper.state('form').username).toEqual('decidehueznar');
    });

    it('password check',() => {
        wrapper = shallow(<Login styles={light}/>);
        wrapper.find('#password').simulate('changeText', 'decidehueznar');

        expect(wrapper.state('form').password).toEqual('decidehueznar');
    })

    it('handleChange check',() => {
        const wrapper = shallow(<Login styles={light}/>)

        const instance = wrapper.instance();
        expect(wrapper.state('form').username).toBe('');
        instance.handleChange('username','user');
        expect(wrapper.state('form').username).toBe('user');
   })


    
    describe('login', () => {
        let wrapper;
        configure({adapter: new Adapter()});

        it('Correct getUser', async () => {
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
                await new Promise(r => setTimeout(r, 250)); 
                expect(String(ans.data)).toBe(String(correctUser));
        })


        it('Incorrect getUser', async () => {
            const wrapper = shallow(<Login styles={light}/>)                
            const mockAxios =  new MockAdapter(axios);
            mockAxios.onPost(config.GETUSER_URL).reply(400);                 
            await wrapper.instance().getUser()
            await new Promise(r => setTimeout(r, 250)); 
            expect(wrapper.state('error')).toBe(true);
        })


        it('Correct submitLogin', async () => {
            const correctUser = {
                    token: '100'
                }
                
                const data = {
                    username: 'decidehueznar',
                    password: 'decidehueznar'
                }
                const mockAxios =  new MockAdapter(axios);
                mockAxios.onPost(config.LOGIN_URL, data).reply(200, correctUser)
                const ans = await postData(config.LOGIN_URL, data)
                await new Promise(r => setTimeout(r, 250)); 
                await new Promise(r => setTimeout(r, 250)); 
                expect(String(ans.data)).toBe(String(correctUser));
        })
        
        it('Incorrect submitLogin', async () => {
            const wrapper = shallow(<Login styles={light}/>)                
            const mockAxios =  new MockAdapter(axios);
            mockAxios.onPost(config.LOGIN_URL).reply(400);                 
            await wrapper.instance().onSubmitLogin()
            await new Promise(r => setTimeout(r, 250)); 
            expect(wrapper.state('error')).toBe(true);
        })
    });
   
})

describe('Testing Login style',() => {
    

    it('Correct "Usuario" text ligth style', async () => {
        wrapper = shallow(<Login styles={light}/>);
        wrapperText = wrapper.find(Text).at(0).get(0);
        expect(wrapperText.props.style).toHaveProperty('fontSize', 24);
    });

    it('Correct "Contraseña" text ligth style', async () => {
        wrapper = shallow(<Login styles={light}/>);
        wrapperText = wrapper.find(Text).at(1).get(0);
        expect(wrapperText.props.style).toHaveProperty('fontSize', 24);
    });

    it('Correct "Usuario" text dark style', async () => {
        wrapper = shallow(<Login styles={dark}/>);
        wrapperText = wrapper.find(Text).at(0).get(0);
        expect(wrapperText.props.style).toHaveProperty('color', 'white');
    });

    it('Correct "Contraseña" text dark style', async () => {
        wrapper = shallow(<Login styles={dark}/>);
        wrapperText = wrapper.find(Text).at(1).get(0);
        expect(wrapperText.props.style).toHaveProperty('color', 'white');
    });

    it('Correct "Login" text style', async () => {
        wrapper = shallow(<Login styles={light}/>);
        wrapperText = wrapper.find(Text).at(2);
        expect(wrapperText.prop('style')).toHaveProperty('color', '#fff');
    });

    it('Correct "Usuario" text input style', async () => {
        wrapper = shallow(<Login styles={light}/>);
        wrapperTextInput = wrapper.find(TextInput).at(0).get(0);
        expect(wrapperTextInput.props.style).toHaveProperty('fontSize', 15);
    });

    it('Correct "Contraseña" text input style', async () => {
        wrapper = shallow(<Login styles={light}/>);
        wrapperTextInput = wrapper.find(TextInput).at(1).get(0);
        expect(wrapperTextInput.props.style).toHaveProperty('fontSize', 15);
    });

    it('Correct "Button" style', async () => {
        wrapper = shallow(<Login styles={light}/>);
        wrapperButton = wrapper.find('#button');
        expect(wrapperButton.prop('style')).toHaveProperty('backgroundColor', '#0064cd');
    });

    it('Correct dark background style', async () => {
        wrapper = shallow(<Login styles={dark}/>);
        wrapperButton = wrapper.find(View).at(2);
        expect(wrapperButton.prop('style')).toHaveProperty('backgroundColor', '#1f1f1f');
    });
})