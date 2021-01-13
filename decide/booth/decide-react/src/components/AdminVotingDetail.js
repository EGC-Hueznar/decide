import React, { Component } from 'react';
import { Alert, StyleSheet, Button, Text, View, TouchableOpacity, SafeAreaView, FlatList } from 'react-native';
import RadioForm, {RadioButton, RadioButtonInput, RadioButtonLabel} from 'react-native-simple-radio-button';
import axios from 'axios';
import config from '../config.json';
import AddUserForm from './AddUserForm';


export default class AdminVoting extends Component {

    state = {
        voters: new Array(),
        isEditing: false,
        availableVoters: [
            {
                id: 0,
                first_name: "Andrés",
                last_name: "Pérez",
            },
            {
                id: 1,
                first_name: "Paula",
                last_name: "Vigo",
            },
        ],
    }

    enableEditing = (edit) =>  {
        this.setState({isEditing: edit});
    }

    loadVoters = (voting) => {
        axios.get(`${config.CENSUS_URL}${voting.voting_type}?voting_id=${voting.id}`).then(response => {
            this.setState({voters: response.data});
        });
    }

    componentDidMount() {
        this.loadVoters(this.props.voting);
    }


    render_user = ({item}) => (
            <View style={styles.item}>
                <Text style={styles.userName}>{item.first_name ? `${item.first_name} ${item.last_name ? item.last_name : ""}` : `Usuario ${item.id}`}</Text>
                {item.email && <Text>{item.email}</Text>}
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
                    <Text style={styles.text}>{voting.descripcion} {voting.voting_type}</Text>
                    <Text style={styles.text}>Fecha: {voting.fecha_inicio.split("+")[0]}</Text>
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
                    <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Añadir participante" onPress={() => this.enableEditing(true)} disabled={this.state.availableVoters.length == 0}/>
                </View>
            </View> : <AddUserForm voting={voting} users={this.state.availableVoters} enableEditing={this.enableEditing}/>}
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