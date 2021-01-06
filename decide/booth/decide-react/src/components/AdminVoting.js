import React, { Component } from 'react';
import { Alert, StyleSheet, Button, Text, View } from 'react-native';
import RadioForm, {RadioButton, RadioButtonInput, RadioButtonLabel} from 'react-native-simple-radio-button';

export default class AdminVoting extends Component {

    state = {
        voting: undefined,
        options: new Array(),
    }

    render() {
        const { voting } = this.props;

        return <View style={styles.htmlStyle}>
                <View style={styles.containerStyle}>
                    <View style={styles.contentStyle}>
                        <View style={styles.row}>
                            <View style={styles.clearfix}>
                                <Text style={styles.textStyle}>{voting.name}</Text>
                                <Text style={styles.textStyle}>{voting.question.desc}</Text>
                                <View style={{flex: 1, backgroundColor: 'powderblue'}} />
                            </View>
                            <View style={styles.clearfix}>
                            <RadioForm style={styles.radioStyle}
                                            radio_props={this.state.options}
                                            disabled = {true}
                                            initial={-1}
                                            formHorizontal={true}
                                            labelHorizontal={false}
                                            buttonColor={'#2196f3'}
                                            animation={true}
                                            onPress={() => {}}
                                            buttonSize={20}
                                        />
                            </View>
                            <View style={styles.clearfix}>
                                <View style={styles.button1Style}>
                                    <Button title="Votar" color="linear-gradient(top, #049cdb, #0064cd)" disabled={true} />
                                </View>
                            </View>
                            <View style={styles.clearfix}>
                                <View style={styles.button2Style}>
                                    <Button title="Volver" color="linear-gradient(top, #696969, #000000)" />
                                </View>
                            </View>
                        </View>
                    </View>
                </View>
        </View>
    }
}

const styles = StyleSheet.create ({
    htmlStyle: {
        marginTop: 0,
        marginBottom: 0,
        marginRight: 0,
        marginLeft: 0,
        paddingTop: 0,
        paddingBottom: 0,
        paddingRight: 0,
        paddingLeft: 0
    },

    containerStyle: {
        justifyContent: 'center',
        alignItems: 'center'
    },
    contentStyle: {
        width: 960,
        backgroundColor: '#fff',
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        borderBottomRightRadius: 10,
        borderBottomLeftRadius: 10,
        overflow: 'hidden',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        paddingTop: 50,
        paddingRight: 50,
        paddingBottom: 50,
        paddingLeft: 50
    },
    textStyle:{
        fontSize: 26,
        lineHeight: 24,
        paddingTop:10,
        paddingBottom:10,
        justifyContent: 'center',
        alignSelf: 'center'
    },
    radioStyle:{
        justifyContent: 'center',
        alignSelf: 'center'
    },
    row: {
    },
    clearfix: {
        "marginBottom": 24,
    },
    button1Style: {
        width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
        borderBottomRightRadius: 25,
        borderBottomLeftRadius: 25,
        backgroundColor: "#0064cd",
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        textShadowOffset: {
          width: 0,
          height: -1
        },
        textShadowRadius: 0,
        textShadowColor: "rgba(0, 0, 0, 0.25)",
        borderTopColor: "#0064cd",
        borderRightColor: "#0064cd",
        borderBottomColor: "#0064cd",
        borderLeftColor: "#0064cd"
    },
    button2Style: {
        width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
        borderBottomRightRadius: 25,
        borderBottomLeftRadius: 25,
        backgroundColor: "#000000",
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        textShadowOffset: {
          width: 0,
          height: -1
        },
        textShadowRadius: 0,
        textShadowColor: "rgba(0, 0, 0, 0.25)",
        borderTopColor: "#000000",
        borderRightColor: "#000000",
        borderBottomColor: "#000000",
        borderLeftColor: "#000000"
    },
});