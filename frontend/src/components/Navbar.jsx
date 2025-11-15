import { Link } from "react-router-dom";
import "../styles/Navbar.css"

export default function Navbar() {
    return (
        <nav className="navbar">
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/unknowns">Unknowns</Link></li>
            </ul>
        </nav>
    )   
}