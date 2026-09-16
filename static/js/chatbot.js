/* ============================================================
   FRAUDDETECT CHATBOT JAVASCRIPT
   ============================================================ */

console.log("🔥🔥🔥 FRAUDDETECT CHATBOT JS LOADED 🔥🔥🔥");


/* ============================================================
   OPEN CHATBOT
   ============================================================ */

function toggleChatbot() {

    console.log("🔥 toggleChatbot() called");

    const overlay =
        document.getElementById("chatbotOverlay");

    if (!overlay) {

        console.error(
            "❌ chatbotOverlay NOT FOUND"
        );

        return;
    }

    overlay.classList.toggle("active");
}


/* ============================================================
   CLOSE CHATBOT
   ============================================================ */

function closeChatbot() {

    console.log("🔥 closeChatbot() called");

    const overlay =
        document.getElementById("chatbotOverlay");

    if (!overlay) {

        console.error(
            "❌ chatbotOverlay NOT FOUND"
        );

        return;
    }

    overlay.classList.remove("active");
}


/* ============================================================
   MINIMIZE CHATBOT
   ============================================================ */

function minimizeChatbot() {

    console.log("🔥 minimizeChatbot() called");

    const overlay =
        document.getElementById("chatbotOverlay");

    if (!overlay) {
        return;
    }

    overlay.classList.remove("active");
}


/* ============================================================
   CLEAR CHAT
   ============================================================ */

function clearChat() {

    console.log("🔥 clearChat() called");

    const body =
        document.getElementById("chatbotBody");

    if (!body) {

        console.error(
            "❌ chatbotBody NOT FOUND"
        );

        return;
    }

    body.innerHTML = "";
}


/* ============================================================
   QUICK MESSAGE
   ============================================================ */

function sendQuickMessage(message) {

    console.log(
        "🔥 QUICK MESSAGE:",
        message
    );

    const input =
        document.getElementById("chatbotInput");

    if (!input) {

        console.error(
            "❌ chatbotInput NOT FOUND"
        );

        return;
    }

    input.value = message;

    sendMessage();
}


/* ============================================================
   SEND MESSAGE
   ============================================================ */

async function sendMessage() {

    console.log("");
    console.log("======================================");
    console.log("🔥 SEND MESSAGE CALLED");
    console.log("======================================");


    /* --------------------------------------------------------
       GET INPUT
       -------------------------------------------------------- */

    const input =
        document.getElementById("chatbotInput");


    /* --------------------------------------------------------
       GET SEND BUTTON
       -------------------------------------------------------- */

    const sendBtn =
        document.getElementById("sendBtn");


    /* --------------------------------------------------------
       CHECK INPUT
       -------------------------------------------------------- */

    if (!input) {

        console.error(
            "❌ chatbotInput NOT FOUND"
        );

        return;
    }


    /* --------------------------------------------------------
       CHECK BUTTON
       -------------------------------------------------------- */

    if (!sendBtn) {

        console.error(
            "❌ sendBtn NOT FOUND"
        );

        return;
    }


    /* --------------------------------------------------------
       GET MESSAGE
       -------------------------------------------------------- */

    const message =
        input.value.trim();


    console.log(
        "👤 USER MESSAGE:",
        message
    );


    /* --------------------------------------------------------
       EMPTY MESSAGE
       -------------------------------------------------------- */

    if (!message) {

        console.log(
            "⚠️ MESSAGE IS EMPTY"
        );

        return;
    }


    /* --------------------------------------------------------
       SHOW USER MESSAGE
       -------------------------------------------------------- */

    addChatMessage(
        message,
        "user"
    );


    /* --------------------------------------------------------
       CLEAR INPUT
       -------------------------------------------------------- */

    input.value = "";

    input.style.height = "auto";


    /* --------------------------------------------------------
       DISABLE SEND BUTTON
       -------------------------------------------------------- */

    sendBtn.disabled = true;


    /* ========================================================
       CSRF TOKEN
       ======================================================== */

    const csrfElement =
        document.querySelector(
            'meta[name="csrf-token"]'
        );


    if (!csrfElement) {

        console.error(
            "❌ CSRF TOKEN NOT FOUND"
        );


        addChatMessage(
            "Security token not found. Please refresh the page.",
            "bot"
        );


        sendBtn.disabled = false;

        return;
    }


    const csrfToken =
        csrfElement.getAttribute("content");


    console.log(
        "🔐 CSRF TOKEN FOUND:",
        csrfToken ? "YES" : "NO"
    );


    /* ========================================================
       SEND REQUEST TO DJANGO
       ======================================================== */

    const apiUrl =
        "/chatbot/api/chat/";


    console.log(
        "📡 API URL:",
        apiUrl
    );


    console.log(
        "📡 CALLING DJANGO..."
    );


    try {

        const response =
            await fetch(
                apiUrl,
                {
                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "X-CSRFToken":
                            csrfToken,

                        "X-Requested-With":
                            "XMLHttpRequest"

                    },

                    body: JSON.stringify({

                        message: message

                    })

                }
            );


        /* ----------------------------------------------------
           HTTP RESPONSE
           ---------------------------------------------------- */

        console.log(
            "📡 HTTP STATUS:",
            response.status
        );


        console.log(
            "📡 RESPONSE OK:",
            response.ok
        );


        /* ----------------------------------------------------
           GET RESPONSE
           ---------------------------------------------------- */

        const data =
            await response.json();


        console.log(
            "📦 DJANGO RESPONSE:",
            data
        );


        /* ====================================================
           SUCCESS
           ==================================================== */

        if (
            response.ok &&
            data.success
        ) {

            console.log(
                "✅ AI RESPONSE RECEIVED"
            );


            console.log(
                "🤖 ANSWER:",
                data.answer
            );


            addChatMessage(
                data.answer,
                "bot"
            );

        }


        /* ====================================================
           SERVER ERROR
           ==================================================== */

        else {

            console.error(
                "❌ CHATBOT API ERROR:",
                data.error
            );


            addChatMessage(

                data.error ||
                "Something went wrong while processing your request.",

                "bot"

            );

        }


    }


    /* ========================================================
       NETWORK / FETCH ERROR
       ======================================================== */

    catch (error) {

        console.error(
            "❌ FETCH ERROR:",
            error
        );


        addChatMessage(

            "Unable to connect to FraudDetect Assistant.",

            "bot"

        );

    }


    /* ========================================================
       ENABLE BUTTON
       ======================================================== */

    finally {

        sendBtn.disabled = false;


        console.log(
            "🔓 SEND BUTTON ENABLED"
        );

    }

}


/* ============================================================
   ADD CHAT MESSAGE
   ============================================================ */

function addChatMessage(message, sender) {

    console.log(
        "💬 ADD MESSAGE:",
        sender,
        message
    );


    const body =
        document.getElementById("chatbotBody");


    if (!body) {

        console.error(
            "❌ chatbotBody NOT FOUND"
        );

        return;
    }


    /* ========================================================
       CLEAN BOT RESPONSE
       ======================================================== */

    let cleanMessage =
        String(message);


    /*
       Remove Markdown bullet:

       * Fraud detected
       * High risk
       * Recent alerts

       becomes:

       Fraud detected
       High risk
       Recent alerts
    */

    if (sender === "bot") {

        cleanMessage =
            cleanMessage.replace(
                /^\s*\*\s+/gm,
                ""
            );


        /*
           Remove Markdown bold:

           **Fraud Count**

           becomes:

           Fraud Count
        */

        cleanMessage =
            cleanMessage.replace(
                /\*\*(.*?)\*\*/g,
                "$1"
            );


        /*
           Remove Markdown italic:

           *important*

           becomes:

           important
        */

        cleanMessage =
            cleanMessage.replace(
                /(?<!\*)\*([^*\n]+)\*(?!\*)/g,
                "$1"
            );


        /*
           Remove Markdown heading symbols:

           # Fraud Statistics
           ## Recent Alerts

           becomes:

           Fraud Statistics
           Recent Alerts
        */

        cleanMessage =
            cleanMessage.replace(
                /^\s*#{1,6}\s+/gm,
                ""
            );


        /*
           Remove Markdown horizontal lines
        */

        cleanMessage =
            cleanMessage.replace(
                /^\s*[-*_]{3,}\s*$/gm,
                ""
            );


        /*
           Remove extra blank lines
        */

        cleanMessage =
            cleanMessage.replace(
                /\n{3,}/g,
                "\n\n"
            );

    }


    /* ========================================================
       CREATE MESSAGE DIV
       ======================================================== */

    const messageDiv =
        document.createElement(
            "div"
        );


    messageDiv.classList.add(
        "chat-message"
    );


    /* --------------------------------------------------------
       USER / BOT CLASS
       -------------------------------------------------------- */

    if (sender === "user") {

        messageDiv.classList.add(
            "user-message"
        );

    }

    else {

        messageDiv.classList.add(
            "bot-message"
        );

    }


    /* ========================================================
       MESSAGE HTML
       ======================================================== */

    messageDiv.innerHTML = `

        <div class="message-avatar">

            <i class="fas fa-${
                sender === "user"
                    ? "user"
                    : "robot"
            }"></i>

        </div>


        <div class="message-content">

            <div class="message-bubble">

                ${escapeHtml(
                    cleanMessage
                ).replace(/\n/g, "<br>")}

            </div>


            <span class="message-time">

                Just now

            </span>

        </div>

    `;


    /* --------------------------------------------------------
       ADD TO CHAT
       -------------------------------------------------------- */

    body.appendChild(
        messageDiv
    );


    /* --------------------------------------------------------
       SCROLL TO BOTTOM
       -------------------------------------------------------- */

    body.scrollTop =
        body.scrollHeight;

}


/* ============================================================
   AUTO RESIZE TEXTAREA
   ============================================================ */

function autoResizeTextarea(
    textarea
) {

    textarea.style.height =
        "auto";


    textarea.style.height =
        textarea.scrollHeight + "px";

}


/* ============================================================
   ENTER KEY HANDLER
   ============================================================ */

function handleChatKeydown(
    event
) {

    /*
       Enter       → Send
       Shift+Enter → New line
    */

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


/* ============================================================
   ESCAPE HTML
   ============================================================ */

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}
