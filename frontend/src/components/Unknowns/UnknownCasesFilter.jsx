
import { useState, useMemo } from "react";
import Select from "react-select";
import useDropdownOptions from "./useDropdownOptions";

const initialFilters = {
    "organ-systems" : null,
    "staff-uploaders" : null
}

export default function UnknownCasesFilter( { searchApi } ) {

    const [ filters, setFilters ] = useState(initialFilters);

    const staffOptions = useDropdownOptions("staff-uploaders/")
    const organSystemOptions = useDropdownOptions("organ-systems/")

    const handleInput = (name) => (data) => {
        // data is either an option object or null when cleared
        setFilters((f) => ({ ...f, [name]: data }));
    };

    const payload = useMemo(() => {
        const raw = {
            "organ-systems": filters["organ-systems"]?.label ?? null,
            "staff-uploaders": filters["staff-uploaders"]?.label ?? null,
        };
        return Object.fromEntries(Object.entries(raw).filter(([_, v]) => v !== "" && v != null))
       
    },[filters]);

    const onSubmit = (e) => {e.preventDefault(); searchApi?.(payload)};
    const onReset = (e) => {e.preventDefault(); setFilters(initialFilters)};


    return (
        <form className="unknown-cases-filter" onReset={onReset} onSubmit={onSubmit}>
            <h3>Filter</h3>
            <details className="acc">
                <summary className="acc__summary">
                    <Select 
                        options = {staffOptions}
                        placeholder="Staff"
                        onChange={handleInput("staff-uploaders")}
                        value={filters["staff-uploaders"] }
                        isClearable                   
                    />
                    <Select 
                        options = {organSystemOptions}
                        placeholder = "Organ system"
                        onChange={handleInput("organ-systems")}
                        value={filters["organ-systems"]}
                        isClearable
                    />

                </summary>
            </details>
            <div className="unknown-filter-buttons">
                <button type="submit">Filter</button>
                <button type ="reset">Reset</button>
            </div>
        </form>
    )
}