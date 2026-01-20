import { Routes, Route } from "react-router-dom";

import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";

function App() {
  return (
    <Routes>
      {/* Home (React render edilir, Django index.html verir) */}
      <Route path="/" element={<LoginPanel />} />

      {/* Login */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Register */}
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
