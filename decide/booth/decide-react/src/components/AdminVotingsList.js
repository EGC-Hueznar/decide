import React, { Component } from 'react';
import {FlatList, Text, TouchableOpacity, View, StyleSheet, Button, SafeAreaView} from 'react-native';

export default class AdminVotings extends Component {

  render_voting = ({item}) => (
    <TouchableOpacity onPress={() => this.props.setVotingId(item.id)} disabled={!item.start_date}>
        <View style={styles.item}>
            <Text>{item.name}</Text>
        </View>
    </TouchableOpacity>
  );

  render() {
     return (
        <View style={styles.container}>
            <View style={styles.content}>
                <Text style={styles.title}>Votaciones creadas</Text>
                <Text style={styles.subtitle}>Aquí puedes ver todas las votaciones existentes en el sistema.
                Para obtener información más detallada sobre una votación o gestionarla, solo tines que hacer click en
                el nombre de la misma. </Text>
                <SafeAreaView style={styles.list}>
                        <FlatList data={this.props.votings} renderItem={this.render_voting} />
                </SafeAreaView>
                <View style={styles.sections}>
                    <View style={styles.button}>
                        <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Volver al inicio"
                         onPress={() => this.props.setSelectedView("home")}/>
                    </View>
                    <View style={styles.button}>
                        <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Nueva votación"/>
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
    width: "100%",
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