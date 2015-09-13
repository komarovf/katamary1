var React = require("react");


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
            selectCountClass: ""
        };
    },

    createSurvey: function(e) {
        e.preventDefault();
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

    handleAddQuestion: function(e) {
        e.preventDefault();
        if (this.state.questions.length >= this.props.maxCount) {
            alert("Достигнут максимум вопросов в анкете");
        } else {
            questions = this.state.questions;
            q = {};
            q.type = this.refs.q_type.getDOMNode().value;
            q.body = "";
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

    render: function() {
        var selectTypeOptions = this.props.types.map(function(type, index) {
            return (
                <option key={"type"+index} value={index}>{type}</option>
            );
        });
        var selectCount = this.props.aCount.map(function(c, index) {
            return (
                <option key={"count"+index} value={index}>{c}</option>
            );
        });
        return (
            <form ref="survey_form">
                <hr />
                <label htmlFor="name">Название опроса </label>
                <input type="text" id="name" />
                <br />
                <label htmlFor="intro_text">Описание опроса </label>
                <textarea id="intro_text"></textarea>
                <br />
                <label htmlFor="start_time">Дата начала опроса </label>
                <input type="date" id="start_time"/>
                <br />
                <label htmlFor="end_time">Дата завершения опроса </label>
                <input type="date" id="end_time"/>
                <br />
                <span>Лимит вопросов: {this.props.maxCount - this.state.questions.length}</span>
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
                        defaultValue={this.props.aCount[0]}
                        ref="a_count"
                        id="a_count"
                    >
                        {selectCount}
                    </select>
                </div>
                <button onClick={this.handleAddQuestion}>
                    Добавить вопрос
                </button>
                <hr />
                <QuestionList questions={this.state.questions} />
                <button onClick={this.createSurvey}>Сохранить опрос</button>
            </form>
        );
    }
});


var QuestionList = React.createClass({
    render: function() {
        var questions = this.props.questions.map(function(q, index) {
            return (
                <li key={"question"+index}>
                    <Question data={q} id={index}/>
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
        var value = this.props.data.body || "";
        var nodes = [
            <label htmlFor="question">Вопрос: </label>,
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
                    <p>Вопрос: </p>
                    <p>{value}</p>
                </div>
            );
        };
    },

    handleSaveClick: function(e) {
        e.preventDefault();
        var errors = {};

        // validation here!
        for (var ref in this.refs) {
            if (this.refs[ref].getDOMNode().value == "") {
                errors[ref] = "Нужно заполнить это поле!";
            };
        };
        this.setState({
            errors: errors
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
                    <button>Удалить вопрос</button>
                    <button>Редактировать вопрос</button>
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


React.render(
    <Survey
        types={questionTypes}
        aCount={answersNumber}
        maxCount={maxQuestionsCount}
    />,
    document.getElementById("survey_add")
);
