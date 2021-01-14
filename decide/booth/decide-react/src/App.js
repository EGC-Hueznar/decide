import React from 'react';
import Barra from './components/Barra';
import Login from './components/Login';
import Admin from './components/Admin';
import Voting from './components/Voting';
import {StatusBar, FlatList, Text, TouchableOpacity, View, SafeAreaView} from 'react-native';
import axios from 'axios';
import config from './config.json';
import { postData } from './utils';
import AsyncStorage from '@react-native-community/async-storage'
import { light, dark } from "./styles";


class App extends React.Component {

    state = {
        user: undefined,
        selectedVoting: undefined,
        token: undefined,
        votings: [],
        signup: true,
        done:false,
        styles: 'light'
    }

    setStyles = () => {
        this.setState({styles : this.state.styles === 'light' ? 'dark' : 'light'});
    }

    init = () => {
        this.clearStorage()
        this.handleGetStorage('decide')        
    }

    //Sustituye a la gestión de las cookies
    handleSetStorage = (key, value) => {
        AsyncStorage.setItem(key, value)
    }

    //Sustituye a la gestión de las cookies. Actualiza el estado
    handleGetStorage = (key) => {
        return AsyncStorage.getItem(key).then((decide) =>{
            if (decide != null && decide != ""){
                this.setToken(decide)
                this.getUser(decide);
            }
        });
    }

    clearStorage = () => {
        AsyncStorage.clear
    }

    
    //Get User para la alternativa a las cookies
    getUser = (tokenStorage) => {
        const token = tokenStorage

        const data = {
            token
        };
        postData(config.GETUSER_URL, data, token)
            .then(response => {
                this.setUser(response.data);
                this.setSignup(false);
            }).catch(error => {
                alert(`Error: ${error}`);
            });
    }

    setUser = (user) => {
        const oldUserValue = this.state.user;
        this.setState({user});
        
        // Actualizar votings
        if (user && oldUserValue !== user) {
            this.loadVotings();
        } else if (!user) {
            this.setState({votings: []})
        }
    }

    setToken = (token2) =>  {
        this.setState({token:token2});
    }

    setSignup = (signup2) =>  {
        this.setState({signup:signup2});
    }

    setSelectedVoting = (voting) => {
        this.setState({selectedVoting: voting});
    }

    setDone = (done2) => {
        this.setState({done:done2});
    }

    loadVotings = () => {
        this.setDone(false)
        axios.get(`${config.CENSUS_VOTINGS_URL}${this.state.user.id}/`).then(response => {
            const votings = response.data.votings;
            axios.get(config.VOTING_URL).then(response => {
                this.setState({votings: response.data.filter(v => votings.includes(v.id) 
                    && v.start_date 
                    && Date.parse(v.start_date) < Date.now() 
                    && !v.end_date)});
            });
        });

    }

    componentDidMount() {
        this.init();
        this.render();
    }

    render_voting = ({item}) => {
        const styles = this.state.styles === 'light' ? light : dark;
        return <TouchableOpacity onPress={() => this.setSelectedVoting(item)} disabled={!item.start_date}>
        <View style={styles.item}><Text style={styles.sectionHeader}>{item.name}</Text></View></TouchableOpacity>}

    render() {
        const statusHeight = StatusBar.currentHeight ? StatusBar.currentHeight : 0;

        const styles = this.state.styles === 'light' ? light : dark;

        return(
            <View style={styles.parent}>
                <Barra styles={styles} toggleTheme={this.setStyles} urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup} token={this.state.token} setToken={this.setToken} setUser={this.setUser} handleSetStorage={this.handleSetStorage}/>
                

                                {this.state.signup ? 
                                    <Login styles={styles} setUser={this.setUser} setToken={this.setToken} setSignup={this.setSignup} token={this.state.token} handleSetStorage={this.handleSetStorage}/>
                                    : 
                                    (this.state.user.is_staff ? (<Admin votings={this.state.votings}/>) : (!this.state.selectedVoting ?
                                        <View>
                                            <View View style={styles.html}>
                                                <View View style={styles.body}>
                                                    <View View style={styles.container}>
                                                        <View View style={styles.content}>
                                                          <Text style={styles.title}>Votaciones disponibles</Text>
                                                            {this.state.done == true &&  <View style={{width: '100%', //Si la votación se ha realizado se muestra la barra verde.
                                                                backgroundColor: '#00D090',
                                                                paddingHorizontal: 20,
                                                                paddingTop: 20,
                                                                paddingBottom: 20,
                                                                marginBottom: 20}}>
                                                                    <Text style={{fontSize:16}}>¡Votación enviada!</Text>
                                                            </View>}
                                                            <SafeAreaView style={styles.containerList}>
                                                                    <FlatList style={styles.item} data={this.state.votings} renderItem={this.render_voting} />
                                                            </SafeAreaView>
                                                            <TouchableOpacity style={styles.btnprimary} onPress={this.onSubmitLogin}>
                                                                <Text style={{color:"#fff", textAlign:'center'}}>Recargar</Text>
                                                            </TouchableOpacity>
                                                        </View>
                                                    </View>
                                                </View>
                                            </View>
                                        </View> :
                                        <Voting styles={styles} setDone={this.setDone} voting={this.state.selectedVoting} user={this.state.user} token={this.state.token} resetSelected={() => this.setSelectedVoting(undefined)}/> )

                                    )
                                }

  
            </View>
);
    }
}

export default App;
