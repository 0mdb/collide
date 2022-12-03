import { Outlet } from 'react-router-dom';
import Nav from '../../components/Nav';

function Layout() {
  return (
    <main className="App">
      <Nav />
      <Outlet />
    </main>
  );
}

export default Layout;
