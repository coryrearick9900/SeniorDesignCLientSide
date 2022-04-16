import React, {Component} from 'react';
import require from 'react';

export default class Image extends Component {
    constructor(props) {
        super(props);

    }


    render() {
        return (
            <div class="center" >
                <div class="image-box">
                    <img src={this.props.image} />
                </div>
            </div>
        );
    }


}

