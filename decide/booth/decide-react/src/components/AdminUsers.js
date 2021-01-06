import React, { Component } from 'react';
import { Text, View, StyleSheet, Button, FlatList, SafeAreaView } from 'react-native';


export default class AdminUsers extends Component {

    state = {
        users: [
        {
            id: 1,
            first_name: undefined,
            last_name: undefined,
            email: undefined,
        },
        {
            id: 2,
            first_name: "Pedro",
            last_name: "Gómez",
            email: "pedro@gmail.com",
        },
        {
            id: 3,
            first_name: "Luis",
            last_name: "Pérez",
            email: undefined,
        },
        ],
    }

    render_user = ({item}) => (
            <View style={styles.item}>
                <Text style={styles.userName}>{item.first_name ? `${item.first_name} ${item.last_name ? item.last_name : ""}` : `Usuario ${item.id}`}</Text>
                {item.email && <Text>{item.email}</Text>}
            </View>
    );

  render() {
     return (
        <View style={styles.content}>
            <Text style={styles.title}>Usuarios registrados</Text>
            <Text style={styles.subtitle}>Aquí puedes consultar qué usuarios están registrados en Decide.</Text>
            <SafeAreaView style={styles.list}>
                <FlatList data={this.state.users} renderItem={this.render_user} />
            </SafeAreaView>
            <View style={styles.button}>
                <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Volver al inicio" onPress={() => this.props.setSelectedView("home")}/>
            </View>
        </View>
     );
  }
}

const styles = StyleSheet.create({
 title: {
    fontSize: 30,
    fontWeight: "bold",
    marginBottom: 30,
 },
 subtitle: {
    marginBottom: 30,
 },
 list: {
    display: "flex",
    justifyContent: "flex-start",
    width: "100%",
    marginBottom: 60,
 },
 content: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "100%",
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
 sections: {
    marginTop: 60,
    display: "flex",
    flexDirection: "row",
    justifyContent: "center"
 },
 userName: {
    marginRight: "auto",
 },
 button: {
    minWidth: 60,
    marginRight: 10,
    marginLeft: 10,
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
    borderLeftColor: "#0064cd"
 },
});