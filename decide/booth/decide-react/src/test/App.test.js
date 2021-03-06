import React from 'react';
import { shallow, configure, mount, render } from 'enzyme';
import App from '../App';
import Adapter from 'enzyme-adapter-react-16';
import AsyncStorage from '@react-native-community/async-storage'
import 'jsdom-global/register';
import Login from '../components/Login';
import { Alert, Button, FlatList, Text, TextInput, TouchableOpacity, View } from 'react-native';
import Barra from '../components/Barra';
import axios from 'axios';
import MockAdapter from "axios-mock-adapter";
import config from '../config.json'
import { postData } from '../utils';
import { light, dark } from "../styles";

// Hide warning
console.error = () => {}

describe('Testing AsyncStorage methods',() => {
    
    //Mockeamos las llamadas externas de AsyncStorage
    jest.mock('@react-native-community/async-storage', () => ({
        AsyncStorage: {
            setItem: jest.fn(),
            getItem: jest.fn(),
            clear: jest.fn(),
          }
    }));

    //Probamos si handleSetStorage llama al metodo setItem de AsyncStorage
    it('check if setItem in AsyncStorage is called through handleSetStorage', async () => {
        let wrapper = shallow(<App/>)

        await wrapper.instance().handleSetStorage('testing','testing')
        
        expect(AsyncStorage.setItem).toBeCalledWith('testing','testing')

        wrapper.unmount()
    });

    //Probamos si handleGetStorage llama al metodo setItem de AsyncStorage
    it('check if getItem in AsyncStorage is called through handleGetStorage', async () => {
        let wrapper = shallow(<App/>)

        await wrapper.instance().handleGetStorage('testing')
        
        expect(AsyncStorage.getItem).toBeCalledWith('testing')

        wrapper.unmount()
    });
})

describe('mocking handleGetStorage', () => {

    it('handleGetStorage setted token', async () =>{
        AsyncStorage.getItem.mockResolvedValueOnce('Valor de prueba para mock')
        const getItemSpy = jest.spyOn(AsyncStorage, 'getItem')
        const componentDidMountSpy = jest.spyOn(App.prototype, 'componentDidMount')
        
        const wrapper = await shallow(<App/>)

        expect(getItemSpy).toHaveBeenCalled()
        expect(componentDidMountSpy).toHaveBeenCalledTimes(1)
        expect(wrapper.state('token')).toBe('Valor de prueba para mock')

        wrapper.unmount()
    })

    it('handleGetStorage did not set token with null value', async () =>{

        const wrapper1 = await shallow(<App/>)

        //Por defecto está a indefinido
        expect(wrapper1.state('token')).toBe(undefined)

        wrapper1.unmount()

        AsyncStorage.getItem.mockResolvedValueOnce('')
        const getItemSpy = jest.spyOn(AsyncStorage, 'getItem')
        
        const wrapper2 = await shallow(<App/>)

        expect(getItemSpy).toHaveBeenCalled()
        expect(wrapper2.state('token')).toBe(undefined)

        wrapper2.unmount()
    })

})

describe('componentDidMount call other methods',() =>{

    //Comprueba si se llama a componentDidMount al montar App
    it('componentDidMount called at mounted', () =>{

        const componentDidMountSpy = jest.spyOn(App.prototype, 'componentDidMount')

        let wrapper = mount(<App/>)

        expect(componentDidMountSpy).toBeCalled()
        
    })

    //Comprueba si al llamar a componentDidMount ejecuta las funciones que se esperan
    it('Should call functions during componentDidMount', async () =>{
        let wrapper = mount(<App/>) 

        const instance = wrapper.instance()


        const initSpy = jest.spyOn(instance,'init')
        const stylesGetSpy = jest.spyOn(instance,'styleGetStorage')
        const handleGetSpy = jest.spyOn(instance,'handleGetStorage')

        instance.componentDidMount()

        expect(initSpy).toHaveBeenCalled()
        expect(stylesGetSpy).toHaveBeenCalled()
        expect(handleGetSpy).toHaveBeenCalled()
    })

    //Comprueba que, si no se llama a componentDidMount las funciones no se ejecutan
    it('Check if expected methods are not called by componentDidMount', async () =>{
        let wrapper = shallow(<App/>)
    
        let instance = wrapper.instance()
    
        const initSpy = jest.spyOn(instance,'init')
        const stylesGetSpy = jest.spyOn(instance,'styleGetStorage')
        const handleGetSpy = jest.spyOn(instance,'handleGetStorage')
        
        expect(initSpy).toBeCalledTimes(0)
        expect(stylesGetSpy).toBeCalledTimes(0)
        expect(handleGetSpy).toBeCalledTimes(0)
    
    })
})

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
        const wrapperWithButton = wrapperLogin.find(TouchableOpacity);

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
        const wrapperWithButton = wrapperLogin.find(TouchableOpacity)

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("contrasenna_erronea");
        
        wrapperLogin.find(TouchableOpacity).simulate('click')

        await new Promise((r) => setTimeout(r, 2000));

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
        const wrapperWithButton = wrapperLogin.find(TouchableOpacity)

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");
        
        wrapperLogin.find(TouchableOpacity).simulate('click')

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

describe('Testing App methods',() => {

    it('Correct setUser',() => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('user')).toBe(undefined);
        instance.setUser('test');
        expect(wrapper.state('user')).toBe('test');

    });

    it('Correct setToken',() => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('token')).toBe(undefined);
        instance.setToken('AjhdjahDahdjahdajAj');
        expect(wrapper.state('token')).toBe('AjhdjahDahdjahdajAj');

    });

    it('Correct setSignup',() => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('signup')).toBe(true);
        instance.setSignup(false);
        expect(wrapper.state('signup')).toBe(false);

    });

    it('Correct setSelectedVoting', () => {
        const wrapper = shallow(<App />)

        const instance = wrapper.instance();
        expect(wrapper.state('selectedVoting')).toBe(undefined);
        instance.setSelectedVoting('qwerty');
        expect(wrapper.state('selectedVoting')).toBe('qwerty');
    });

    it('Correct setDone', () => {
        const wrapper = shallow(<App />);

        const instance = wrapper.instance();
        expect(wrapper.state('done')).toBe(false);
        instance.setDone(true);
        expect(wrapper.state('done')).toBe(true);
    });


    it('Correct setStyles', () => {
        const wrapper = shallow(<App />);

        const instance = wrapper.instance();
        expect(wrapper.state('styles')).toBe('light');
        instance.setStyles('dark')
        expect(wrapper.state('styles')).toBe('dark')
    })

})

describe('Testing App style',() => {
    
    
    it('Correct "Votaciones disponibles" text style', async () => {
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

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");

        wrapperLogin.find(TouchableOpacity).simulate('click')
        wrapperText = wrapper.find(Text).at(2).get(0);
        expect(wrapperText.props.style).toHaveProperty('fontSize', 24);
    });


    it('Correct Button style', async () => {
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

        const usernameForm = wrapperLogin.find(TextInput).at(0);
        usernameForm.props()["onChangeText"]("decidehueznar");

        const passwordForm = wrapperLogin.find(TextInput).at(1);
        passwordForm.props()["onChangeText"]("decidehueznar");

        wrapperLogin.find(TouchableOpacity).simulate('click')
        wrapperButton = wrapper.find(TouchableOpacity).at(1);
        expect(wrapperButton.prop("style").backgroundColor).toBe("#0064cd");
    });


    
    it('Correct Mock loadVotings', async () => {
        correctVoting = [1,2,3]
        
        const mockAxios =  new MockAdapter(axios);
        mockAxios.onGet(`${config.CENSUS_VOTINGS_URL}1/`).reply(200, correctVoting)

        const ans = await axios.get(`${config.CENSUS_VOTINGS_URL}1/`)

        await new Promise(r => setTimeout(r, 250)); 
        expect(String(ans.data)).toBe(String(correctVoting));
    });


    it('Correct Mock loadVotings2', async () => {
    
    const votings = [{
    id: 2,
    name: "Vote2",
    desc: "Esta es una descripción de prueba creada para ver como queda el texto de la descripción",
    question: {
        desc:"Color favorito",
        options:[{
                number:1,
                option:"Rojo"
            },
            {
                number:2,
                option:"Amarillo"
            },
            {
                number:3,
                option:"Cyan (Azul)"
            },
            {
                number:4,
                option:"Otro"
            }
        ]
    },
    pub_key: {
        p:"1.0779545050313737e+77",
        g:"4.238427403087084e+76",
        y:"5.270561551615331e+76"
    },
    start_date:"2021-01-12T12:08:28.469991Z",
    end_date:null,
    auths:[{
            name:"test",
            url:"http://localhost:8000",
            me:true
        }
    ],
    tally:null,
    postproc:null},
    {   
    id: 1,
    name: "Votacion",
    desc: "",
    question: {
        desc:"Color favorito",
        options:[{
                number:1,
                option:"Rojo"
            },
            {
                number:2,
                option:"Amarillo"
            },
            {
                number:3,
                option:"Cyan (Azul)"
            },
            {
                number:4,
                option:"Otro"
            }
        ]
    },
    pub_key: {
        p:"8.029228140198205e+76",
        g:"3.235761470093718e+76",
        y:"6.818583710286106e+76"
    },
    start_date:"2021-01-12T12:08:28.487695Z",
    end_date:null,
    auths:[{
            name:"test",
            url:"http://localhost:8000",
            me:true
        }
    ],
    tally:null,
    postproc:null},
    {   
        id: 3,
        name: "Test3",
        desc: "Prueba",
        question: {
            desc:"Color favorito",
            options:[{
                    number:1,
                    option:"Rojo"
                },
                {
                    number:2,
                    option:"Amarillo"
                },
                {
                    number:3,
                    option:"Cyan (Azul)"
                },
                {
                    number:4,
                    option:"Otro"
                }
            ]
        },
        pub_key: {
            p:"6.178616200531794e+76",
            g:"5.5132376062826775e+76",
            y:"5.59174128989179e+76"
        },
        start_date:"2021-01-12T12:20:07.065776Z",
        end_date:null,
        auths:[{
                name:"test2",
                url:"http://localhost:8000",
                me:false
            }
        ],
        tally:null,
        postproc:null}

]
        
    const mockAxios =  new MockAdapter(axios);
    mockAxios.onGet(config.VOTING_URL).reply(200, votings)

    const ans = await axios.get(config.VOTING_URL)

    await new Promise(r => setTimeout(r, 250)); 
    expect(String(ans.data)).toBe(String(votings));
    });


    it('Correct Mock loadVotings4', async () => {
    
        const wrapper = shallow(<App />);

        const votingsTest = [{
        
        id: 2,
        name: "Vote2",
        desc: "Esta es una descripción de prueba creada para ver como queda el texto de la descripción",
        question: {
            desc:"Color favorito",
            options:[{
                    number:1,
                    option:"Rojo"
                },
                {
                    number:2,
                    option:"Amarillo"
                },
                {
                    number:3,
                    option:"Cyan (Azul)"
                },
                {
                    number:4,
                    option:"Otro"
                }
            ]
        },
        pub_key: {
            p:"1.0779545050313737e+77",
            g:"4.238427403087084e+76",
            y:"5.270561551615331e+76"
        },
        start_date:"2021-01-12T12:08:28.469991Z",
        end_date:null,
        auths:[{
                name:"test",
                url:"http://localhost:8000",
                me:true
            }
        ],
        tally:null,
        postproc:null},
        {   
        id: 1,
        name: "Votacion",
        desc: "",
        question: {
            desc:"Color favorito",
            options:[{
                    number:1,
                    option:"Rojo"
                },
                {
                    number:2,
                    option:"Amarillo"
                },
                {
                    number:3,
                    option:"Cyan (Azul)"
                },
                {
                    number:4,
                    option:"Otro"
                }
            ]
        },
        pub_key: {
            p:"8.029228140198205e+76",
            g:"3.235761470093718e+76",
            y:"6.818583710286106e+76"
        },
        start_date:"2021-01-12T12:08:28.487695Z",
        end_date:null,
        auths:[{
                name:"test",
                url:"http://localhost:8000",
                me:true
            }
        ],
        tally:null,
        postproc:null},
        {
        id: 3,
        name: "Test3",
        desc: "Prueba",
        question: {
            desc:"Color favorito",
            options:[{
                    number:1,
                    option:"Rojo"
                },
                {
                    number:2,
                    option:"Amarillo"
                },
                {
                    number:3,
                    option:"Cyan (Azul)"
                },
                {
                    number:4,
                    option:"Otro"
                }
            ]
        },
        pub_key: {
            p:"6.178616200531794e+76",
            g:"5.5132376062826775e+76",
            y:"5.59174128989179e+76"
        },
        start_date:"2021-01-12T12:20:07.065776Z",
        end_date:null,
        auths:[{
                name:"test2",
                url:"http://localhost:8000",
                me:false
            }
        ],
        tally:null,
        postproc:null}]
        
    correctVoting = {votings:[1,2]}

    const mockAxios =  new MockAdapter(axios);
    
    mockAxios.onGet(config.VOTING_URL).reply(200, votingsTest)
    mockAxios.onGet(`${config.CENSUS_VOTINGS_URL}1/`).reply(200, correctVoting)

    const instance = wrapper.instance()
    const user = {id:1}

    await instance.setState({user:user})    
    await instance.loadVotings()

    await new Promise(r => setTimeout(r, 250));

    expect(instance.state.votings).toHaveLength(2);
    });

})