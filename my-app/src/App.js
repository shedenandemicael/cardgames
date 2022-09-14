import './App.css';
import React from 'react'
// import { render } from '@testing-library/react';

function App() {
  return (
    <div className="App">

      <Navbar />

      <CommunityCards />

      <div id="hands">
        <Hand hand="s2"/>
        <Hand hand="c5"/>
        <Hand hand="d10"/>
        <Hand hand="d9"/>
        <Hand hand="sA"/>
      </div>
    </div>
  );
}

class Hand extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: this.props.hand,
    };
  }

  render() {
    return (
    <div class="hand"> {this.state.text} </div>
    );
  }
}

class Navbar extends React.Component {
  render() {
    return (
      <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
          <a id="title" href='/game'>Poker Now</a>
        </div>
      </nav>
    );
  }
}

class Card extends React.Component {
  render () {
    return (
      <div class="hand">S6</div>
    );
  }
}

class CommunityCards extends React.Component {
  render() {
    return (
      <div id="community-cards">
        <Card />
        <Card />
        <Card />
        <Card />
        <Card />
      </div>
    );
  }
}

export default App;
