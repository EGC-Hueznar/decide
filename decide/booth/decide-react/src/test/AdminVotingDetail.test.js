import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import AdminVotingDetail from '../components/AdminVotingDetail';
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

const setVotingId = () => {};


describe('Testing AdminVotingDetail component',() => {

    let wrapper;
    configure({adapter: new Adapter()});

    it('Render AdminVotingDetail component', () => {
        wrapper = mount(<AdminVotingDetail voting={voting} setVotingId={setVotingId} />);
        const wrapperAdminVotingDetail = wrapper.find(AdminVotingDetail);

        expect(wrapperAdminVotingDetail).toHaveLength(1);
    });

})