import { Container, Col, Row, InputGroup, FormControl, Button} from 'react-bootstrap';
import React from 'react';

export default class MainForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        groups: [{ name: "Group 1", population: 100 }],
        contactRates: [[]],
        groupName:"",
      };
  
      this.addGroup = this.addGroup.bind(this);
    }
  
    handleChange(event) {
      let fieldName = event.target.name;
      let fieldVal = event.target.value;
      this.setState({
        [fieldName]:fieldVal
      })
    }
  
    handlePopulationChange(event) {
      let groupName = event.target.name;
      let fieldVal = event.target.value;
    }
  
    addGroup() {
      let name = this.state.groupName
      if (name == "") return
      this.setState(prevState => ({
        groupName:"",
        groups: [...prevState.groups, {
          name,
          population: 200
        }]
      }))
    }
  
    render() {
      return (
        <div class='wrapper'>
          <Container>
            <Row>
              <Col sm={4}>
                <h2>Groups</h2>
                <InputGroup className="mb-3">
                  <FormControl
                  name='groupName' 
                    placeholder="Group Name"
                    value={this.state.groupName}
                    onChange={this.handleChange.bind(this)}
                  />
                  <InputGroup.Append>
                    <Button variant="outline-secondary" onClick={this.addGroup}>Add</Button>
                  </InputGroup.Append>
                </InputGroup>
  
                {this.state.groups.map((group) =>
                  <InputGroup className="mb-3">
                  <InputGroup.Prepend>
                    <InputGroup.Text id="basic-addon1">{group.name}</InputGroup.Text>
                  </InputGroup.Prepend>
                  <FormControl
                    name={group.name}
                    value={group.population}
                    aria-label="Username"
                    aria-describedby="basic-addon1"
                    onChange={this.handlePopulationChange.bind(this)}
                  />
                </InputGroup>
                )}
  
                
  
  
              </Col>
  
  
  
  
              <Col sm={8}>
                <h2>Contact Rates</h2>
              </Col>
            </Row>
          </Container>
        </div>
      );
    }
  }