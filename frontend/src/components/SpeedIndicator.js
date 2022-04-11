import React, {Component} from 'react';
import require from 'react';
import SpeedText from './SpeedText';

export default class SpeedIndicator extends Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <>
                <div class="label-50px">
                    <h>Current Speed:</h>
                </div>
                <div class="speed_indicator">
                    <label><SpeedText speed={this.props.speed}/> MPH!</label>
                </div>

            </>
        );
    }

}