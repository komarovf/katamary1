var React = require("react");


var AnswerForm = React.createClass({
    getInitialState: function() {
        return {
          survey: {},
        };
    },

    componentDidMount: function() {
        $.get(this.props.source, function(result) {
            var survey = result.survey;
            console.log(survey);
            if (this.isMounted()) {
                this.setState({
                    survey: survey,
                });
            }
        }.bind(this));
    },

    renderAnswers: function(a, type) {
        return (
            <li>{a}</li>
        );
    },

    renderQuestions: function(questions) {
        var self = this;
        var result = questions.map(function(q, index) {
            var answers = q.answers.map(function(a, i) {
                var key = "answer"+index+"_"+i;
                return (
                    <ul key={key}>
                        {self.renderAnswers(a, q.type)}
                    </ul>
                );
            });

            return (
                <li key={"question"+index}>
                    <p>{q.body}</p>
                    {answers}
                </li>
            );
        });
        return result;
    },

    render: function() {
        var today = moment();
        var survey = this.state.survey;
        if (survey.start_time > today || survey.end_time < today) {
            return (
                <div>
                    Время опроса: {survey.start_time} - {survey.end_time}
                </div>
            );
        } else {
            return (
                <div>
                    <h1>{survey.name}</h1>
                    <p>{survey.intro_text}</p>
                    <h3>Вопросы:</h3>
                    <ol>
                        {this.renderQuestions(survey.questions || [])}
                    </ol>
                </div>
            );
        }
    }
});


module.exports = AnswerForm;
