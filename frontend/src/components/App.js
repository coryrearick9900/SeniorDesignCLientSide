import React, {Component} from "react";
import {render} from "react-dom";
import ConnectToDB from "./ConnectToDB";
import Homepage from "./Homepage";


export default class App extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(
            
            <div>
                <Homepage />
            </div>
        );
    }

}

const appDiv = document.getElementById("app");
render(<App  />, appDiv);