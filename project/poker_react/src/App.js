import './App.css';
import React from 'react'
//import { render } from '@testing-library/react';

function App() {
  return (
    <div className="App">

      <nav className="navbar navbar-dark bg-dark">
        <div className="container-fluid">
          <a id="title" href='/game'>Poker Now</a>
        </div>
      </nav>

      <CommunityCards />

      <div id="hands">
        <Hand hand="s2"/>
        <Hand hand="c5"/>
        <Hand hand="d10"/>
        <Hand hand="d9"/>
        <Hand hand="sA"/>
      </div>

      <PlayArea />
    </div>
  );
}

class PlayArea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playbutton: true,
    };
  }

  render() {
    return (
      <form action="./api/gamedata.json" id="startButton" method="POST">
        <input name="players" type="number"/>
        <button name="play" onClick={handleStart()} type="submit" value="begin" />
      </form>
    );
  }
}

function handleStart() {
  document.getElementById("startButton");
  let data = {players: "3"};
  fetch("./api/gamedata.json", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
  }).then(res => {
    console.log("Request complete! response:", res);
  });
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
    <div className="hand"> {this.state.text} </div>
    );
  }
}

class Card extends React.Component {
  render () {
    return (
      <div className="hand">S6</div>
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
