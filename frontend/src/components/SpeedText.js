import React, {Component} from 'react';
import require from 'react';

export default class SpeedText extends Component {
    constructor(props) {
        super(props);

        
    }
    
    render() {
        
        console.log("I recieved a speed value of " + this.props.speed_text);
        
        return (

            <>
                <label>{this.props.speed_text}</label>
            </>
        );
    }

}