import "./Login.css";
import { useState } from "react";
import { useRecoilState } from "recoil";
import { Button, TextField, Card } from "@mui/material";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.jpg";
import { ApiConnector } from "../api/ApiConnector";
import { authTokenAtom } from "../store/atoms/authAtom";

function Login() {
  const navigate = useNavigate();
  const { login } = ApiConnector();

  const [, setAuthToken] = useRecoilState(authTokenAtom);

  const [usernameInput, setUsernameInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");
  const [loginError, setLoginError] = useState("");

  function getAuthToken() {
    // navigate("/");
  }

  return (
    <div className="Login">
      <img className="Logo" src={logo} />
      <div className="FormContainer">
        <TextField
          label="Username"
          style={{ marginBottom: 20 }}
          value={usernameInput}
          onChange={(event) => setUsernameInput(event.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          style={{ marginBottom: 20 }}
          value={passwordInput}
          onChange={(event) => setPasswordInput(event.target.value)}
        />
        {loginError && <small>{loginError}</small>}
        <Button variant="contained" onClick={getAuthToken}>
          Sign in
        </Button>
      </div>
    </div>
  );
}

export default Login;
