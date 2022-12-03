import React from 'react';
import {
  Classes,
  Icon,
  H6,
  Menu,
  Colors,
  MenuDivider,
  MenuItem,
} from '@blueprintjs/core';
import 'normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';

function SideBar() {
  return (
    <div className="SideBar">
      <Menu
        className={Classes.ELEVATION_1}
        style={{ background: Colors.DARK_GRAY4 }}
      >
        <li className={Classes.MENU_HEADER}>
          <H6 className={Classes.HEADING}>Projects</H6>
        </li>
        <MenuDivider />
        <MenuItem icon="new-text-box" text="New text box" />
        <MenuItem icon="new-object" text="New object" />
        <MenuItem icon="new-link" text="New link" />
        <MenuDivider />
        <MenuItem
          icon="cog"
          labelElement={<Icon icon="share" />}
          text="Settings..."
          intent="primary"
        />
      </Menu>
    </div>
  );
}

export default SideBar;
