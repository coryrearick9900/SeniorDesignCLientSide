import React, {Component} from 'react';
import Image from "./Image"
import DataBaseConnection from './DataBaseConnection';
import {BrowserRouter, Switch, Routes, Link, Route, Redirect} from 'react-router-dom'
import SpeedIndicator from './SpeedIndicator';
import SpeedLimitChanger from './SpeedLimitChanger';
import StartStop from './StartStop';
import { Grid, Button } from "@material-ui/core";

export default class Homepage extends Component {
    constructor(props) {
        super(props);
        this.state = {currentSpeed: 0 };
    }


    getSpeedFromBackend() {


        fetch('/api/getLastReading').then((responce) =>
        responce.json()
        ).then((data) => {
            
            console.log("Time to set the speed to " + data);
            
            this.setState({
                currentSpeed: data
            })
        });
    
    
        //console.log("Speed is now " + this.state.currentSpeed);
    
    }

    tick() {

        this.getSpeedFromBackend();
    }

    componentDidMount() {
        this.interval = setInterval(() => this.tick(), 500);
      }



    render() {
        return (
            <div class="homepage_div">
                <div class="row">
                    <div class="column" >
                        <div class="left-column">
                            <Image />
                            <Grid container justify="center">
                                <StartStop />
                            </Grid>
                        </div>
                    </div>
                    <div class="column">
                        <DataBaseConnection />
                        <hr />
                        <SpeedIndicator speed={this.state.currentSpeed} />
                        <hr />
                        <SpeedLimitChanger />
                    </div>
                </div>
            </div>
        );
    }
}