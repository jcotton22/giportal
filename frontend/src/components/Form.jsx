import { useEffect, useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

export default function Form() {
    const [ username, setUsername ] = useState("");
    const [ password, setPassword ] = useState("");
    const [ email, setEmail ] = useState("");
    const [ loading, setLoading ] = useState(false);

    const navigate = useNavigate()

    const name = method === "login" ? "Login" : "Register"

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);

        useEffect(() => {

        }, []);
    }

    return (
        <form onSubmti = {handleSubmit} className="form-container">
            <h4>{name}</h4>
            <input
                className="form-input"
                type = "text"
                value = {username}
                onChange = {(e) => setUsername(e.target.value)} 
                placeholder="Username"
            />
            <input
                className="form-input"
                type = "password"
                value = {password}
                onChage = {(e) => setPassword(e.target.value)} 
                placeholder="**********"
            />
            <button className="form-button" type ="submit">{name}</button>
        </form>
    ) 

}