import { useState } from 'react';
import './SignUp.css';
import {Link} from "react-router-dom"
import axios from 'axios'
const Login = () => {

    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("")

    return (
        <div className='loginbody'>
            <section className="logincontainer">
                <header>Login</header>
                <div className="form">
                    <div className="input-box">
                        <label>Email Address</label>
                        <input type="text" placeholder="Enter email address" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    <div className="input-box">
                        <label>Password</label>
                        <input type="password" placeholder="Enter Password" value={pass} onChange={(e) => setPass(e.target.value)} />
                    </div>
                    
                    <div className='signUpbutton'>Login</div>
                </div>
                <div className='loginLink'>
                    New User? <Link to="/">Sign up here</Link>
                </div>
            </section>
        </div>
    )
}
export default Login;