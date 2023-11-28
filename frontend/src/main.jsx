import React from "react";
import ReactDOM from "react-dom/client";
import { RecoilRoot } from "recoil";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { StyledEngineProvider } from "@mui/material/styles";
import "./index.css";
import App from "./App.jsx";
import TweetList from "./pages/TweetList.jsx";
import ScheduleTweet from "./pages/ScheduleTweet.jsx";
import Tweet from "./pages/Tweet";
import Settings from "./pages/Settings";
import Login from "./pages/Login";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: <App />,
    errorElement: <>Error Page</>,
    children: [
      {
        path: "/schedule",
        element: <ScheduleTweet />,
      },
      {
        path: "/",
        element: <TweetList />,
      },
      {
        path: "/tweet/:id",
        element: <Tweet />,
      },
      {
        path: "/settings",
        element: <Settings />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RecoilRoot>
      <StyledEngineProvider injectFirst>
        <RouterProvider router={router} />
      </StyledEngineProvider>
    </RecoilRoot>
  </React.StrictMode>
);
