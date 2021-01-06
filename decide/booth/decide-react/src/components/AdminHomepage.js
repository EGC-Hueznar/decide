import React, { Component } from 'react';
import { Text, View, StyleSheet, Button } from 'react-native';

export default class AdminHome extends Component {

  render() {
     return (
          <View style={styles.content}>
            <Text style={styles.title}>¡Bienvenido Admin!</Text>
            <Text>Desde este portal puedes gestionar tanto las votaciones creadas como los usuarios registrados.</Text>
            <View style={styles.sections}>
                <View style={styles.button}>
                    <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Votaciones" onPress={() => this.props.setSelectedView("votings")}/>
                </View>
                <View style={styles.button}>
                    <Button color="linear-gradient(top, #049cdb, #0064cd)" title="Usuarios" onPress={() => this.props.setSelectedView("users")}/>
                </View>
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