import { useState } from "react"
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Register() {

    const [ username, setUsername ] = useState("");
    const [ email, setEmail ] = useState("");
    const [ password, setPassword ] = useState("")
    const [ loading, setLoading ] = useState(false);
    const [ msg, setMsg ] = useState("");

    const submit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {

        } catch (err) {
            setMsg.apply(err.response?.data?.detail || "Registration failed")
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="register-container">
            <h3>Register</h3>
            <form onSubmit={submit}>
                <input 
                    type = "text"
                    placeholder="Choose username"
                    value = {username}
                    onChange = {(e) => setUsername(e.target.value)}
                />
                <input 
                    type = "email"
                    placeholder = "Email verification address"
                    value = {email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type = "password"
                    placeholder="Choose password"
                    value = {password} 
                    onChange = {(e)=> setPassword(e.target.value)}
                />
                <button>Submit</button>
            </form>

        </div>
    )

}