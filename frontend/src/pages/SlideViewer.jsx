import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import OpenSeadragon from "openseadragon";
import api from "../api";

export default function Slide() {

    const { slideId } = useParams();

    // server payload for this slide (expects { dzi_xml_url, ... })
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState(null);

    // the DIV we mount the viewer into
    const containerRef = useRef(null);
    // holds the OSD instance so we can destroy it
    const viewerRef = useRef(null);

      // 1) fetch slide metadata (gets the DZI URL)
    useEffect(() => {
        let cancelled = false;
        async function fetchSlideData() {
        setLoading(true);
        setErr(null);
        try {
            const res = await api.get(`/slides/${slideId}`);
            if (!cancelled) setData(res.data ?? null);
        } catch (e) {
            console.error("Error fetching slide data:", e);
            if (!cancelled) setErr(e);
        } finally {
            if (!cancelled) setLoading(false);
        }
        }
        fetchSlideData();
        return () => { cancelled = true; };
    }, [slideId]);

    // 2) create/destroy the OSD viewer when data is ready/changes
    useEffect(() => {
        // need both: a mounted container and a valid tilesource URL
        if (!containerRef.current || !data?.dzi_xml_url) return;

        // clean up any previous viewer (defensive)
        if (viewerRef.current) {
            viewerRef.current.destroy();
            viewerRef.current = null;
        }

        // create viewer
        viewerRef.current = OpenSeadragon({
            // IMPORTANT: pass the DOM node via `element`, not `id` string
            element: containerRef.current,
            prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
            tileSources: data.dzi_xml_url, // DZI (Deep Zoom) URL from your API

            // guardrails / UX
            showNavigator: true,
            constrainDuringPan: true,
            visibilityRatio: 1,
            minZoomImageRatio: 1,
            maxZoomPixelRatio: 8,
        });
                // optional: tweak mouse behavior
        viewerRef.current.gestureSettingsMouse.clickToZoom = false;
        viewerRef.current.gestureSettingsMouse.flickEnabled = false;

        // cleanup on data change or unmount
        return () => {
        viewerRef.current?.destroy();
        viewerRef.current = null;
        };
    }, [data]);
    
    console.log("HEre is requested data ", data);
    //   // 3) simple UI states (optional but helpful)
    if (loading) return <div style={{ padding: 12 }}>Loading slide…</div>;
    if (err) return <div style={{ padding: 12, color: "crimson" }}>Failed to load slide.</div>;
    if (!data?.dzi_xml_url) return <div style={{ padding: 12 }}>No DZI URL found for this slide.</div>;

    // 4) the mount point for OSD (must have width/height)
    return (
        <div
        ref={containerRef}
        style={{ width: "100%", height: "100vh", background: "#111" }}
        />
    );
}



