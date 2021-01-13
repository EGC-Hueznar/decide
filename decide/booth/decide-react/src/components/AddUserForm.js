import React, { Component } from 'react';
import { Text, StyleSheet, TouchableOpacity, SafeAreaView, FlatList, View, Button } from 'react-native';
import RadioForm from 'react-native-simple-radio-button';

export default class AddUserForm extends Component {

    state = {
        options: new Array(),
        voterId: undefined,
    }

    setOptions = (voters) => {
        const cleanedOptions = voters.map(opt => ({
            label: `${opt.first_name} ${opt.last_name}`,
            value: opt.id
        }))
        this.setState({options: cleanedOptions});
    }

    setUserId = (id) => {
        this.setState({voterId: id});
        console.log(id);
    }

    componentDidMount() {
        const { users } = this.props;
        this.setOptions(users);
    }


    render() {
     return (
        <View style={styles.container}>
            <View style={styles.content}>
                <Text style={styles.title}>Añadir participantes</Text>
                <Text style={styles.subtitle}>Selecciona un nuevo participante: </Text>
                    <RadioForm
                      style={styles.radioStyle}
                      radio_props={this.state.options}
                      initial={-1}
                      formHorizontal={false}
                      labelHorizontal={true}
                      buttonColor={"#2196f3"}
                      animation={true}
                      onPress={(val) => this.setUserId(val)}
                      buttonSize={20}
                    />
                    <View style={styles.sections}>
                    <View style={styles.button}>
                        <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Cancelar"
                         onPress={() => this.props.enableEditing(false)}/>
                    </View>
                    <View style={styles.button}>
                        <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Añadir" disabled={this.state.voterId == undefined}/>
                    </View>
                </View>
            </View>
        </View>
     );
  }
}

const styles = StyleSheet.create({
 container: {
    paddingTop: 60,
    paddingBottom: 60,
    width: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
 },
 item: {
    marginBottom: 10,
    marginTop: 10,
    padding: 8,
    backgroundColor: "#eeeeee",
    borderRadius: 4,
    display: "flex",
    flexDirection: "row",
 },
 list: {
    display: "flex",
    justifyContent: "flex-start",
    width: "100%",
    marginBottom: 60,
 },
 title: {
    fontSize: 30,
    fontWeight: "bold",
    marginBottom: 30,
 },
 subtitle: {
    marginBottom: 30,
 },
 containerList: {
    display: "flex",
    justifyContent: "flex-start",
    width: "100%",
 },
 content: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
 },
 sections: {
    marginTop: 60,
    display: "flex",
    flexDirection: "row",
    justifyContent: "center"
 },
 button: {
    width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        marginRight: 10,
        marginLeft: 10,
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
    borderBottomColor: "#003f81",
    borderLeftColor: "#0064cd"
 },
});