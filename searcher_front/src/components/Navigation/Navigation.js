import { Navbar, Nav, Container} from 'react-bootstrap';

function Navigation() {
  const navbarStyle = {
    height: '80px',
  };

  return (
    <Navbar expand="lg" bg="dark" variant="dark" style={navbarStyle}>
      <Container>
        <Navbar.Brand href="/">Searcher App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav>
            <Nav.Link href="/searcher">Поисковик</Nav.Link>
            {/* <Nav.Link href="/swagger">Документация</Nav.Link> */}
          </Nav>
          </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;