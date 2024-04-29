import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Button as BaseButton } from '@mui/base/Button';
import { Link } from "react-router-dom";
import { Dropdown } from '@mui/base/Dropdown';
import { Menu } from '@mui/base/Menu';
import { MenuButton as BaseMenuButton } from '@mui/base/MenuButton';
import { MenuItem as BaseMenuItem, menuItemClasses } from '@mui/base/MenuItem';
import { styled } from '@mui/system';
import Constant_Colours from './component/color.js'
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import Drawer from '@mui/material/Drawer';
import ApiIcon from '@mui/icons-material/Api';
import ChatIcon from '@mui/icons-material/Chat';
import ArticleIcon from '@mui/icons-material/Article';
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing';
import LayersIcon from '@mui/icons-material/Layers';
import KeyIcon from '@mui/icons-material/Key';
import EmailIcon from '@mui/icons-material/Email';
import VerticalNav from './component/vertical_nav.js';
const blue = Constant_Colours.blue;
const grey = Constant_Colours.grey;


const Listbox = styled('ul')(
  ({ theme }) => `
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.875rem;
  box-sizing: border-box;
  padding: 6px;
  margin: 12px 0;
  min-width: 80px;
  border-radius: 12px;
  overflow: auto;
  outline: 0px;
  background: ${theme.palette.mode === 'dark' ? grey[900] : '#fff'};
  border: 1px solid ${theme.palette.mode === 'dark' ? grey[700] : grey[200]};
  color: ${theme.palette.mode === 'dark' ? grey[300] : grey[900]};
  box-shadow: 0px 4px 6px ${theme.palette.mode === 'dark' ? 'rgba(0,0,0, 0.50)' : 'rgba(0,0,0, 0.05)'
    };
  z-index: 1;
  `,
);

const MenuItem = styled(BaseMenuItem)(
  ({ theme }) => `
  list-style: none;
  padding: 8px;
  border-radius: 8px;
  cursor: default;
  user-select: none;

  &:last-of-type {
    border-bottom: none;
  }

  &:focus {
    outline: 3px solid ${theme.palette.mode === 'dark' ? blue[600] : blue[200]};
    background-color: ${theme.palette.mode === 'dark' ? grey[800] : grey[100]};
    color: ${theme.palette.mode === 'dark' ? grey[300] : grey[900]};
  }

  &.${menuItemClasses.disabled} {
    color: ${theme.palette.mode === 'dark' ? grey[700] : grey[400]};
  }
  `,
);

const MenuButton = styled(BaseMenuButton)(
  ({ theme }) => `

  font-size: 14px;
  line-height: 1;
  padding: 8px;
  border-radius: 8px;
  transition: all 150ms ease;
  cursor: pointer;
  background: transparent;
  border: 0px solid ${theme.palette.mode === 'dark' ? grey[700] : grey[200]};
  color: ${theme.palette.mode === 'dark' ? grey[100] : grey[100]};

  &:hover {
    background: ${theme.palette.mode === 'dark' ? grey[800] : grey[100]};
    color: ${theme.palette.mode === 'dark' ? grey[200] : grey[900]};
    border-color: ${theme.palette.mode === 'dark' ? grey[600] : grey[300]};
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  }

  &:active {
    background: ${theme.palette.mode === 'dark' ? grey[700] : grey[100]};
    color: ${theme.palette.mode === 'dark' ? grey[100] : grey[900]}
  }

  &:focus-visible {
    box-shadow: 0 0 0 4px ${theme.palette.mode === 'dark' ? blue[300] : blue[200]};
    outline: none;
  }
  `,
);

const NavLink = styled(Link)(
  ({ theme }) => `
    display: flex;
    align-items: center;
    text-decoration: none;
    width:100%;
    cursor: pointer;
    color: ${theme.palette.mode === 'dark' ? grey[200] : grey[900]};
    &.active {
        color: #4d4dff;
    }
`
);
const Button = styled(BaseButton)(
  ({ theme }) => `

  font-size: 14px;
  line-height: 1;
  padding-top: 8px;
  padding-bottom: 4px;
  padding-left: 8px;
  padding-right: 8px;
  border-radius: 8px;
  transition: all 150ms ease;
  cursor: pointer;
  border: 0px;
  background: transparent;
  color: ${theme.palette.mode === 'dark' ? grey[100] : grey[100]};

  &:hover {
    background: ${theme.palette.mode === 'dark' ? grey[800] : grey[100]};
    color: ${theme.palette.mode === 'dark' ? grey[200] : grey[900]};
    border-color: ${theme.palette.mode === 'dark' ? grey[600] : grey[300]};
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  }

  &:active {
    background: ${theme.palette.mode === 'dark' ? grey[700] : grey[100]};
  }

  &:focus-visible {
    box-shadow: 0 0 0 4px ${theme.palette.mode === 'dark' ? blue[300] : blue[200]};
    outline: none;
  }
  `,
);
function ResponsiveAppBar() {
  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };


  const [open, setOpen] = React.useState(false);
  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };
  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      <VerticalNav />
    </Box>
  );
  return (

    <AppBar position="sticky" >
      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2, display: { xs: 'block', sm: 'none' } }}
            onClick={toggleDrawer(true)}
          >

            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Inference
          </Typography>


          <Dropdown>
            <MenuButton sx={{ display: { xs: 'none', sm: 'block' } }}>Information</MenuButton>
            <Menu slots={{ listbox: Listbox }}>
              <MenuItem> <NavLink to="/frontend">Introduction</NavLink></MenuItem>
              <MenuItem> <NavLink to="/frontend/manual">Manual</NavLink></MenuItem>
              <MenuItem> <NavLink to="/frontend/model">Model</NavLink></MenuItem>
            </Menu>
          </Dropdown>
          <Dropdown>
            <MenuButton sx={{ display: { xs: 'none', sm: 'block' } }}>Modes</MenuButton>
            <Menu slots={{ listbox: Listbox }}>
              <MenuItem ><NavLink to="/frontend/hub">Chat & Log</NavLink></MenuItem>
              <MenuItem >API</MenuItem>
            </Menu>
          </Dropdown>


          <Button
            key='key-management'
            href="/frontend/key-management"
            onClick={handleCloseNavMenu}
            sx={{
              textDecoration: 'none',
              display: { xs: 'none', sm: 'block' }
            }}
          >
            Key & Credit
          </Button>
          <Button
            key='contact'
            href="/frontend/contact"
            onClick={handleCloseNavMenu}
            sx={{
              textDecoration: 'none',
              display: { xs: 'none', sm: 'block' }
            }}
          >
            Contact
          </Button>


        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default ResponsiveAppBar;