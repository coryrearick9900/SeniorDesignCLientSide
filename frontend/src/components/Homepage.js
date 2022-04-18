import React, {Component, isValidElement, useState } from 'react';
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
            "currentSpeed": 0,
            "image": "",
            active: false
        }

        
    }


    getSpeedFromBackend() {

        //console.log("state must be true");

        if (this.state.active) {

            fetch('/api/getLastReading')
            .then(response => response.json())
            .then(data => {
                
                var image = data['image'];
                
                const ImageRender = ({image}) => <img src={`data:image/jpeg;base64,${image}`} />
                
                ReactDOM.render(<ImageRender image={this.state.image} />, document.getElementById('image_container'));
                
                var speed = data['speed'];
                speed = Math.round(speed * 1000) / 1000;
                
                    this.setState({
                        currentSpeed: speed,
                        image: image
                    }, () => {
                        //console.log("state should be changed");
                    });
                    
                    
                    //console.log("speeeeeeeed iS " + this.state.currentSpeed);
                    //console.log("Image is " + this.state.image);
                    
                }).catch(console.error);
                
            }else {
                this.setState(
                    {
                        "currentSpeed": 0,
                        "image": ""
                    }
                );
            }
                
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
                                <button onClick={() => {this.state.active = true; console.log("State is now " + this.state.active)}}  >
                                    Start Collection
                                </button>
                                <button onClick={() => {this.state.active = false; console.log("State is now " + this.state.active)}} >
                                    Stop Collection
                                </button>
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
