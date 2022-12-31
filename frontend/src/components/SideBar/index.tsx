import React from 'react';
import { Link } from 'react-router-dom'
import { Icon } from '@blueprintjs/core';

const SideBar = () => {
  return (
    <div className="fixed top-0 left-0 h-screen w-16 flex flex-col
                  bg-white dark:bg-gray-900 shadow-lg">
                    
        
          <Link to='/'>
        <SideBarIcon icon={<Icon icon='home' size={28} />} text={'Home'} />
          </Link>
        <Divider />
        <SideBarIcon icon={<Icon icon='plus' size={32} />} />
        <SideBarIcon icon={<Icon icon='export' size={20} />} />

    <Link to='/sankey'>
      <SideBarIcon icon={<Icon icon="diagram-tree" size={28} />} text='Sankey' />
      </Link>
        <Divider />
        <SideBarIcon icon={<Icon icon ='cog' size={28} />} text='Settings ' />
    <Link to='/admin'>
        <SideBarIcon icon={<Icon icon='database' size={28} />} text='Admin' />
    </Link>
        <SideBarIcon icon={<Icon icon='help' size={28} />} text='Help' />
    </div>
  );
};

const SideBarIcon = ({ icon, text = 'tooltip 💡' }) => (
  <div className="sidebar-icon group">
    {icon}
    <span className="sidebar-tooltip group-hover:scale-100">
      {text}
    </span>
  </div>
);


const Divider = () => <hr className="sidebar-hr" />;

export default SideBar;