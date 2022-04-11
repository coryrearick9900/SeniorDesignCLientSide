import React, {Component} from 'react';

export default class DataBaseConnection extends Component {
    constructor(props) {
        super(props);

    }

    render() {
        return(
            <div>
                <input type="text" id="database_connection" ></input>
                <button id="connection">Enter IP</button>
            </div>
        );
    }

}