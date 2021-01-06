import React, { Component } from 'react';
import { Text, View, Button } from 'react-native';
import AdminVotingsList from './AdminVotingsList';
import AdminVotingDetail from './AdminVotingDetail';

export default class Admin extends Component {

    state = {
        votingId: undefined,
    }

    setVotingId = (id) =>  {
        this.setState({votingId:id});
    }

  render() {
     return (
        <View>
            { this.state.votingId == undefined ?
             (<AdminVotingsList votings={this.props.votings} setSelectedView={this.props.setSelectedView} setVotingId={this.setVotingId}/>)
             :
             (<AdminVotingDetail voting={this.props.votings.find((v) => v.id == this.state.votingId)} setVotingId={this.setVotingId}/>)
            }
        </View>
     );
  }
}
