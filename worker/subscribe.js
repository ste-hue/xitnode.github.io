export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(),
      });
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "Method not allowed" }, 405);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return jsonResponse({ error: "Invalid JSON" }, 400);
    }

    const email = body.email?.trim().toLowerCase();
    if (!email || !isValidEmail(email)) {
      return jsonResponse({ error: "Indirizzo email non valido" }, 400);
    }

    try {
      const res = await fetch(
        `https://api.resend.com/audiences/${env.RESEND_AUDIENCE_ID}/contacts`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${env.RESEND_API_KEY}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        }
      );

      // 409 = duplicate contact, treat as success
      if (res.ok || res.status === 409) {
        return jsonResponse({ message: "Iscrizione completata!" }, 200);
      }

      const err = await res.text();
      console.error(`Resend API error: ${res.status} ${err}`);
      return jsonResponse({ error: "Errore durante l'iscrizione. Riprova." }, 500);
    } catch (err) {
      console.error("Fetch error:", err);
      return jsonResponse({ error: "Errore di rete. Riprova." }, 500);
    }
  },
};

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "https://xitnode.com",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function jsonResponse(data, status) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(),
    },
  });
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
