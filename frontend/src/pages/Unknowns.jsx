import qs from "qs"
import { useState, useEffect } from "react"
import api from "../api"

import UnknownCasesFilter from "../components/Unknowns/UnknownCasesFilter";
import UnknownCasesList from "../components/Unknowns/UnknownsCaseList";

import "../styles/Unknowns.css"

export default function Unknowns () {

    const [ data, setData ] = useState([]);
    const [ filters, setFilters ] = useState({});
    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState(null);

    const handleFilters = (newFilters) => {
        setFilters(newFilters)
    }

    useEffect(()=> {
        const fetchData = async () => {
            setLoading(true);
            setError(false);
            try {
                const hasFilters = Object.keys(filters).length > 0
                const query = hasFilters ? qs.stringify(filters,{skipNulls:true, addQueryPrefix: true}) : "";
                const response = await api.get("modules/", { params: filters });
                setData(response.data);
            } catch (e) {
                setError(e)
                console.error("Error loading data ", e);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, [filters]);

    return (
       <div className="unknowns-container">
            <div className="uknowns-filter">
                <UnknownCasesFilter searchApi={handleFilters}/>
            </div>
            <div className="unknowns-case-list">
                {loading && <p>Loading...</p>}
                {error && <p style={{ color: "red" }}>{error}</p>}
                {!loading && data.length === 0 && <p>No modules found</p>}
                <UnknownCasesList modules= {data}/>
            </div>
        </div>
    )

}