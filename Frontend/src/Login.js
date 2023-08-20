import { useState } from 'react';
import './SignUp.css';
import {Link} from "react-router-dom"
import axios from 'axios'
const Login = () => {

    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");

    const handleSubmit = async(req,res) => {
        const data={
            uname: email,
            pwd: pass
        }
        await axios.post("http://127.0.0.1:8000/login", data)
        .then(res => { 
            console.log(res) 
            localStorage.setItem('uname', email)
        })
        .catch(err=>{
            console.log(err)
        })
    }

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

                    <div className='signUpbutton'
                        onClick={(e) => handleSubmit(e)}>
                        Login
                    </div>
                </div>
                <div className='loginLink'>
                    New User? <Link to="/">Sign up here</Link>
                </div>
            </section>
        </div>
    )
}
export default Login;