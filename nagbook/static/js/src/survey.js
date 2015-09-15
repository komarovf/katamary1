var React = require("react");
var AnswerForm = require("./answer_form.js");

var questionTypes = [
    "one_answer",
    "multiple_answers",
    "text_answer"
];
var answersNumber = [2, 3, 4, 5, 6];
var maxQuestionsCount = 10;


var Survey = React.createClass({
    getInitialState: function() {
        return {
            questions: [],
            emails: [],
            errors: {},
            selectCountClass: ""
        };
    },

    validateSurvey: function(data) {
        var errors = {};
        for (var field in data) {
            if (!data[field].length) {
                if (field == "questions") {
                    errors[field] = "Добавьте минимум 1 вопрос!";
                } else {
                    errors[field] = "Нужно заполнить это поле!";
                };
            }
        };

        this.setState({
            errors: errors
        });

        if (Object.keys(errors).length === 0) {
            return true;
        };
        return false;
    },

    createSurvey: function(e) {
        e.preventDefault();
        var survey = [{
            "name": $('#name').val(),
            "intro_text": $('#intro_text').val(),
            "start_time": $('#start_time').val(),
            "end_time": $('#end_time').val(),
            "questions": this.state.questions.filter(function(q) {return q.status == "saved";}),
            "emails": this.state.emails
        }];
        if (this.validateSurvey(survey[0])) {
            console.log(survey[0]);
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                data: JSON.stringify({ data: survey }),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data) {
                    try {
                        if (data.status == "ok") {
                            // Redirect to cabinet page!
                            window.location = window.location.pathname.replace("survey", "cabinet");
                        };
                    } catch (e) {
                        alert("Что-то пошло нетак! Попробуйте еще раз.");
                    };
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(textStatus);
                }
            });
        };
    },

    handleTypeSelect: function(e) {
        if (e.target.value == 2) {
            this.setState({
                selectCountClass: "hidden"
            });
        } else {
            this.setState({
                selectCountClass: ""
            });
        };
    },

    handleQuestionSave: function(qBody, answers, id) {
        q = this.state.questions[id];
        q.body = qBody;
        q.answers = answers;
        q.status = "saved";
        this.setState({
            questions: this.state.questions
        });
    },

    handleQuestionDel: function(id) {
        this.state.questions.splice(id, 1);
        this.setState({
            questions: this.state.questions
        });
    },

    handleAddQuestion: function(e) {
        e.preventDefault();
        if (this.state.questions.length >= this.props.maxCount) {
            alert("Достигнут максимум вопросов в анкете");
        } else {
            questions = this.state.questions;
            q = {};
            q.type = this.refs.q_type.getDOMNode().value;
            q.body = "";
            q.status = "unsaved";
            if (q.type != 2) {
                q.aCount = this.refs.a_count.getDOMNode().value;
            };
            q.answers = [];
            questions.push(q);
            this.setState({
                questions: questions
            });
        }
    },

    emailValidate: function(email) {
        var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        return re.test(email);
    },

    handleEmailAdd: function(e) {
        e.preventDefault();
        var email = this.refs.email_input.getDOMNode().value;
        var emails = this.state.emails;
        var errors = {};

        if (this.emailValidate(email) && (emails.indexOf(email) === -1)) {
            emails.push(email);
        } else {
            errors.email_input = "Неверный Email (Возможно такой Email уже есть в списке)!";
        };
        this.setState({
            emails: emails,
            errors: errors
        });
    },

    handleEmailDel: function(email, e) {
        e.preventDefault();
        var emails = this.state.emails;
        emails.splice(emails.indexOf(email), 1);
        this.setState({
            emails: emails
        });
    },

    render: function() {
        var self = this;
        var selectTypeOptions = this.props.types.map(function(type, index) {
            return (
                <option key={"type"+index} value={index}>{type}</option>
            );
        });
        var selectCount = this.props.aCount.map(function(c) {
            return (
                <option key={"count"+c} value={c}>{c}</option>
            );
        });
        var emails = this.state.emails.map(function(email, index) {
            return (
                <li key={"email"+index}>
                    <span>{email}</span>
                    <button onClick={self.handleEmailDel.bind(null, email)}>Удалить</button>
                </li>
            );
        });

        return (
            <form ref="survey_form">
                <hr />
                <label htmlFor="name">Название опроса </label>
                <input type="text" id="name" ref="name" />
                <span>{this.state.errors.name || ""}</span>
                <br />
                <label htmlFor="intro_text">Описание опроса </label>
                <textarea id="intro_text" ref="intro_text"></textarea>
                <span>{this.state.errors.intro_text || ""}</span>
                <br />
                <label htmlFor="start_time">Дата начала опроса </label>
                <input
                    type="date"
                    id="start_time"
                    ref="start_time"
                    defaultValue={moment().format('YYYY-MM-DD')}
                />
                <span>{this.state.errors.start_time || ""}</span>
                <br />
                <label htmlFor="end_time">Дата завершения опроса </label>
                <input
                    type="date"
                    id="end_time"
                    ref="end_time"
                    defaultValue={moment().format('YYYY-MM-DD')}
                />
                <span>{this.state.errors.end_time || ""}</span>
                <br />
                <span>Можно добавить еще {this.props.maxCount - this.state.questions.length} вопросов.</span>
                <hr/>
                <div>
                    <label htmlFor="q_type">Тип вопроса</label>
                    <select
                        defaultValue={this.props.types[0]}
                        onChange={this.handleTypeSelect}
                        ref="q_type"
                        id="q_type"
                    >
                        {selectTypeOptions}
                    </select>
                    </div>
                <div className={this.state.selectCountClass}>
                    <label htmlFor="a_count">Количество ответов</label>
                    <select
                        defaultValue={this.props.aCount[1]}
                        ref="a_count"
                        id="a_count"
                    >
                        {selectCount}
                    </select>
                </div>
                <button onClick={this.handleAddQuestion}>
                    Добавить вопрос
                </button>
                <span>{this.state.errors.questions || ""}</span>
                <hr />
                <QuestionList
                    questions={this.state.questions}
                    saveQuestion={this.handleQuestionSave}
                    delQuestion={this.handleQuestionDel}
                />
                <ol>
                    {emails}
                </ol>
                <input type="text" id="email_input" ref="email_input" />
                <span>{this.state.errors.email_input || ""}</span>
                <br />
                <button onClick={this.handleEmailAdd}>
                    Добавить Email для рассылки
                </button>
                <span>{this.state.errors.emails || ""}</span>
                <hr />
                <button onClick={this.createSurvey}>Сохранить опрос</button>
            </form>
        );
    }
});


var QuestionList = React.createClass({
    render: function() {
        var self = this;
        var questions = this.props.questions.map(function(q, index) {
            return (
                <li key={"question"+index}>
                    <Question
                        data={q}
                        questionTypes={questionTypes}
                        id={index}
                        onQuestionSave={self.props.saveQuestion}
                        onQuestionDel={self.props.delQuestion}
                    />
                </li>
            );
        });
        return (
            <ul>
                {questions}
            </ul>
        );
    }
});


var Question = React.createClass({
    getInitialState: function() {
        return {
            edit: true,
            errors: {}
        }
    },

    displayAnswer: function(index) {
        var r = "a_" + this.props.id + "_" + index;
        var value = this.props.data.answers[index] || "";
        var nodes = [
            <input type="text" defaultValue={value} ref={r} />
        ];

        if (this.state.errors[r]) {
            nodes.push(<span>{this.state.errors[r]}</span>);
        };
        if (this.state.edit) {
            return (
                <div>
                    {nodes}
                </div>
            );
        } else {
            return <p>{value}</p>
        }
    },

    displayQuestion: function() {
        var qType = this.props.questionTypes[this.props.data.type];
        var value = this.props.data.body || "";
        var nodes = [
            <label htmlFor="question">Вопрос: ({qType})</label>,
            <input type="text" id="question" ref="ans" defaultValue={value} />
        ];
        if (this.state.errors["ans"]) {
            nodes.push(
                <span>{this.state.errors["ans"]}</span>
            );
        };
        if (this.state.edit) {
            return (
                <div>
                    {nodes}
                </div>
            );
        } else {
            return (
                <div>
                    <p>Вопрос: ({qType})</p>
                    <p>{value}</p>
                </div>
            );
        };
    },

    handleSaveClick: function(e) {
        e.preventDefault();
        var errors = {};
        var answers = [];
        var qBody = "";

        // validation here!
        for (var ref in this.refs) {
            if (this.refs[ref].getDOMNode().value == "") {
                errors[ref] = "Нужно заполнить это поле!";
            } else {
                if (ref == "ans") {
                    qBody = this.refs[ref].getDOMNode().value;
                } else {
                    answers.push(this.refs[ref].getDOMNode().value);
                };
            };
        };

        if (Object.keys(errors).length === 0) {
            // save question
            this.props.onQuestionSave(qBody, answers, this.props.id);
            this.setState({
                edit: false
            });
        }

        this.setState({
            errors: errors
        });
    },

    handleDelClick: function(e) {
        e.preventDefault();
        // Delete question
        this.props.onQuestionDel(this.props.id);
    },

    handleEditClick: function(e) {
        e.preventDefault();
        this.setState({
            edit: true
        });
    },

    render: function() {
        var answers, btn;

        if (this.props.data.aCount) {
            var answer_list = [];
            for (var i=0; i<this.props.data.aCount; i++) {
                answer_list.push(
                    <li key={"answ"+i}>
                        {this.displayAnswer(i)}
                    </li>
                );
            };
            answers = (
                <div>
                    <p>Варианты ответов: </p>
                    <ol>{answer_list}</ol>
                </div>
            );
        } else {
            answers = [];
        };

        if (this.state.edit) {
            btn = (
                <button onClick={this.handleSaveClick}>
                    Сохранить вопрос
                </button>
            );
        } else {
            btn = (
                <div>
                    <button onClick={this.handleDelClick}>
                        Удалить вопрос
                    </button>
                    <button onClick={this.handleEditClick}>
                        Редактировать вопрос
                    </button>
                </div>
            );
        };

        return (
            <div>
                {this.displayQuestion()}
                {answers}
                {btn}
                <hr />
            </div>
        );
    }
});


var node_add = document.getElementById("survey_add");
if (node_add) {
    React.render(
        <Survey
            types={questionTypes}
            aCount={answersNumber}
            maxCount={maxQuestionsCount}
        />,
        node_add
    );
};


var node_ans = document.getElementById("answer_survey");
if (node_ans) {
    React.render(
        <AnswerForm source={$(node_ans).data('url')} />,
        node_ans
    );
};
