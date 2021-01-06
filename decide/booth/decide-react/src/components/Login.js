import React, { Component } from 'react';
import { Text, TextInput, TouchableOpacity, View } from 'react-native';
import config from '../config.json';
import { postData } from '../utils';
import { StyleSheet} from "react-native";
import { styles } from "../styles";


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
                                            {this.state.error && <View style={{paddingTop:10, paddingBottom:7}}>
                                                <Text style={{fontWeight: 'bold', color:'rgb(192,26,26)', fontFamily: 'calibri', fontSize:'15px', textAlign:'center'}}>
                                                El usuario introducido no existe
                                                </Text>
                                            </View>}
                                        </View>
                                        <TouchableOpacity id="button" style={styles.btnprimary} onPress={this.onSubmitLogin}>
                                            <Text style={{color:"#fff", textAlign:'center'}}>Login</Text>
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