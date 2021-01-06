import React, {Component} from 'react';
import { StatusBar, Text, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';
import { StyleSheet} from "react-native";

export default class Barra extends Component{

    logout = () => {
        const {token, setToken, setUser, setSignup } = this.props;
        const data = {token};  

        postData(config.LOGOUT_URL, data, token);
        setToken(null);
        setUser(null);
        this.props.handleSetStorage("decide", "")
        setSignup(true);
    }

    render(){
        return(
            <View>
                {StatusBar.currentHeight && <View style={{height:StatusBar.currentHeight, backgroundColor: '#0040A0'}}></View>}
                <View style={styles.barraStyle}>
                    
                    <View>
                        <Text style={styles.titleStyle}>DecideHueznar</Text>
                    </View>
                    {!this.props.signup && <View>
                        <Text style={styles.textStyle} onPress={this.logout}>Logout</Text>
                    </View>}
                </View>
            </View>
        );
    }
}


const styles = StyleSheet.create ({

    barraStyle: {
        width: '100%',
        backgroundColor: '#002080',
        justifyContent: 'space-between',
        paddingHorizontal: 20,
        paddingTop: 15,
        paddingBottom: 15,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
    },
    titleStyle: {
        color: 'white',
        fontSize: 18,
    },
    textStyle: {
        color: 'white',
        fontSize: 14,
    },

});

