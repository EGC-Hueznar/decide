import React, { Component } from 'react';
import { Text, View, Button } from 'react-native';
import AdminVotingsList from './AdminVotingsList';
import AdminVotingDetail from './AdminVotingDetail';
import axios from 'axios';
import config from '../config.json';

export default class Admin extends Component {

    state = {
        normalVotings: new Array(),
        binaryVotings: [],
        multipleVotings: [],
        preferenceVotings: [],
        selectedVoting: undefined,
    }

    setSelectedVoting = (voting) =>  {
        this.setState({selectedVoting:voting});
    }

    componentDidMount() {
        this.loadAllVotings();
    }

    loadAllVotings = () => {
        axios.get(`${config.ALL_VOTINGS_URL}votacion/all`).then(response => {
         this.setState({normalVotings:response.data.votaciones.map((v) => ({
            id: v.id,
            titulo: v.titulo,
            descripcion: v.descripcion,
            fecha_inicio: v.fecha_inicio,
            voting_type: "votacion",
         }))
        });
        });
        axios.get(`${config.ALL_VOTINGS_URL}votacionBinaria/all`).then(response => {
            this.setState({binaryVotings: response.data.votaciones.map((v) => ({
            id: v.id,
            titulo: v.titulo,
            descripcion: v.descripcion,
            fecha_inicio: v.fecha_inicio,
            voting_type: "votacionBinaria",
         }))
         });
        });
        axios.get(`${config.ALL_VOTINGS_URL}votacionMultiple/all`).then(response => {
            this.setState({multipleVotings: response.data.votaciones.map((v) => ({
            id: v.id,
            titulo: v.titulo,
            descripcion: v.descripcion,
            fecha_inicio: v.fecha_inicio,
            voting_type: "votacionMultiple",
         }))});
        });
        axios.get(`${config.ALL_VOTINGS_URL}votacionPreferencia/all`).then(response => {
            this.setState({preferenceVotings: response.data.votaciones.map((v) => ({
            id: v.id,
            titulo: v.titulo,
            descripcion: v.descripcion,
            fecha_inicio: v.fecha_inicio,
            voting_type: "votacionPreferencia",
         }))});
        });
    }

  render() {
     return (
        <View>
            { this.state.selectedVoting == undefined ?
             (<AdminVotingsList
                    normalVotings={this.state.normalVotings}
                    binaryVotings={this.state.binaryVotings}
                    multipleVotings={this.state.multipleVotings}
                    preferenceVotings={this.state.preferenceVotings}
                    setSelectedView={this.props.setSelectedView}
                    setSelectedVoting={this.setSelectedVoting}
             />)
             :
             (<AdminVotingDetail voting={this.state.selectedVoting} setSelectedVoting={this.setSelectedVoting}/>)
            }
        </View>
     );
  }
}
