import api from "../api";
import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import "../styles/ModuleDetails.css";

export default function ModuleDetails() {
  const { moduleId } = useParams();
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.get(`/modules/${moduleId}`);
        setQuestions(response.data.questions || []);
      } catch (e) {
        setError(e);
        console.error("Cannot fetch module data ", e);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [moduleId]);

  if (loading) {
    return <p>Loading module…</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>Error loading module</p>;
  }

  return (
    <div className="module-details-container">
      {questions.map((q) => {
        const slides = q.files || [];

        return (
          <div className="module-details-question" key={q.id}>
            {/* Slides first */}
            <div className="module-slide-grid">
              {slides.map((f) => {
                const slideId = f.id;
                return (
                  <div className="module-slide-card" key={f.id}>
                    <Link to={`/slides/${slideId}`}>
                      <img
                        src={f.thumbnail_url}
                        loading="lazy"
                        alt={f.filename || "slide thumbnail"}
                      />
                    </Link>
                  </div>
                );
              })}
            </div>

            {/* Text underneath, centered */}
            <div className="module-details-row clinical">
              {q.clinical_information}
            </div>
            <div className="module-details-row question">
              {q.question}
            </div>
          </div>
        );
      })}
    </div>
  );
}