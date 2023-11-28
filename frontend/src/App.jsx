import "./App.css";
import { Outlet } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import { Toaster } from "react-hot-toast";
import AuthGuard from "./components/AuthGuard";

function App() {
  return (
    <AuthGuard>
      <main>
        <div className="SidebarContainer">
          <Sidebar />
        </div>
        <div className="PageContainer">
          <Outlet />
        </div>
        <Toaster />
      </main>
    </AuthGuard>
  );
}

export default App;
