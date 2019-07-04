import React from "react";
import PropTypes from "prop-types";

import { getDevice } from "frontend/utils/api";
import { connect } from "react-redux";
import PixelColorGraph from "frontend/components/PixelColorGraph/PixelColorGraph.jsx";
import { getDevices } from "../../utils/api";

class PixelColorGraphView extends React.Component {
  constructor() {
    super();
    this.state = {
      devices: null
    };
  }

  componentDidMount() {
    getDevices()
      .then(devices => {
        this.setState({ devices });
      })
      .catch(error => console.log(error));
  }

  createList = devices => {
    let deviceList = [];
    devices.forEach(device => {
      deviceList.push(<PixelColorGraph device={device} />);
    });
  };

  render() {
    const { classes } = this.props;
    const { device_id } = this.props.match.params;
    const { devices } = this.state;

    if (devices) {
      return <div />;
    }
    return <p>Loading</p>;
  }
}

export default PixelColorGraphView;
