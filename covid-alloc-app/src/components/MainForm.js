import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/styles';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import InputAdornment from '@material-ui/core/InputAdornment';
import Icon from '@material-ui/core/Icon';
import ReactDataSheet from 'react-datasheet';

import axios from "axios"
import React from 'react';

const styles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  group: {
    marginTop: 10
  },
  buttonMargin: {
    marginTop: 10,
  },
}));

class MainForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      groups: [],
      groupName: "",
      grid: [
        // [{value: 0}]
      ],
      ve: 0.50,
      results: null,
    };

    this.addGroup = this.addGroup.bind(this);
  }

  // handling change for text box values (Group, vaccine efficacy)
  handleChange(event) {
    let fieldName = event.target.name;
    let fieldVal = event.target.value;
    this.setState({
      [fieldName]: fieldVal
    })
  }

  // handling change for population size values
  handlePopulationChange(event) {
    let groupName = event.target.name;
    let fieldVal = event.target.value;
    let grpsClone = JSON.parse(JSON.stringify(this.state)).groups
    let index = -1
    grpsClone.find(function (item, i) {
      if (item.name === groupName) {
        index = i
        return i
      }
    });

    grpsClone[index].population = fieldVal

    this.setState({
      groups: grpsClone
    })
  }

  // helper function for contact grid
  addToPrev(prevGrid, newVal) {
    prevGrid.forEach(row => {
      while (row.length !== newVal) {
        row.push({ value: 0 })
      }
    })
    return prevGrid
  }

  // adding new population group, updating state for groups array and contact grid
  addGroup() {
    let name = this.state.groupName
    if (name === "") return
    this.setState(prevState => ({
      groupName: "",
      groups: [...prevState.groups, {
        name,
        population: 200
      }],
      grid: [
        ...this.addToPrev(prevState.grid, prevState.groups.length + 1),
        Array.apply(null, Array(prevState.groups.length + 1)).map(function () { return { value: 0 } })
      ]
    }))

    console.log(this.state.grid)
  }

  // for removing population groups
  removeGroup = name => () => {
    console.log(name)
    let groupName = name;
    let grpsClone = JSON.parse(JSON.stringify(this.state)).groups
    let index = -1
    grpsClone.find(function (item, i) {
      if (item.name === groupName) {
        index = i
        return i
      }
    });
    grpsClone.splice(index, 1);
    this.setState(prevState => ({
      groups: grpsClone,
      grid: [
        ...this.removeFromPrev(prevState.grid, prevState.groups.length - 1),
      ]
    }))
  }

  // helper function for contact grid
  removeFromPrev(prevGrid, newVal) {
    while (prevGrid.length !== newVal) {
      prevGrid.pop()
    }

    prevGrid.forEach(row => {
      while (row.length !== newVal) {
        row.pop()
      }
    })
    return prevGrid
  }


  // for allocate button
  allocate() {
    console.log(this.state)

    // build API URL
    let apiURL = "http://34.123.195.162:5000/solve?groups=["

    this.state.groups.forEach((group, index) => {
      apiURL += "%22" + group.name + "%22"
      if (index !== this.state.groups.length - 1) {
        // apiURL += ","
        apiURL += "%2C"
      }
    });

    apiURL += "]&N0=[";

    this.state.groups.forEach((group, index) => {
      apiURL += group.population
      if (index !== this.state.groups.length - 1) {
        // apiURL += ","
        apiURL += "%2C"
      }
    });

    apiURL += "]&fn0=[0.5%2C0.5]&Kmatval=[";
    this.state.grid.forEach((row, ri) => {
      // console.log(row)
      row.forEach((cell, ci) => {
        apiURL += cell.value
        if (ri !== this.state.grid.length - 1 || ci !== row.length - 1) {
          // apiURL += ","
          apiURL += "%2C"
        }
      })
    });

    apiURL += "]&H=" + this.state.ve;
    let sample = "http://34.123.195.162:5000/solve?groups=[%22A%22%2C%22B%22]&N0=[200%2C200]&fn0=[0.5%2C0.5]&Kmatval=[1.0%2C0.9%2C0.8%2C0.9]&H=0.98"
    console.log(sample)
    console.log(apiURL)
    axios
      .get(apiURL)
      .then((response) => {
        // console.log(response)
        // this.setState({
        //   results: response.data
        // })
        alert(response.data.result[1])
        console.log(response.data.result)
      })
      .catch((error) => {
        console.log(error);
      });
  }

  handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      this.addGroup()
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <div className='wrapper'>
        <Container>
          <Grid container spacing={1}>
            {/* Left Column */}
            <Grid item xs={4}>
              {/* Population Group text input */}
              <h2>Population Groups</h2>
              {/* <form noValidate autoComplete="off"> */}
              <TextField
                fullWidth
                label="Group Name"
                name='groupName'
                value={this.state.groupName}
                onChange={this.handleChange.bind(this)}
                variant="outlined"
                onKeyPress={this.handleKeyPress}
                InputProps={{ endAdornment: <Button onClick={this.addGroup}>Add</Button> }}
              />
              {/* </form> */}

              {/* Population size input for every group */}
              {this.state.groups.map((group) =>
                <Box mt={2} key={group.name}>
                  <TextField
                    fullWidth
                    // label={group.name}
                    value={group.population}
                    onChange={this.handlePopulationChange.bind(this)}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">{group.name}:</InputAdornment>,
                      endAdornment: <Icon onClick={this.removeGroup(group.name)} className={classes.closeBtn}>close</Icon>
                    }}
                    name={group.name}
                  />
                </Box>
              )}

<h2>Vaccine Efficacy</h2>
              {/* Vaccine efficacy input */}
              <Box mt={2}>
                <TextField fullWidth required id="standard-required" label="Vaccine Efficiency" value={this.state.ve}
                  onChange={this.handleChange.bind(this)} name='ve'
                />
              </Box>

              {
                this.state.results && this.state.results.status === true ?
                  <div>
                    <h2>Results</h2>
                    {this.state.results.result.map((result) =>
                      <p>{result}</p>
                    )}

                  </div>
                  :
                  this.state.results ?
                    <div>
                      <h2>Error!</h2>
                      <p>{this.state.results.errors}</p>
                    </div>
                    :
                    <div></div>

              }


            </Grid>

            {/* Right Column */}
            <Grid item xs={8}>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <h2>Contact Rates</h2>
                </Grid>
                {/* Allocate button */}
                <Grid item xs={6}>
                  <Box mt={2}>
                    <Button onClick={this.allocate.bind(this)} className={classes.buttonMargin} variant="contained" color="primary">
                      Allocate
                    </Button>
                  </Box>
                </Grid>
              </Grid>

              {/* Contact rates data sheet */}
              <ReactDataSheet
                data={this.state.grid}
                valueRenderer={cell => cell.value}
                sheetRenderer={props => (
                  <table className={props.className + ' my-awesome-extra-class'}>
                    <thead>
                      <tr>
                        <th className='action-cell' />
                        {this.state.groups.map((group) => (<th key={group.name}>{group.name}</th>))}
                      </tr>
                    </thead>
                    <tbody>
                      {props.children}
                    </tbody>
                  </table>
                )}
                rowRenderer={props => (
                  <tr>
                    <td className='read-only'>
                      <span className="value-viewer">{this.state.groups[props.row] ? this.state.groups[props.row].name : null}</span>
                    </td>
                    {props.children}

                  </tr>
                )}
                onCellsChanged={changes => {
                  const grid = this.state.grid.map(row => [...row]);
                  changes.forEach(({ cell, row, col, value }) => {
                    grid[row][col] = { ...grid[row][col], value };
                  });
                  this.setState({ grid });
                }}
              />

            </Grid>
          </Grid>
        </Container>
      </div>
    );
  }
}

MainForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(MainForm);