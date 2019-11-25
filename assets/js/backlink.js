window.onload = function () {
    var quotes = document.getElementsByClassName("quotelink");

    for (var i = 0; i < quotes.length; ++i) {
        var quote = quotes[i]
        var quoteID = quote.parentElement.id.substring(1);

        var quotedID = quote.getAttribute("href").substring(2);
        
        var blDiv = document.getElementById("bl_"+quotedID);
        if (blDiv == null) {
            blDiv = document.createElement("div");
            blDiv.setAttribute("id", "bl_"+quotedID);
            blDiv.classList.add("backlink");
        }
        var quotedPost = document.getElementById("pi"+quotedID);
        quotedPost.appendChild(blDiv);

        var newSpan = document.createElement('span');
        var newA = document.createElement('a');
        newA.appendChild(document.createTextNode(">>"+quoteID));
        newA.href = "#p"+quoteID;

        newSpan.appendChild(newA);
        blDiv.appendChild(newSpan);
    }

};