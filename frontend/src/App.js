import React, { Component } from "react";

import GoogleApiWrapper from './components/Map';
import { getPropertyNeighbords } from './services/property-service';


class App extends Component {

  constructor() {
    super();
    this.state = { data: [] };
  }

  componentDidMount() {
    const queryParams = new URLSearchParams(window.location.search)

    const id = queryParams.get("id")
    const distance = queryParams.get("distance") || 60000

    if (!id) {
      throw new Error('Should provide property `id` param')
    }

    getPropertyNeighbords(id, distance)
      .then(json => this.setState({ data: json.data || {} }))
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
        <div style={{ height: '100vh', width: '100%' }}>
          <GoogleApiWrapper 
            data={this.state.data}
            defaultZoom={10}
          >
          </GoogleApiWrapper>
        </div>
        </header>
      </div>
    );
  }
}

export default App;
