class MyForm extends React.Component {
  render() {
    return (
      <form className="form">
        <input className="input"/>
      </form>
    );
  }
}

//var realPython = React.createClass({
//  render: function() {
//    return (<input>Greetings, from Real Python!</input>);
//  }
//});

ReactDOM.render(<MyForm />, document.getElementById('content__'));
