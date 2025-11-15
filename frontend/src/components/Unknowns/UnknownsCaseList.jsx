import { Link } from "react-router-dom";

export default function UnknownCasesList( { modules } ) {
    
    const filteredModules = modules.filter(m=> m.model_type === "U");

    return (
        <div className="unknown-cases-list">
            <div className="unknown-case-grid">
                {filteredModules.map((module) => {
                   const thumbnailUrl = module.questions?.[0]?.files?.[0]?.thumbnail_url ?? null
                   const numQuestions = module.questions?.length
                   const organSystem = module.organ_system['name']

                   return (
                    <div key={module.id} className = "module-entry">
                        <Link 
                            to = {`/modules/${module.id}/`}
                            className="module-link"
                            aria-label={`Open module ${module.id}`}
                        >
                        { thumbnailUrl? (
                            <img 
                                src = {thumbnailUrl}
                                alt={`Thumbnail url for ${module.id}`}
                                loading="lazy"
                            />
                        ) :
                        (
                             <div className="placeholder-image">No Img</div>
                        )}    
                        </Link>
                        <div className="module-entry-row"> Organ system: {organSystem} </div>
                        <div className="module-entry-row"> Number of questions: {numQuestions}</div>
                    </div>
                   )
                })
                }
            </div>
        </div>
    )
}