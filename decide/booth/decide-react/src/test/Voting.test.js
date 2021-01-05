import React from 'react';
import { configure, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import Voting from '../components/Voting';
import { RadioButton } from 'react-native-simple-radio-button';
import { Button } from 'react-native';
import config from '../config.json'
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";

// Hide warning
console.error = () => {}

// Mocking
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

const correctVoting = {...voting, id:1}
const nonExistentVoting = {...voting, id:2}
const closedVoting = {...voting, id:3}
const user = {
    id: 1
};
const setDone = () => {};
const resetSelected = () => {}

const mockAxios =  new MockAdapter(axios);
mockAxios.onPost(config.STORE_URL).reply(config => {
    const data = JSON.parse(config.data);
    switch (data.voting) {
        case correctVoting.id:
            return [200, correctVoting];
        case nonExistentVoting.id:
            return [404, {msg: "Not found"}];
        case closedVoting.id:
            return [403, {msg: "Forbidden. Voting closed"}]
        default:
            return [500, {msg: "An error ocurred"}]
    }
});


describe('Testing Voting component',() => {

    let wrapper;
    configure({adapter: new Adapter()});

    it('Render voting component', () => {
        wrapper = mount(<Voting voting={correctVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const wrapperVoting = wrapper.find(Voting);

        expect(wrapperVoting).toHaveLength(1);
    });

    it('Render questions', async () => {
        wrapper = mount(<Voting voting={correctVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const radioButtons = wrapper.find(RadioButton);
        
        expect(radioButtons).toHaveLength(3);
    });

})

