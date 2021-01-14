import React, { Component } from 'react';
import { Alert, StyleSheet, Button, Text, View, TouchableOpacity, SafeAreaView, FlatList } from 'react-native';
import RadioForm, {RadioButton, RadioButtonInput, RadioButtonLabel} from 'react-native-simple-radio-button';
import axios from 'axios';
import config from '../config.json';
import AddUserForm from './AddUserForm';


export default class AdminVoting extends Component {

    state = {
        voters: [],
        isEditing: false,
        users: [],
    }

    enableEditing = (edit) =>  {
        console.log(edit);
        this.setState({isEditing: edit});
    }

    loadCensus = (voting) => {
        axios.get(`${config.CENSUS_URL}${voting.voting_type}?voting_id=${voting.id}`).then(response => {
            this.setState({voters: response.data.voters});
        });
    }

    loadUsers = () => {
        axios.get(config.GET_ALL_USERS_URL).then(response => {
            this.setState({users: response.data.users.filter((v) => !this.state.voters.includes(v))});
        });
    }


    componentDidMount() {
        this.loadCensus(this.props.voting);
        this.loadUsers();
    }


    render_user = ({item}) => (
            <View style={styles.item}>
                <Text style={styles.userName}>Usuario {item}</Text>
            </View>
    );

    render() {
        const { voting } = this.props;

        return (
        <View style={styles.content}>
        {!this.state.isEditing ?
            <View style={styles.content}>
                <View style={styles.section}>
                    <Text style={styles.title}>{voting.titulo}</Text>
                    <Text style={styles.text}>{voting.descripcion}</Text>
                    <Text style={styles.text}>Fecha: {voting.fecha_inicio ? voting.fecha_inicio.split("+")[0] : "Sin determinar"}</Text>
                </View>
                <View style={styles.button}>
                    <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Volver al inicio" onPress={() => this.props.setSelectedVoting(undefined)}/>
                </View>
                <View style={styles.section}>
                    <Text style={styles.title}>Censo</Text>
                    <Text>Aquí puedes ver y gestionar las personas que pueden participar en esta votación.</Text>
                </View>
                <SafeAreaView style={styles.list}>
                    <FlatList data={this.state.voters} renderItem={this.render_user} />
                </SafeAreaView>
                <View style={styles.button}>
                    <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Añadir participante" onPress={() => this.enableEditing(true)} disabled={this.state.users.length == 0}/>
                </View>
            </View> : <AddUserForm voting={voting} users={this.state.users} loadCensus={this.loadCensus} loadUsers={this.loadUsers}  voting={voting} enableEditing={this.enableEditing}/>}
            </View>
        );
    }
}

const styles = StyleSheet.create ({
    content: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: "100%",
    },
    title: {
        fontSize: 30,
        fontWeight: "bold",
        marginBottom: 30,
    },
    list: {
        display: "flex",
        justifyContent: "flex-start",
        width: "100%",
        marginBottom: 60,
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
    userName: {
        marginRight: "auto",
    },
    text: {
        fontSize: 26,
        lineHeight: 24,
        paddingTop:10,
        paddingBottom:10,
        justifyContent: 'center',
        alignSelf: 'center'
    },
    options: {
        justifyContent: 'center',
        alignSelf: 'center',
        marginBottom: 24,

    },
    section: {
        marginBottom: 24,
    },
    button: {
        minWidth: 60,
        marginRight: 10,
        marginLeft: 10,
        marginBottom: 50,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        width: "120",
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
        borderBottomColor: "#003f81",
        borderLeftColor: "#0064cd",
    },
});