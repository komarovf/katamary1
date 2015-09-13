var React = require("react");

var HelloWorld = React.createClass({
    getInitialState: function() {
        return {count: 0};
    },
    increaseCount: function() {
        var newCount = this.state.count + 1;
        this.setState({
            count: newCount
        });
    },
    render: function() {
        return (
            <li>
                <button onClick={this.increaseCount}>Say hello</button>
            </li>
        );
    }
});
