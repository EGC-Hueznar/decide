import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import AddUserForm from '../components/AddUserForm';
import { RadioButton } from 'react-native-simple-radio-button';
import { Button, TouchableOpacity, Text } from 'react-native';
import config from '../config.json'
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";

//Hide warning
console.error = () => {}

const voting = {
    id: 1,
    name: "Voting name",
    desc: "Description",
    question: {
        desc: "Question description",
        options: [{
                number: 1,
                option: "Option 1"
            },
            {
                number: 2,
                option: "Option 2"
            },
            {
                number: 3,
                option: "Option 3"
            }
        ]
    },
    pub_key: {
        p: "100",
        g: "200",
        y: "300"
    },
}

const users = [
        {
        id: 0,
        first_name: "Andrés",
        last_name: "Pérez",
        },
        {
        id: 1,
        first_name: "Paula",
        last_name: "Vigo",
        },
        ];

const enableEditing = () => {};

describe('Testing AddUserForm component',() => {

    let wrapper;
    configure({adapter: new Adapter()});

    it('Render addUserForm component', () => {
        wrapper = mount(<AddUserForm voting={voting} users={users} enableEditing={enableEditing} />);
        const wrapperAddUserForm = wrapper.find(AddUserForm);

        expect(wrapperAddUserForm).toHaveLength(1);
    });

})