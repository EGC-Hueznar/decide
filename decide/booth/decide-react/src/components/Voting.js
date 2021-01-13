import React, { Component } from 'react';
import { BigInt } from '../crypto/BigInt';
import { ElGamal } from '../crypto/ElGamal';
import { Text, TouchableOpacity, View } from 'react-native';
import { postData } from '../utils';
import config from '../config.json';
import { StyleSheet} from "react-native";
import RadioForm from 'react-native-simple-radio-button';

export default class Voting extends Component {

    state = {
        bigpk: {
            p: BigInt.fromJSONObject(this.props.voting.pub_key.p.toString()),
            g: BigInt.fromJSONObject(this.props.voting.pub_key.g.toString()),
            y: BigInt.fromJSONObject(this.props.voting.pub_key.y.toString()),
        },
        voting: null,
        selected: null,
        options: [],
        noSelection: false,
        error: false,

    }

    doneToFalse =() => {
        this.props.setDone(false);
    }

    handleSubmit = () => {
        if (!this.state.selected) {
            this.setState({noSelection:true})
        } else {
            const { voting, user } = this.props;
            const vote = this.encrypt();
            const data = {
                vote: {a: vote.alpha.toString(), b: vote.beta.toString()},
                voting: voting.id,
                voter: user.id,
                token: this.props.token
            };
            this.send(data);
        }
    }

    encrypt = () =>  {
        const { selected } = this.state;
        const bigmsg = BigInt.fromJSONObject(selected.toString());
        const cipher = ElGamal.encrypt(this.state.bigpk, bigmsg);
        return cipher;
    }

    send = (data) => {
        postData(config.STORE_URL, data, this.props.token)
            .then(response => {
                this.props.setDone(true)
                this.props.resetSelected();
            })
            .catch(error => {
                this.setState({ error })
            });
    }


    setOptions = (voting) => {
        const cleanedOptions = voting.question.options.map(opt => ({
            label: opt.option,
            value: opt.number
        }))
        this.setState({options: cleanedOptions});
    }

    componentDidMount() {
        this.doneToFalse();
        const { voting } = this.props;
        this.setOptions(voting);
    }

    updateSelected = (itemValue) => {
        this.setState({selected: itemValue})
    }

    render() {
        const { voting, resetSelected } = this.props;

        const {styles} = this.props;

        return <View style={styles.htmlStyle}>
        <View View style={styles.body}>
        <View style={styles.container}>
          <View style={styles.content}>
            <View style={styles.row}>
              <View style={styles.clearfix}>
                <Text style={styles.votingStyle}>{voting.name}</Text>
                <Text style={styles.votingStyle}>{voting.question.desc}</Text>
                <View style={{ flex: 1, backgroundColor: "powderblue" }} />
              </View>
              <View style={styles.clearfix}>
                <RadioForm 
                  labelColor={styles.labelColor}
                  style={styles.radioStyle}
                  radio_props={this.state.options}
                  initial={-1}
                  formHorizontal={false}
                  labelHorizontal={true}
                  buttonColor={"#2196f3"}
                  animation={true}
                  onPress={(val) => this.updateSelected(val)}
                  buttonSize={20}
                />
              </View>
              {this.state.noSelection && (
                <View style={styles.textStyle}>
                  <Text
                    style={styles.state}
                  >
                    Debe seleccionar una opción
                  </Text>
                </View>
              )}
      
              <View style={styles.clearfix}>
                <TouchableOpacity style={styles.button1Style} onPress={this.handleSubmit}>
                  <Text style={{color:"#fff", textAlign:'center'}}>Votar</Text>
                </TouchableOpacity>
              </View>
              <View style={styles.clearfix}>
                <TouchableOpacity style={styles.button2Style} onPress={resetSelected}>
                  <Text style={{color:"#999", textAlign:'center'}}>Volver a votaciones</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </View>
        </View>
      </View>;      
    }
}
