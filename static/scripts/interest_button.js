class InterestButton extends React.Component {
  constructor(props) {
    super(props);

    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      form.submit()
      return 'Done!';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'SUBMIT'
    );
  }
}

//const domContainer = document.querySelector('#submit_button');
ReactDOM.render(<InterestButton />, document.getElementById('interest_button'));
//ReactDOM.render(e(SubmitButton), domContainer);