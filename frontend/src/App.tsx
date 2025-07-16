import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Operators from "./pages/Operators";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <div style={{ display: "flex" }}>
        <Sidebar />
        <div style={{ flex: 1, padding: "20px" }}>
          <Routes>
            <Route path="/" element={<Operators />} />
          </Routes>
        </div>
      </div>
      {/* Add ToastContainer here */}
      <ToastContainer />
    </Router>
  );
};

export default App;
