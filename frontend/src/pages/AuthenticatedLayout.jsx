import { Children } from "react";
import Navbar from "../components/Navbar";

export default function AuthenticatedLayout({ children }) {
    return (
        <>
            <Navbar />
            <div style={{paddingTop: "20px"}}>
                { children }
            </div>
        
        </>
    )
}