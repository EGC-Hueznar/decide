import React, { Component } from 'react';
import {FlatList, Text, TouchableOpacity, View, StyleSheet, Button, SafeAreaView} from 'react-native';

export default class AdminVotings extends Component {

  render_voting = ({item}) => (
    <TouchableOpacity onPress={() => this.setSelectedVoting(item)} disabled={!item.start_date}>
        <View View style={styles.item}>
            <Text style={styles.sectionHeader}>{item.name}</Text>
        </View>
    </TouchableOpacity>
  );

  render() {

     return (
        <View style={styles.container}>
            <View style={styles.content}>
                <Text style={styles.title}>Votaciones creadas</Text>
                <Text>Aquí puedes ver todas las votaciones existentes en el sistema.</Text>
                    <SafeAreaView style={styles.containerList}>
                            <FlatList style={styles.item} data={this.props.votings} renderItem={this.render_voting} />
                    </SafeAreaView>
                <View style={styles.sections}>
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