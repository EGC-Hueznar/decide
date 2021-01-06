import React, { Component } from 'react';
import { Text, View, StyleSheet, Button } from 'react-native';
import AdminHome from './AdminHomepage';
import AdminVotings from './AdminVotings';

export default class Admin extends Component {

    state = {
        selectedView: "home",
    }

    setSelectedView = (view) =>  {
        this.setState({selectedView:view});
    }

  render() {
     return (
        <View style={styles.container}>
            { this.state.selectedView == "home" ?
             (<AdminHome setSelectedView={this.setSelectedView}/>)
             :
             (this.state.selectedView == "votings" ?
                (<AdminVotings votings={this.props.votings}/>)
                :
                (<Button title="Volver al inicio" onPress={() => this.setSelectedView("home")}/>))
            }
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
