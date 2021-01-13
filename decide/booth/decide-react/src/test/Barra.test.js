import React from 'react';
import { shallow, mount, configure } from 'enzyme';
import { Button, Text, TextInput } from 'react-native';
import Barra from '../components/Barra';
import Adapter from 'enzyme-adapter-react-16';
import config from '../config.json';
import {postData} from '../utils';
import 'jsdom-global/register';
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";
import { light, dark } from "../styles";
import { string } from 'joi';

//Hide warning
console.error = () => {}

describe('Testing Barra style',() => {

    let wrapper;

    configure({adapter: new Adapter()});

    it('Correct style DecideHueznar text', async () => {
        wrapper = mount(<Barra styles={light} />);

        const wrapperText = wrapper.find(Text).at(0).get(0);
        expect(wrapperText.props.style).toHaveProperty('color', 'white');
    });


    it('Correct style in cambiar tema option', async () => {
        wrapper = mount(<Barra styles={light} />);

        const wrapperText = wrapper.find(Text).at(1).get(0);
        expect(wrapperText.props.style).toHaveProperty('color', 'white');
    });
    
    it('Correct logout style', async () => {
        wrapper = mount(<Barra styles={light} />);
        
        const wrapperText = wrapper.find(Text).at(2).get(0);
        expect(wrapperText.props.style).toHaveProperty('fontSize', 14);
    });

})