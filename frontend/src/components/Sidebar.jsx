import "./Sidebar.css";
import { Link } from "react-router-dom";
import logo from "../assets/logo.jpg";
import {
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import ListAltIcon from "@mui/icons-material/ListAlt";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import SettingsIcon from "@mui/icons-material/Settings";

function Sidebar() {
  return (
    <div className="Sidebar">
      <img className="Logo" src={logo} />
      {/* <h2>Twitter App</h2> */}
      <ul className="NavListContainer">
        <List>
          <Link to="/">
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <ListAltIcon />
                </ListItemIcon>
                <ListItemText primary="Tweet List" />
              </ListItemButton>
            </ListItem>
          </Link>
          <Link to="/schedule">
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <AccessTimeIcon />
                </ListItemIcon>
                <ListItemText primary="Schedule Tweet" />
              </ListItemButton>
            </ListItem>
          </Link>
          <Link to="/settings">
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <SettingsIcon />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItemButton>
            </ListItem>
          </Link>
        </List>
      </ul>
      {/* <Link to="settings">Settings</Link> */}
    </div>
  );
}

export default Sidebar;
