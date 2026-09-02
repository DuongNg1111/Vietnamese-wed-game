console.log("ANALYTICS.JS LOADED");

"use strict";

/*
==============================================================
  SURVIVAL VIETNAMESE
  Anonymous Analytics
==============================================================
*/


/* ==========================================================
   STORAGE KEYS
========================================================== */

const ANALYTICS_VISITOR_KEY =
    "sv_visitor_id";


const ANALYTICS_SESSION_KEY =
    "sv_session_id";


/* ==========================================================
   CREATE RANDOM ID
========================================================== */

function createAnalyticsId() {

    if (
        window.crypto &&
        typeof window.crypto.randomUUID ===
            "function"
    ) {

        return window.crypto.randomUUID();

    }


    return (
        Date.now().toString(36) +
        Math.random()
            .toString(36)
            .substring(2, 12)
    );

}


/* ==========================================================
   GET / CREATE VISITOR ID
========================================================== */

function getVisitorId() {

    let visitorId =
        localStorage.getItem(
            ANALYTICS_VISITOR_KEY
        );


    if (!visitorId) {

        visitorId =
            createAnalyticsId();


        localStorage.setItem(
            ANALYTICS_VISITOR_KEY,
            visitorId
        );

    }


    return visitorId;

}


/* ==========================================================
   GET / CREATE SESSION ID
========================================================== */

function getSessionId() {

    let sessionId =
        sessionStorage.getItem(
            ANALYTICS_SESSION_KEY
        );


    if (!sessionId) {

        sessionId =
            createAnalyticsId();


        sessionStorage.setItem(
            ANALYTICS_SESSION_KEY,
            sessionId
        );

    }


    return sessionId;

}


/* ==========================================================
   INITIALIZE IDS
========================================================== */

const analyticsVisitorId =
    getVisitorId();


const analyticsSessionId =
    getSessionId();


/* ==========================================================
   SEND ANALYTICS EVENT
========================================================== */

async function trackEvent(
    eventName,
    options = {}
) {

    if (
        !window.supabaseClient
    ) {

        console.warn(
            "Analytics: Supabase client is not available."
        );

        return;

    }


    const eventData = {

        visitor_id:
            analyticsVisitorId,

        session_id:
            analyticsSessionId,

        event_name:
            eventName,

        page:
            options.page ?? null,

        game:
            options.game ?? null,

        metadata:
            options.metadata ?? null

    };


    const {
        error
    } =
        await window.supabaseClient
            .from("analytics_events")
            .insert(eventData);


    if (error) {

        console.error(
            "Analytics event error:",
            error
        );

        return;

    }


    console.log(
        "Analytics event:",
        eventName
    );

}


/* ==========================================================
   SESSION START
========================================================== */

trackEvent(
    "session_start",
    {
        page:
            window.location.pathname
    }
);

trackEvent(
    "page_view",
    {
        page:
            window.location.pathname +
            window.location.search
    }
);

console.log(
    "Analytics visitor:",
    analyticsVisitorId
);

console.log(
    "Analytics session:",
    analyticsSessionId
);

window.trackGameStart = function (
    gameName
) {

    return trackEvent(
        "game_start",
        {
            page:
                window.location.pathname +
                window.location.search,

            game:
                gameName
        }
    );

};

console.log(
    "TRACK GAME START LOADED:",
    typeof window.trackGameStart
);

function trackGameComplete(gameName, score, total) {
    const safeScore = Number(score) || 0;
    const safeTotal = Number(total) || 0;

    const accuracy =
        safeTotal > 0
            ? Math.round((safeScore / safeTotal) * 100)
            : 0;

    return trackEvent(
        "game_complete",
        {
            page:
                window.location.pathname +
                window.location.search,
            game: gameName,
            metadata: {
                score: safeScore,
                total: safeTotal,
                accuracy: accuracy
            }
        }
    );
}