import { useState , useEffect} from "react"
import api from "../api"

export default function Home() {

    const [ data, setData ] = useState([]);
    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState(null);
    
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                const response = await api.get(`/modules/`)
                console.log(response.data);
            } catch (err) {
                setError(err);
                console.log("Error loading data ", err)
            } finally {
                setLoading(false)
            }
        }
        fetchData();
    }, []);

    return (
        <div className="home-container">
            <p>You have reached the home page</p>
        </div>
    )
}