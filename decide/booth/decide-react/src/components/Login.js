import React, { Component } from 'react';
import { Text, TextInput, TouchableOpacity, View } from 'react-native';
import config from '../config.json';
import { postData } from '../utils';
import { StyleSheet} from "react-native";


export default class Login extends Component {

    state = {
        form: {
            username: '',
            password: ''
        },
        error: false

    }

    onSubmitLogin = () => {
        const { setToken, handleSetStorage } = this.props;
        postData(config.LOGIN_URL, this.state.form)
            .then(response => {
               handleSetStorage("decide", response.data.token)
                setToken(response.data.token)
                this.getUser();
            })
            .catch(error => {
                this.setState({error:true})
            });
    }    

    getUser = () => {
        const { token, setUser, setSignup } = this.props;
        const data = {
            token
        };
        
        postData(config.GETUSER_URL, data, token)
            .then(response => {
                setUser(response.data);
                setSignup(false);
            }).catch(error => {
                this.setState({error:true})
            });
    }
  
    handleChange = (name, value) => {        
        this.setState(
            {
                form: {
                    ...this.state.form,
                    [name]: value
                }
            }
        );
    }

    render() {
        return (
            <View>
                <View style={styles.html}>
                    <View style={styles.body}>
                      <View style={styles.container}>                            
                            <View style={styles.content}>
                                <View style={styles.row}>
                                    <View style={styles.span14}>
                                        <View style={styles.clearfix}>
                                            <View>
                                                <Text style={styles.title}>Usuario</Text>
                                            </View>
                                            <View>
                                                <TextInput id='username'  name="username" hint="username" style={styles.input} onChangeText={(val) => this.handleChange('username', val)} placeholder="Introduce tu usuario"></TextInput>
                                            </View>
                                            <View>
                                                <Text style={styles.title}>Contraseña</Text>
                                            </View>
                                            <View>
                                                <TextInput id='password' name="password" hint="password" style={styles.input} secureTextEntry={true} onChangeText={(val) => this.handleChange('password', val)} placeholder="Introduce tu contraseña"></TextInput>
                                            </View>
                                        </View>
                                        {this.state.error && <View style={{paddingTop:10, paddingBottom:7}}>
                                        <Text style={{color:'rgb(192,26,26)', fontSize:15}}>El usuario introducido no existe</Text>
                                        </View>}
                                        <TouchableOpacity id="button" style={styles.btnprimary} onPress={this.onSubmitLogin}>
                                            <Text style={{color:"#fff"}}>Login</Text>
                                        </TouchableOpacity>
                                    </View>
                                </View>
                            </View>
                        </View>
                    </View>
                </View>
            </View>
        );
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
    row: {
    },
    clearfix: {
        "marginBottom": 24,
    },
    input: {
        fontSize: 15,
        lineHeight: 1,
        color: '#666666',
        width: '100%',
        backgroundColor: '#f1f1f1',
        height: 50,
        borderRadius: 25,
        paddingTop: 0,
        paddingRight: 30,
        paddingBottom: 0,
        paddingLeft: 20,
        width: '100%',
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
    actions: {

    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#000000',
        lineHeight: 1.2,
        textAlign: 'center',
        width: '100%',
        padding: 30
    },
  });