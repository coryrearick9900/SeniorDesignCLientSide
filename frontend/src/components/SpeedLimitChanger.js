import React, {Component} from 'react';

export default class SpeedLimitChanger extends Component {
    constructor(props) {
        super(props);

        console.log("creating state...");

        this.setState({
            new_speed_thresh: 0

        });

        this.change_new_speed = this.change_new_speed.bind(this);
        this.send_new_speedthresh = this.send_new_speedthresh.bind(this);

        fetch('/api/changeSpeedThreshhold?newSpeed=' + 0,  {
            method: 'POST',
            mode: 'cors'
        }).then((responce) => 
            responce.json()
        ).then((data) => {
            console.log("Speed thresh has been changed to " + data);

            this.setState({
                new_speed_thresh: data
            });

        });

        
    }

    componentDidMount() {
        this.setState({
            new_speed_thresh: 0
        });
      }



    change_new_speed(new_number) {
        this.setState({
            new_speed_thresh: new_number
        });

        console.log("new stateful number is " + this.state.new_speed_thresh);

        
    }

    send_new_speedthresh() {

        const gathered_new_speed_thresh = this.state.new_speed_thresh;

        console.log("Gathered " + gathered_new_speed_thresh);


        let new_json = JSON.stringify({
            "newSpeed": parseInt(this.state.new_speed_thresh)
        });

        console.log("JSON is " + new_json);

        fetch('/api/changeSpeedThreshhold?newSpeed=' + this.state.new_speed_thresh,  {
            method: 'POST',
            mode: 'cors'
        }).then((responce) => 
            responce.json()
        ).then((data) => {
            console.log("Speed thresh has been changed to " + data);

            this.setState({
                new_speed_thresh: data
            });

        });

        
    }


    render() {
        return (
            <div>
                <label class="label-50px"  >Speed Limit: </label>
                <input type="number" onChange={event => this.change_new_speed(event.target.value)} class="number-50px" min="0" defaultValue="0"/>
                <button onClick={this.send_new_speedthresh} >Change Speed</button>
            </div>
        );

    }

}