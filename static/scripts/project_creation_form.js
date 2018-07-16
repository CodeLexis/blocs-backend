'use strict';

const e = React.createElement;

class ProjectCreationForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return (<b>Hi</b> Tomisin!)
  }
}

const domContainer = document.getElementById('project_creation_form');
ReactDOM.render('<ProjectCreationForm/>', domContainer);