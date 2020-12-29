// import { Container, Col, Row, InputGroup, FormControl, Button} from 'react-bootstrap';
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
// Be sure to include styles at some point, probably during your bootstrapping

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

  closeBtn:{
    "&:hover": {
      cursor:'pointer'
    },
    
  }


}));

class MainForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      groups: [],
      contactRates: [[]],
      groupName: "",
      grid: [
        // [{value: 0}]
      ],
      ve: 0.0,
    };

    this.addGroup = this.addGroup.bind(this);
  }

  handleChange(event) {
    let fieldName = event.target.name;
    let fieldVal = event.target.value;
    this.setState({
      [fieldName]: fieldVal
    })
  }

  // handleChange = (event) => {
  //   setName(event.target.value);
  // };

  handlePopulationChange(event) {
    // let groupName = event.target.name;
    // let fieldVal = event.target.value;
  }

  addToPrev(prevGrid, newVal) {
    prevGrid.forEach(row => {
      while (row.length !== newVal) {
        row.push({ value: 0 })
      }
    })
    return prevGrid
  }

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
  }

  removeGroup() {

  }

  render() {
    const { classes } = this.props;
    return (
      <div className='wrapper'>
        <Container>
          <Grid container spacing={1}>
            <Grid item xs={4}>
              <h2>Population Groups</h2>
              {/* <form noValidate autoComplete="off"> */}
              <TextField
                fullWidth
                label="Group Name"
                name='groupName'
                value={this.state.groupName}
                onChange={this.handleChange.bind(this)}
                variant="outlined"
                InputProps={{ endAdornment: <Button onClick={this.addGroup}>Add</Button> }}
              />

              {/* </form> */}

              {this.state.groups.map((group) =>

                <Box mt={2}>
                  <TextField
                    fullWidth
                    // label={group.name}
                    // value={group.population}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">{group.name}:</InputAdornment>,
                      endAdornment: <Icon onClick={this.removeGroup} className={classes.closeBtn}>close</Icon>
                    }}
                  />

                </Box>

              )}

              <Box mt={2}>
                <TextField fullWidth required id="standard-required" label="Vaccine Efficiency" value={this.state.ve}
                onChange={this.handleChange.bind(this)} name='ve'
                 />
              </Box>



            </Grid>

            <Grid item xs={8}>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <h2>Contact Rates</h2>
                </Grid>
                <Grid item xs={6}>
                <Box mt={2}>
                  <Button className={classes.buttonMargin} variant="contained" color="primary">
                    Allocate
                    </Button>
                    </Box>
                </Grid>
              </Grid>
              <ReactDataSheet
                data={this.state.grid}
                valueRenderer={cell => cell.value}
                sheetRenderer={props => (
                  <table className={props.className + ' my-awesome-extra-class'}>
                    <thead>
                      <tr>
                        <th className='action-cell' />
                        {this.state.groups.map((group) => (<th>{group.name}</th>))}
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