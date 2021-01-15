import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import AdminUsers from '../components/AdminUsers';
import { RadioButton } from 'react-native-simple-radio-button';
import { Button, TouchableOpacity, Text } from 'react-native';
import config from '../config.json'
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";

//Hide warning
console.error = () => {}

const setSelectedView = () => {};

describe('Testing AdminUsers component',() => {

    let wrapper;
    configure({adapter: new Adapter()});

    it('Render AdminUsers component', () => {
        wrapper = mount(<AdminUsers setSelectedView={setSelectedView} />);
        const wrapperAdminUsers = wrapper.find(AdminUsers);

        expect(wrapperAdminUsers).toHaveLength(1);
    });

})