var React = require("react");
var CheckboxGroup = require('react-checkbox-group');
var RadioGroup = require('react-radio');


var AnswerForm = React.createClass({
    getInitialState: function() {
        return {
          survey: {},
          answers: {},
          errors: []
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
                    <RadioGroup name={"q"+index} ref={"q"+index} onChange={self.handleAnswerChange.bind(null, index, 0)}>
                        <div>
                            {answersData}
                        </div>
                    </RadioGroup>
                );
            } else if (q.type == 1) {
                answers = (
                    <CheckboxGroup name={"q"+index} ref={"q"+index} onChange={self.handleAnswerChange.bind(null, index, 1)}>
                        <div>
                            {answersData}
                        </div>
                    </CheckboxGroup>
                );
            } else {
                answers = (
                    <textarea onChange={self.handleAnswerChange.bind(null, index, 2)} ref={"q"+index}></textarea>
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

    handleAnswerChange: function(i, type) {
        if (type == 2) {
            this.state.answers[i] = this.refs["q"+i].getDOMNode().value;
        } else if (type == 1) {
            this.state.answers[i] = this.refs["q"+i].getCheckedValues();
        } else if (type == 0) {
            this.state.answers[i] = this.refs["q"+i].getValue();
        };

        this.setState({
            answers: this.state.answers
        });
    },

    handleSaveAnswers: function(e) {
        e.preventDefault();
        var errors = [];
        for (var i=0; i < this.state.survey.questions.length; i++) {
            if (!this.state.answers[i] || this.state.answers[i].length == 0) {
                errors.push(i+1);
            } 
        };
        this.setState({
            errors: errors
        });
        if (errors.length == 0) {
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                data: JSON.stringify(this.state.answers),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data) {
                    try {
                        if (data.status == "ok") {
                            // Redirect to index page!
                            window.location.href = '/';
                        };
                    } catch (e) {
                        alert("Что-то пошло нетак! Попробуйте еще раз.");
                    };
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown);
                }
            });
        }
    },

    render: function() {
        var today = moment();
        var survey = this.state.survey;
        if (this.state.errors.length > 0) {
            var error = "Нужно ответить на вопросы: " + this.state.errors;
        }
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
                    <div className="text-warning">
                        {error}
                    </div>
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
