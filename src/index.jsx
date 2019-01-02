import ReactDOM from 'react-dom';
import React from 'react';
import P5Wrapper from 'react-p5-wrapper';
import { startOfWeek } from 'date-fns';

/**
 * The main React container for the app. It holds the state and passes it down
 * as props to its child components.
 */
class App extends React.Component {

    constructor(props) {
        super(props);
    };

    drawLines = (p) => {
        let points = [];

        p.setup = () => {
            p.createCanvas(600,400, p.WEBGL)
            p.colorMode(p.HSB);
        };

        p.myCustomRedrawAccordingToNewPropsHandler = (props) => {
            if (props.points){
              points = props.points
            }
          };

        p.draw = () => {
            let i = 1;
            // p.line(20,100,20,100);
            for (i = 1; i < points.length; i++) {
                p.stroke(i*15, 255, 120)
                p.line(points[i-1][0], points[i-1][1], points[i][0], points[i][1]);
            }
        };
    };

    render() {
        return (<div>Yo!<P5Wrapper sketch={this.drawLines} points={[[100,100],[20,20],[150,50],[20,20],[20,20]]}/></div>);     
    }
}

ReactDOM.render(<App />, document.getElementById('root'));