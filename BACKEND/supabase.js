"use strict";

/*
==============================================================
  SURVIVAL VIETNAMESE WITH DUONG
  Supabase Client
==============================================================

  This file creates the Supabase client used by:

  - Login / Register
  - User sessions
  - Game progress
  - Game results

  IMPORTANT:
  The publishable key is safe to use in frontend code.
  NEVER put the Supabase service_role / secret key here.
==============================================================
*/


/* ==========================================================
   SUPABASE CONFIGURATION
========================================================== */

const SUPABASE_URL =
    "https://wzdpngqssqezoljfvdpl.supabase.co";


const SUPABASE_PUBLISHABLE_KEY =
    "sb_publishable__lI7cv0BAn9lNB7Q5FVRwQ_y8ugOr3V";


/* ==========================================================
   SAFETY CHECK
========================================================== */

if (
    !SUPABASE_URL ||
    SUPABASE_URL.includes("PASTE_")
) {

    console.error(
        "Supabase URL is not configured."
    );

}


if (
    !SUPABASE_PUBLISHABLE_KEY ||
    SUPABASE_PUBLISHABLE_KEY.includes("PASTE_")
) {

    console.error(
        "Supabase publishable key is not configured."
    );

}


/* ==========================================================
   CREATE SUPABASE CLIENT
========================================================== */

if (
    typeof window.supabase === "undefined"
) {

    console.error(
        "Supabase JavaScript library was not loaded."
    );

}
else {

    window.supabaseClient =
        window.supabase.createClient(
            SUPABASE_URL,
            SUPABASE_PUBLISHABLE_KEY
        );

}


/* ==========================================================
   HELPER: GET CURRENT USER
========================================================== */

async function getCurrentUser() {

    if (
        !window.supabaseClient
    ) {

        return null;

    }


    const {
        data,
        error
    } =
        await window.supabaseClient
            .auth
            .getUser();


    if (error) {

        console.error(
            "Could not get current user:",
            error
        );

        return null;

    }


    return data.user || null;

}


/* ==========================================================
   HELPER: GET CURRENT SESSION
========================================================== */

async function getCurrentSession() {

    if (
        !window.supabaseClient
    ) {

        return null;

    }


    const {
        data,
        error
    } =
        await window.supabaseClient
            .auth
            .getSession();


    if (error) {

        console.error(
            "Could not get current session:",
            error
        );

        return null;

    }


    return data.session || null;

}


/* ==========================================================
   HELPER: LOGOUT
========================================================== */

async function logoutUser() {

    if (
        !window.supabaseClient
    ) {

        return {
            success: false,
            error: "Supabase client is not available."
        };

    }


    const {
        error
    } =
        await window.supabaseClient
            .auth
            .signOut();


    if (error) {

        console.error(
            "Logout error:",
            error
        );

        return {
            success: false,
            error: error.message
        };

    }


    return {
        success: true
    };

}


/* ==========================================================
   AUTH STATE LISTENER
==========================================================

   Other pages can use this to react when the user:

   - logs in
   - logs out
   - refreshes the page
   - changes authentication state
========================================================== */

function onAuthStateChange(
    callback
) {

    if (
        !window.supabaseClient
    ) {

        console.error(
            "Supabase client is not available."
        );

        return null;

    }


    const {
        data
    } =
        window.supabaseClient
            .auth
            .onAuthStateChange(
                (
                    event,
                    session
                ) => {

                    if (
                        typeof callback ===
                        "function"
                    ) {

                        callback(
                            event,
                            session
                        );

                    }

                }
            );


    return data.subscription;

}