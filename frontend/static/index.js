let lastSuggestions = [];

        function fetchSuggestions(text) {
            $.ajax({
                url: "/api/suggest",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({input_text: text}),
                success: function(response) {
                    let suggDiv = $("#suggestions");
                    suggDiv.empty();
                    lastSuggestions = response.suggestions;

                    if(lastSuggestions.length > 0) {
                        lastSuggestions.forEach(function(word) {
                            let span = $("<span class='suggestion'>" + word + "</span>");
                            
                            span.click(function() {
                                let currentText = $("#inputBox").val().trim();
                                $("#inputBox").val(currentText + " " + word + " ");
                                $("#inputBox").trigger("input");
                            });

                            suggDiv.append(span);
                        });
                    }
                }
            });
        }

        $(document).ready(function() {
            $("#inputBox").on("input", function() {
                let text = $(this).val();
                fetchSuggestions(text);
            });

            $("#inputBox").keydown(function(e) {
                if ((e.key === "Tab" || e.key === "Enter") && lastSuggestions.length > 0) {
                    e.preventDefault();
                    let firstWord = lastSuggestions[0];
                    let currentText = $("#inputBox").val().trim();
                    $("#inputBox").val(currentText + " " + firstWord + " ");
                    $("#inputBox").trigger("input");
                }
            });
        });