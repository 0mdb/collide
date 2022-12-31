import React from 'react';
import { Link } from 'react-router-dom'
import { Icon } from '@blueprintjs/core';
import useDarkMode from '../../hooks/useDarkMode';
import SearchBar from '../Search';

const TopNavigation = () => {
  return (
    <div className='top-navigation'>
      <Title />
      <ThemeIcon />
      <Search />
      {/* <BellIcon /> */}
      {/* <ThemeIcon /> */}
      {/* <SankeyGraph /> */}
      <UserCircle />
    </div>
  );
};

const ForceGraph = () => {
  return (
    <Link to='/'>
      <Icon icon="graph" size={24} className='top-navigation-icon' text='Force' />
    </Link>
  )
};


const SankeyGraph = () => {
  return (
    <Link to='/sankey'>
      <Icon icon="diagram-tree" size={24} className='top-navigation-icon' text='Sankey' />
      </Link>
  )
};


const ThemeIcon = () => {
  const [darkTheme, setDarkTheme] = useDarkMode();
  const handleMode = () => setDarkTheme(!darkTheme);
  return (
    <span onClick={handleMode}>
      {darkTheme ? (
        <Icon icon="flash" size={24} className='top-navigation-icon' />
      ) : (
        <Icon icon="moon" size={24} className='top-navigation-icon' />
      )}
    </span>
  );
};
const Search = () => (
  <div className='search'>
    <input className='search-input' type='text' placeholder='Search...' />
    <Icon icon='search' size={18} className='text-secondary my-auto' />
  </div>
);
const BellIcon = () => <Icon icon="notifications" size={24} className='top-navigation-icon' />;
const UserCircle = () => <Icon icon="user" size={24} className='top-navigation-icon' />;
const Title = () => <h5 className='title-text'>collide.io</h5>;

// export { default as NavGroup } from './NavGroup'
export default TopNavigation;
