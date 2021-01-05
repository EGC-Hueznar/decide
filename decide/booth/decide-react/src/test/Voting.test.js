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

    it('Correct change question select state', () => {
        wrapper = mount(<Voting voting={correctVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const radioButtons = wrapper.find(RadioButton);

        const opt1 = radioButtons.at(0).props();
        opt1.onPress(opt1.obj.value);
        expect(wrapper.state().selected).toBe(voting.question.options[0].number);

        const opt2 = radioButtons.at(1).props();
        opt2.onPress(opt2.obj.value);
        expect(wrapper.state().selected).toBe(voting.question.options[1].number);

        const opt3 = radioButtons.at(2).props();
        opt3.onPress(opt3.obj.value);
        expect(wrapper.state().selected).toBe(voting.question.options[2].number);
    });

    it('Store vote for non-existent voting', async () => {
        wrapper = mount(<Voting voting={nonExistentVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const radioButtons = wrapper.find(RadioButton);
        const submitButton = wrapper.find(Button).first();
        
        const opt1 = radioButtons.at(0).props();
        opt1.onPress(opt1.obj.value);
        submitButton.simulate("click")
    
        await new Promise(r => setTimeout(r, 250)); 

        expect(wrapper.state().error).not.toBe(false);
    });

    it('Store vote without selecting option', async () => {   
        wrapper = mount(<Voting voting={correctVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const submitButton = wrapper.find(Button).first();
        submitButton.props().onPress();

        expect(wrapper.state().noSelection).toBe(true);
    });

    it('Store valid vote', async () => {      
        wrapper = mount(<Voting voting={correctVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const radioButtons = wrapper.find(RadioButton);
        const submitButton = wrapper.find(Button).first();
        
        const opt1 = radioButtons.at(0).props();
        opt1.onPress(opt1.obj.value);
        submitButton.simulate("click")
    
        await new Promise(r => setTimeout(r, 250));

        expect(wrapper.state().error).toBe(false);
    });

    it('Store vote of closed voting', async () => {     
        wrapper = mount(<Voting voting={closedVoting} user={user} setDone={setDone} resetSelected={resetSelected} />);
        const radioButtons = wrapper.find(RadioButton);
        const submitButton = wrapper.find(Button).first();
        
        const opt1 = radioButtons.at(0).props();
        opt1.onPress(opt1.obj.value);
        submitButton.simulate("click")
    
        await new Promise(r => setTimeout(r, 250));

        expect(wrapper.state().error).not.toBe(false);
    });


})

