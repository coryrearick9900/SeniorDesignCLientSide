import React, {Component} from 'react';
import require from 'react';

export default class SpeedText extends Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <>
                <label>{this.props.speed_text}</label>
            </>
        );
    }

}