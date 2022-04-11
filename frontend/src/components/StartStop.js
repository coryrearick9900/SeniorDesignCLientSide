import React, {Component} from 'react';

export default class StartStop extends Component {
    constructor(props) {
        super(props);

    }

    render() {
        return(
            <>
                <button class="button-pad" id="start_button">Start Collection</button>
                <button class="button-pad" id="stop_button">Stop Collection</button>
            </>
        );
    }
}