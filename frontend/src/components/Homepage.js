import React, {Component} from 'react';
import Image from "./Image"
import DataBaseConnection from './DataBaseConnection';
import {BrowserRouter, Switch, Routes, Link, Route, Redirect} from 'react-router-dom'
import SpeedIndicator from './SpeedIndicator';
import SpeedLimitChanger from './SpeedLimitChanger';
import StartStop from './StartStop';
import { Grid, Button } from "@material-ui/core";
import { userState, useEffect } from "react";
import ReactDOM from 'react-dom';

export default class Homepage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            "currentSpeed": 12,
            "image": ""
        }
        
    }


    getSpeedFromBackend() {


        
        fetch('/api/getLastReading')
            .then(response => response.json())
            .then(data => {

                console.log("SPEEEEED IS " + this.state.currentSpeed);
                
                //Decode from Base64 to bytes
                imgdecode = atob(this.state.image);
                this.state.image = imgdecode;

                console.log("Image is " + this.state.image);

            }).catch(console.error);

    }

    tick() {
        this.getSpeedFromBackend();
        this.forceUpdate();
    }

    componentDidMount() {

        this.interval = setInterval(() => this.tick(), 1000);
    
    }



    render() {

        

        return (
            <div class="homepage_div">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.1.0/react.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.1.0/react-dom.min.js"></script>

                <div class="row">
                    <div class="column" >
                        <div class="left-column">
                            <div id="image_container" class="image_container">
                                
                            </div>
                            <Grid container justify="center">
                                <StartStop />
                            </Grid>
                        </div>
                    </div>
                    <div class="column">
                        <DataBaseConnection />
                        <hr />
                        
                            <div class="label-50px">
                                <h>Current Speed:</h>
                            </div>
                            <div class="speed_indicator">
                                <Speed speed={this.state.currentSpeed} />
                            </div>

                        <hr />

                        <SpeedLimitChanger />
                    </div>
                </div>
            </div>
        );
    }
}

const Speed = ({ speed }) => (
    <label>{speed} MPH</label>
);

const ImageRender = ({image}) => <img src={`image:image/jpeg;base64,${image}`} />