import ReactDOM from 'react-dom';
import React from 'react';
import io from 'socket.io-client';

/**
 * The main React container for the app. It holds the state and passes it down
 * as props to its child components.
 */
 class Whiteboard extends React.Component {

    componentDidMount() {
        const can = this.refs.canvas.getContext('2d')
        can.fillStyle='green';
        can.fillRect(10,10,150,100);
        this.setState({_isMounted: true});
    }

    componentWillUnmount() {
        this._isMounted = false;
    }
    constructor(props) {
        super(props);
        this.client = io('http://localhost:9091');
        this.client.on('points', this.handleUpdate)
        this.state = {_isMounted: false}
    };

    handleUpdate = (msg) => {
        if (this.state._isMounted) {
            const can = this.refs.canvas.getContext('2d')
            const points = msg.points;
            console.log(points);
            let i=0;
            can.fillStyle='#fdfdfd';
            can.fillRect(0,0,640,480);
            // can.fillStyle='black';

            // can.beginPath();
            // can.moveTo(points.x[0],points.y[0]);
            for (i = 0; i < points.x.length; i++) {
                const fill = 'hsl('.concat(String(i%255), ', 100%, 75%)')
                can.fillStyle=fill;
                can.fillRect(points.x[i], points.y[i], 2, 2);
                // can.lineTo(points.x[i], points.y[i]);
                // can.stroke();
            }
        }
        
    }

    render() {
        return (<canvas ref="canvas" width={640} height={480} />);     
    }
}


ReactDOM.render(<Whiteboard />, document.getElementById('root'));