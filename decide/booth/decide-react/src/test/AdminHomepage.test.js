import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import AdminHomepage from '../components/AdminHomepage';
import { RadioButton } from 'react-native-simple-radio-button';
import { Button, TouchableOpacity, Text } from 'react-native';
import config from '../config.json'
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";

//Hide warning
console.error = () => {}

const setSelectedView = () => {};

describe('Testing AdminHomepage component',() => {

    let wrapper;
    configure({adapter: new Adapter()});

    it('Render AdminHomepage component', () => {
        wrapper = mount(<AdminHomepage setSelectedView={setSelectedView} />);
        const wrapperAdminHomepage = wrapper.find(AdminHomepage);

        expect(wrapperAdminHomepage).toHaveLength(1);
    });

})