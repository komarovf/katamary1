var React = require("react");
var CheckboxGroup = require('react-checkbox-group');
var RadioGroup = require('react-radio')


var AnswerForm = React.createClass({
    getInitialState: function() {
        return {
          survey: {},
        };
    },

    componentDidMount: function() {
        $.get(this.props.source, function(result) {
            var survey = result.survey;
            if (this.isMounted()) {
                this.setState({
                    survey: survey,
                });
            }
        }.bind(this));
    },

    renderAnswers: function(a, type, key, i) {
        var inputType;
        if (type == 0) {
            inputType = "radio"
        } else if (type == 1) {
            inputType = "checkbox"
        }
        return (
            <div key={key}>
                <label>
                    <input type={inputType} value={i} />{a}
                </label>
            </div>
        );
    },

    renderQuestions: function(questions) {
        var self = this;

        var result = questions.map(function(q, index) {
            var answers;
            var answersData = q.answers.map(function(a, i) {
                var key = "answer"+index+"_"+i;
                return self.renderAnswers(a, q.type, key, i);
            });

            if (q.type == 0) {
                answers = (
                    <RadioGroup name={"q"+index}>
                        <div>
                            {answersData}
                        </div>
                    </RadioGroup>
                );
            } else if (q.type == 1) {
                answers = (
                    <CheckboxGroup name={"q"+index}>
                        <div>
                            {answersData}
                        </div>
                    </CheckboxGroup>
                );
            } else {
                answers = (
                    <textarea></textarea>
                );
            };
            return (
                <div>
                    <li key={"question"+index}>
                        <p>{q.body}</p>
                        {answers}
                    </li>
                </div>
            );
        });

        return result;
    },

    handleSaveAnswers: function(e) {
        e.preventDefault();
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
                    <hr />
                    <ol>
                        {this.renderQuestions(survey.questions || [])}
                    </ol>
                    <hr />
                    <button onClick={this.handleSaveAnswers}>Отправить ответы</button>
                </div>
            );
        }
    }
});


module.exports = AnswerForm;
