import { useState } from 'react';
import './SignUp.css';
import { Link } from "react-router-dom"
import axios from 'axios';
const Signup = () => {

    const [name, setName] = useState("");
    const [age, setAge] = useState("")
    const [email, setEmail] = useState("");
    const [region, setRegion] = useState("")

    const [likes, setLikes] = useState([]);
    const [disLikes, setDisLikes] = useState([]);
    const [likesText, setLikesText] = useState("");
    const [disLikesText, setDisLikesText] = useState("");
    const [favouriteColor, setFavouriteColor] = useState("");
    const [attires, setAttires] = useState([])
    const [attiresText, setAttiresText] = useState("")
    // eslint-disable-next-line 
    const [gender, setGender] = useState("")

    const [pass, setPass] = useState("")

    const genderChange = (e) => {
        setGender(e.target.value)
    }

    const likesChange = (e) => {
        setLikesText(e.target.value)
        if (e.target.value[e.target.value.length - 1] === ",") {
            let like = e.target.value;
            like = like.replace(",", "")
            setLikes([
                ...likes,
                like
            ])
            setLikesText("")
        }
        console.log(likes)
    }
    const dislikesChange = (e) => {
        setDisLikesText(e.target.value)
        if (e.target.value[e.target.value.length - 1] === ",") {
            let dislike = e.target.value;
            dislike = dislike.replace(",", "")
            setDisLikes([
                ...disLikes,
                dislike
            ])
            setDisLikesText("")
        }
    }
    const attireChange = (e) => {
        setAttiresText(e.target.value)
        if (e.target.value[e.target.value.length - 1] === ",") {
            let attire = e.target.value;
            attire = attire.replace(",", "")
            setAttires([
                ...attires,
                attire
            ])
            setAttiresText("")
        }
    }

    const removeLike = (like) => {
        let tempLikes = likes.filter(l => l !== like);
        console.log(tempLikes)
        setLikes(tempLikes)
    }

    const signUpCall= async()=>{
        if(!name || !age || !email || !region)
        await axios.post("http://127.0.0.1:8000/signup")
    }

    return (
        <div className='loginbody'>
            <section className="logincontainer">
                <header>Sign up</header>
                <div className="form">
                    <div className="input-box">
                        <label>Full Name</label>
                        <input type="text" placeholder="Enter full name" value={name} onChange={(e) => setName(e.target.value)} />
                    </div>
                    <div className="input-box">
                        <label>Age</label>
                        <input type="number" placeholder="Enter your age" value={age} onChange={(e) => setAge(e.target.value)} />
                    </div>
                    <div className="input-box">
                        <label>Email Address</label>
                        <input type="text" placeholder="Enter email address" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    {/* <div className="column">
                    <div className="input-box">
                        <label>Phone Number</label>
                        <input type="number" placeholder="Enter phone number" required />
                    </div>
                </div> */}
                    <div className="gender-box">
                        <h3>Gender</h3>
                        <div className="gender-option" onChange={genderChange}>
                            <div className="gender">
                                <input type="radio" id="check-male" name="gender" value="male" />
                                <label htmlFor="check-male">Male</label>
                            </div>
                            <div className="gender">
                                <input type="radio" id="check-female" name="gender" value="female" />
                                <label htmlFor="check-female">Female</label>
                            </div>
                            <div className="gender">
                                <input type="radio" id="check-other" name="gender" value="prefer not to say" />
                                <label htmlFor="check-other">prefer not to say</label>
                            </div>
                        </div>
                    </div>

                    <div className="input-box address">
                        <label>Address</label>
                        <input type="text" placeholder="Enter your region" value={region} onChange={(e) => setRegion(e.target.value)} />
                    </div>

                    <div className='content'>
                        <h3>Likes & Dislikes</h3>
                        <ul>
                            {
                                likes.length !== 0 && likes.map((like, id) => (
                                    <li key={id}>{like} <i className="uit uit-multiply" onClick={() => removeLike(like)}></i></li>
                                ))
                            }
                            <input type="text" placeholder="Enter your likes" value={likesText} onChange={likesChange} required />
                        </ul>
                        <ul>
                            {
                                disLikes.length !== 0 && disLikes.map((dislike, id) => (
                                    <li key={id}>{dislike} <i className="uit uit-multiply" onClick={() => removeLike(dislike)}></i></li>
                                ))
                            }
                            <input type="text" placeholder="Enter your dislikes" value={disLikesText} onChange={dislikesChange} required />
                        </ul>
                    </div>

                    {/* favourite color */}
                    <div className='input-box'>
                        <label>Favourites</label>
                        <input type="text" placeholder="Enter your favourite color" value={favouriteColor} onChange={(e) => setFavouriteColor(e.target.value)} required />
                    </div>

                    {/* favourite attire */}
                    <div className='content'>
                        <ul>
                            {
                                attires.length !== 0 && attires.map((attire, id) => (
                                    <li key={id}>{attire} <i className="uit uit-multiply" onClick={() => removeLike(attire)}></i></li>
                                ))
                            }
                            <input type="text" placeholder="Enter your favourites attires" value={attiresText} onChange={attireChange} required />
                        </ul>
                    </div>

                    <div className="input-box">
                        <label>Password</label>
                        <input type="password" placeholder="Enter Password" value={pass} onChange={(e) => setPass(e.target.value)} />
                    </div>
                    <div className='signUpbutton' onClick={signUpCall}>Sign Up</div>
                </div>

                <div className='loginLink'>
                    Already have an account? <Link to="/login">Login here</Link>
                </div>
            </section>
        </div>
    )
}
export default Signup;