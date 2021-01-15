import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import AdminVotings from '../components/AdminVotings';
import { RadioButton } from 'react-native-simple-radio-button';
import { Button, TouchableOpacity, Text } from 'react-native';
import config from '../config.json'
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";

//Hide warning
console.error = () => {}

const votings = {
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
    id: 2,
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

const setSelectedView = () => {};

describe('Testing AdminVotings component',() => {

    let wrapper;
    configure({adapter: new Adapter()});

    it('Render AdminVotings component', () => {
        wrapper = mount(<AdminVotings votings={votings} setSelectedView={setSelectedView} />);
        const wrapperAdminVotings = wrapper.find(AdminVotings);

        expect(wrapperAdminVotings).toHaveLength(1);
    });

})