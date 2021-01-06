import React, { Component } from 'react';
import { Text, View, StyleSheet, Button } from 'react-native';
import AdminHome from './AdminHomepage';
import AdminUsers from './AdminUsers';

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
                (<Button title="Volver al inicio" onPress={() => this.setSelectedView("home")}/>)
                :
                (<AdminUsers setSelectedView={this.setSelectedView} />))
            }
        </View>
     );
  }
}

const styles = StyleSheet.create({
 container: {
    paddingTop: 60,
    paddingBottom: 60,
    paddingRight: 120,
    paddingLeft: 120,
    width: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
 },
});
