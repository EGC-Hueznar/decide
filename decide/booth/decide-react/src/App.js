import React from 'react';
import Barra from './components/Barra';
import Login from './components/Login';
import Voting from './components/Voting';
import {StatusBar, FlatList, Text, TouchableOpacity, View, SafeAreaView} from 'react-native';
import axios from 'axios';
import config from './config.json';
import { postData } from './utils';
import AsyncStorage from '@react-native-community/async-storage'
import { StyleSheet} from "react-native";
import * as JSONbig from "json-bigint";


class App extends React.Component {

    state = {
        user: undefined,
        selectedVoting: undefined,
        token: undefined,
        votings: [],
        signup: true,
        done:false
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
        axios.get(`${config.CENSUS_VOTINGS_URL}${this.state.user.id}`).then(response => {
            const votings = response.data.votings;
            
            axios.get(config.VOTING_URL, {
              transformResponse: res => JSONbig.parse(res)
            }).then(response => { 
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

    render_voting = ({item}) => <TouchableOpacity onPress={() => this.setSelectedVoting(item)} disabled={!item.start_date}>
        <View View style={styles.item}><Text style={styles.sectionHeader}>{item.name}</Text></View></TouchableOpacity>

    render() {
        const statusHeight = StatusBar.currentHeight ? StatusBar.currentHeight : 0;

        return(
            <View style={styles.parent}>
                <Barra urlLogout={this.state.urlLogout} signup={this.state.signup} setSignup={this.setSignup} token={this.state.token} setToken={this.setToken} setUser={this.setUser} handleSetStorage={this.handleSetStorage}/>
                

                                {this.state.signup ? 
                                    <Login setUser={this.setUser} setToken={this.setToken} setSignup={this.setSignup} token={this.state.token} handleSetStorage={this.handleSetStorage}/>
                                    : 
                                    (!this.state.selectedVoting ? 
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
                                                                <Text style={{color:"#fff"}}>Recargar</Text>
                                                            </TouchableOpacity>
                                                        </View>
                                                    </View>
                                                </View>
                                            </View>
                                        </View> :
                                        <Voting setDone={this.setDone} voting={this.state.selectedVoting} user={this.state.user} token={this.state.token} resetSelected={() => this.setSelectedVoting(undefined)}/> )
                                }
  
            </View>);
    }
}


const styles = StyleSheet.create({
    html: {
        margin: 0,
        padding: 0,
    },
    body: {
        margin: 0,
        padding: 0,
        fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
        fontSize: 18,
        fontWeight: 'normal',
        lineHeight: 24,
        display: 'flex',
        alignItems: 'center',
        alignContent: 'center',
        backgroundColor: '#fff',
    },
    container: {
        width: '100%',
        maxWidth: 960,
        justifyContent: 'center',
        alignItems: 'center',
    },
    content: {
        width: '100%',
        borderRadius: 10,
        padding: 25,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#333',
        lineHeight: 1.2,
        textAlign: 'center',
        width: '100%',
        padding: 30
    },
    btnprimary: {
        width: '100%',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        fontSize: 18,
        lineHeight: 1.5,
        color: '#fff',
        textTransform: 'uppercase',
        width: '100%',
        height: 50,
        borderRadius: 25,
        backgroundColor: '#0064cd',
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        textShadowOffset: {
            width: 0,
            height: -1,
        },
        textShadowRadius: 0,
        textShadowColor: 'rgba(0, 0, 0, 0.25)',
        borderTopColor: '#0064cd',
        borderRightColor: '#0064cd',
        borderBottomColor: '#003f81',
        borderLeftColor: '#0064cd',
    },
    containerList: {
        flex: 1,
        paddingTop: 20
    },
    sectionHeader: {
        paddingVertical: 20,
        paddingHorizontal: 30,
        fontSize: 20,
        backgroundColor: "#F1F1F1",
        borderRadius: 5,
    },
    item: {
        marginBottom: 10,
    },
    
});
export default App;
