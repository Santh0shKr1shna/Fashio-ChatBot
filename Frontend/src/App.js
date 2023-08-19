import './App.css';
import Chat from './Chat';
import Signup from './Signup';
import Login from './Login';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {

  return (
    <Router>
      <Routes>
        <Route exact path='/' element={<Signup />} />
        <Route exact path='/login' element={<Login />} />
        <Route exact path="chat" element={<Chat />} />
      </Routes>
    </Router>
    // <Chat />
  );
}

export default App;



