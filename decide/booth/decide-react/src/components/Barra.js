import React, {Component} from 'react';
import { StatusBar, Text, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';
import { styles } from "../styles";

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