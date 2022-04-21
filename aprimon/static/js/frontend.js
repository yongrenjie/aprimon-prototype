const ALL_BALLS = ["beast", "dream", "fast", "friend", "heavy", "level", "love", "lure", "moon", "safari", "sport"]
const SELECT_AN_ENTRY = "-- select --"
const MANUALLY_LIST_APRIMON = "(manually list Aprimon...)"


function populateUserDropdowns() {
    // Populate dropdown menus with registered users {{{1
    let user1a_prev_selected = $("select#user1a-select").val();
    let user2a_prev_selected = $("select#user2a-select").val();
    $.ajax({
        type: "GET",
        url: "/_all_users",
        data: {
            "game": getGame(),
        },
        dataType: "json",
        contentType: "application/json",
        success: function (response) {
            // Store as global variable
            window.allUsers = response["allUsers"];

            let listOfUsernames = Object.keys(allUsers);
            listOfUsernames.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
            listOfUsernames.unshift(SELECT_AN_ENTRY);
            listOfUsernames.push(MANUALLY_LIST_APRIMON);
            $("#user1a-select").html("");
            $("#user2a-select").html("");
            for (let user of listOfUsernames) {
                $("#user1a-select").append("<option>" + user + "</option>");
                $("#user2a-select").append("<option>" + user + "</option>");
            }
            // Preserve username choices when switching games (if available)
            if (listOfUsernames.includes(user1a_prev_selected)) {
                $("#user1a-select").val(user1a_prev_selected).trigger('change');
            }
            if (listOfUsernames.includes(user2a_prev_selected)) {
                $("#user2a-select").val(user2a_prev_selected).trigger('change');
            }
        }
    });
    // }}}1
}
// On page load
populateUserDropdowns();
// When changing the game at the top
$("#game>input").on("click", populateUserDropdowns);


function showOrHideExtras() {
    // Show or hide UI elements (e.g. textareas for manual Aprimon entry) based on user-selected values {{{1
    if (typeof window.allUsers === "undefined") return;

    // Get values of user1 and user2 dropdowns
    const user1 = $("select#user1a-select").val();
    const user2 = $("select#user2a-select").val();

    // Helper function to display link to spreadsheet underneath the dropdown
    function showSpreadsheetLink(divSelector, key) {
        $(divSelector).show();
        $(divSelector).html(`<a target="_blank" href="https://docs.google.com/spreadsheets/d/${key}/edit">(view on Google Sheets)</a>`);
    }

    // If user1 is a real spreadsheet
    if (user1 in window.allUsers) {
        // Hide the manual entry textarea
        $("div#user1a-text").hide();
        // Show the spreadsheet
        showSpreadsheetLink("div#user1a-sheet-link", window.allUsers[user1]);
        // Prompt for extras
        $("div#user1b-text").show();
        $("div#user1b").show();
        // Show the extras textarea if the input is checked
        $("div#user1b-textarea").toggle(!!$("input#user1-extra").is(":checked"));
    }
    else if (user1 == MANUALLY_LIST_APRIMON) {
        // Show the manual entry textarea
        $("div#user1a-text").show();
        // Hide everything else
        $("div#user1a-sheet-link").hide();
        $("div#user1b-text").hide();
        $("div#user1b").hide();
    }
    else {
        // Nothing selected, just hide everything
        $("div#user1a-text").hide();
        $("div#user1a-sheet-link").hide();
        $("div#user1b-text").hide();
        $("div#user1b").hide();
    }

    // Same for user2
    if (user2 in window.allUsers) {
        // Hide the manual entry textarea
        $("div#user2a-text").hide();
        // Show the spreadsheet
        showSpreadsheetLink("div#user2a-sheet-link", window.allUsers[user2]);
        // Prompt for extras
        $("div#user2b-text").show();
        $("div#user2b").show();
        // Show the extras textarea if the input is checked
        $("div#user2b-textarea").toggle(!!$("input#user2-extra").is(":checked"));
    }
    else if (user2 == MANUALLY_LIST_APRIMON) {
        // Show the manual entry textarea
        $("div#user2a-text").show();
        // Hide everything else
        $("div#user2a-sheet-link").empty();
        $("div#user2b-text").hide();
        $("div#user2b").hide();
    }
    else {
        // Nothing selected, just hide everything
        $("div#user2a-text").hide();
        $("div#user2a-sheet-link").empty();
        $("div#user2b-text").hide();
        $("div#user2b").hide();
    }
    // }}}1
}
// On page load
showOrHideExtras();
// When changing the dropdown menus
$("select#user1a-select").on("change", showOrHideExtras);
$("select#user2a-select").on("change", showOrHideExtras);
// When clicking the 'extras' checkboxes
$("input#user1-extra").on("click", showOrHideExtras);
$("input#user2-extra").on("click", showOrHideExtras);


function calculateAprimon() {
    // Send the AJAX query to calculate the Aprimon difference {{{1

    // Determine user 1 type
    let user1 = $("select#user1a-select").val();
    let user1_data;
    if (user1 == SELECT_AN_ENTRY) return;
    else if (user1 == MANUALLY_LIST_APRIMON) {
        user1_data = {"list": $("textarea#user1a-textarea").val().split(/\r?\n/)};
    }
    else {
        user1_data = {"username": user1};
    }
    // Check for user 1 extras
    if ($("input#user1-extra").is(":checked")) {
        user1_data["extra_list"] = $("textarea#user1b-textarea").val().split(/\r?\n/);
    }

    // Determine user 2 type
    let user2 = $("select#user2a-select").val();
    let user2_data;
    if (user2 == SELECT_AN_ENTRY) return;
    else if (user2 == MANUALLY_LIST_APRIMON) {
        user2_data = {"list": $("textarea#user2a-textarea").val().split(/\r?\n/)};
    }
    else {
        user2_data = {"username": user2};
    }
    // Check for user 2 extras
    if ($("input#user2-extra").is(":checked")) {
        user2_data["extra_list"] = $("textarea#user2b-textarea").val().split(/\r?\n/);
    }

    // Construct HTTP request
    let request = {
        "game": getGame(),
        "user1": user1_data,
        "user2": user2_data,
    };

    // Send the request...
    $.ajax({
        type: "POST",
        url: "/_calculate_aprimon",
        data: JSON.stringify(request),
        dataType: "json",
        contentType: "application/json",
        beforeSend: function () {
            $("div#submit").hide();
            $("div#loading").show();
        },
        complete: function () {
            $("div#submit").show();
            $("div#loading").hide();
        },
        success: function (response) {
            // store the aprimon list as a global variable to avoid unnecessary
            // recalculation when changing filters
            window.collection = response['aprimon'];
            // clear any prior selections and the textarea
            window.selectedAprimon = [];
            updateSelectionText();
            // show the table
            displayCollection();
            // scroll down to the table
            $('html, body').animate({
                scrollTop: $("div#results-aprimon").offset().top
            }, 700);
        },
    });
    // }}}1
}
// When clicking the submit button
$("input#submit-button").on("click", calculateAprimon);


function displayCollection() {
    // Generate the table showing the Aprimon difference {{{1

    // Structure of each entry, as passed from the backend:
    // entry = {
    //     "canonical_name": str,
    //     "display_name": str,
    //     "national_dex": int,
    //     "swsh": {"beast": True, "dream", True, ...},
    //     "bdsp": {"beast": True, "dream", True, ...},
    //     "balls": ["beast", "dream", ...]
    // }

    // Initialise collection to display. Note that this is different from
    // window.collection which is unfiltered
    // Apparently in JavaScript this is the way to deepcopy an object...
    let collection_to_show = JSON.parse(JSON.stringify(window.collection));

    // Filter generations
    if (!($("input#gen1").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 1 && entry.national_dex <= 151));
    }
    if (!($("input#gen2").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 152 && entry.national_dex <= 251));
    }
    if (!($("input#gen3").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 252 && entry.national_dex <= 386));
    }
    if (!($("input#gen4").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 387 && entry.national_dex <= 493));
    }
    if (!($("input#gen5").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 494 && entry.national_dex <= 649));
    }
    if (!($("input#gen6").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 650 && entry.national_dex <= 721));
    }
    if (!($("input#gen7").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 722 && entry.national_dex <= 809));
    }
    if (!($("input#gen8").is(":checked"))) {
        collection_to_show = collection_to_show.filter(entry => !(entry.national_dex >= 810 && entry.national_dex <= 905));
    }

    // Filter balls
    for (let ball of ALL_BALLS) {
        if (!$("input#ball-" + ball).is(":checked")) {
            for (let entry of collection_to_show) {
                entry.balls = entry.balls.filter(b => b != ball);
            }
        }
    }

    // Filter legality
    let game = getGame();
    for (let entry of collection_to_show) {
        // entry[game][ball] is a Boolean which tells us if it's legal in the game
        entry.balls = entry.balls.filter(ball => entry[game][ball]);
    }

    // Remove empty entries and sort
    collection_to_show = collection_to_show.filter(entry => entry.balls.length != 0);
    sortCollection(collection_to_show);

    // Construct text
    let h = '<table class="collection"><tr class="collection-row"><th>ND</th><th>Pokémon</th><th>Sprite</th>';
    for (let ball of ALL_BALLS) {
        if ($("input#ball-" + ball).is(":checked")) {
            h = h + `<th>${capitaliseFirst(ball)}</th>`;
        }
    }
    h = h + "</tr>\n";
    for (let entry of collection_to_show) {
        let row = '<tr class="collection-row">';
        row = row + `<td class="collection-entry"><b>${entry.national_dex}</b></td>`;
        row = row + `<td class="collection-entry"><b>${entry.display_name}</b></td>`;
        row = row + `<td class="collection-entry">${makeSpriteImgTagSmall(entry.canonical_name)}</td>`;
        for (let ball of ALL_BALLS) {
            const canonical_id = `${ball}-${entry.canonical_name}`; // dream-togepi
            if ($("input#ball-" + ball).is(":checked")) {
                if (entry.balls.includes(ball)) {
                    const index = getIndexOfSelectedAprimon(entry.canonical_name);
                    if (index !== -1 && window.selectedAprimon[index].balls.includes(ball)) {
                        row = row + `<td class="collection-entry active-entry selected" id="${canonical_id}">${makeSpriteImgTag(ball)}</td>`;
                    }
                    else {
                        row = row + `<td class="collection-entry active-entry unselected" id="${canonical_id}">${makeSpriteImgTag(ball)}</td>`;
                    }
                }
                else {
                    row = row + `<td class="collection-entry inactive-entry"></td>`;
                }
            }
        }
        row = row + "</tr>\n";
        h = h + row;
    }
    h = h + "</table>";
    $("div#results-aprimon").html(h);
    $("div#results-aprimon-container").show();
    
    $("div#results-selector").show();
    makeTableDynamic();
    // }}}1
}
// When changing any of the generation filters
$("div#filter-generations input").each(function () {
    $(this).on("click", displayCollection);
});
// When changing any of the ball filters
$("div#filter-balls input").each(function () {
    $(this).on("click", displayCollection);
});
// When changing any of the sort types
$("input#sort-radio-dex").on("click", displayCollection);
$("input#sort-radio-alpha").on("click", displayCollection);


function makeTableDynamic() {
    // Create dynamic behaviour for table cells {{{1

    $(".active-entry").each(function (index, element) {
        $(this).on("click", function () {
            updateSelection($(this).attr("id"));
        });
    });
    // }}}1
}

function updateSelection(canonical_id) {
    // Add or remove an Aprimon from the selection {{{1

    // Parse the ID to get ball and Pokemon name
    let ball;
    let canonical_name;
    let splits = canonical_id.split("-");
    if (splits.length == 2) {
        ball = splits[0];
        canonical_name = splits[1];
    }
    else {
        ball = splits[0];
        canonical_name = splits.slice(1).join("-");
    }

    // Check if selection already contains an entry for the Pokemon
    let entry_index = getIndexOfSelectedAprimon(canonical_name);

    if (entry_index === -1) {
        // Case 1: Not found. Add a new entry

        // Find the correct entry from global collection
        let entry_to_be_added;
        for (let entry of window.collection) {
            if (entry.canonical_name === canonical_name) {
                // Deepcopy it and modify the ball list
                entry_to_be_added = JSON.parse(JSON.stringify(entry));
                entry_to_be_added.balls = [ball];
                break;
            }
        }
        // Add it to the selection
        window.selectedAprimon.push(entry_to_be_added);
        $("td#" + canonical_id).addClass("selected");
        $("td#" + canonical_id).removeClass("unselected");
    }

    else {
        // Case 2: An entry was found. Check whether the ball is inside
        let existing_entry = window.selectedAprimon[entry_index];
        let ball_index = existing_entry.balls.indexOf(ball);
        
        if (ball_index == -1) {
            // Case 2a. An entry was found but the ball wasn't there. Add it
            existing_entry.balls.push(ball);
            existing_entry.balls.sort();
            $("td#" + canonical_id).addClass("selected");
            $("td#" + canonical_id).removeClass("unselected");
        }
        else {
            // Case 2b. An entry was found and the ball was inside. Remove it
            existing_entry.balls.splice(ball_index, 1);
            $("td#" + canonical_id).addClass("unselected");
            $("td#" + canonical_id).removeClass("selected");
            // Check if it was the last ball remaining...
            if (existing_entry.balls.length == 0) {
                window.selectedAprimon.splice(entry_index, 1);
            }
        }
    }

    // Update the textarea
    updateSelectionText();
    // }}}1
}


function updateSelectionText() {
    // Update textarea {{{1
    let s = "";
    let number = 0;
    sortCollection(window.selectedAprimon);
    for (let entry of window.selectedAprimon) {
        for (let ball of entry.balls) {
            number = number + 1;
            s = s + `${number}. ${capitaliseFirst(ball)} ${entry.display_name}\n`;
        }
    }
    $("textarea#results-selector-textarea").val(s);
    // }}}1
}
// When changing any of the sort types
$("input#sort-radio-dex").on("click", updateSelectionText);
$("input#sort-radio-alpha").on("click", updateSelectionText);


function changeGameSprites() {
    // Change the sprites around the game selector {{{1

    // Determine which game was selected
    let game = getGame();

    if (game == "swsh") {
        $("#left-sprite").html(makeSpriteImgTag("zacian"));
        $("#right-sprite").html(makeSpriteImgTag("zamazenta"));
    }
    else if (game == "bdsp") {
        $("#left-sprite").html(makeSpriteImgTag("dialga"));
        $("#right-sprite").html(makeSpriteImgTag("palkia"));
    }
    // }}}1
}
// On page load
changeGameSprites();
// When game is changed
$("#game>input").on("click", changeGameSprites);


function swapUsers() {
    // Swap the two users round {{{1

    // Swap spreadsheet dropdown
    let p = $("select#user1a-select").val();
    let q = $("select#user2a-select").val();
    $("#user1a-select").val(q).trigger('change');
    $("#user2a-select").val(p).trigger('change');
    // Swap manual lists
    p = $("textarea#user1a-textarea").val();
    q = $("textarea#user2a-textarea").val();
    $("textarea#user1a-textarea").val(q);
    $("textarea#user2a-textarea").val(p);
    // Swap extras checkbox
    p = $("input#user1-extra").is(":checked");
    q = $("input#user2-extra").is(":checked");
    $("input#user1-extra").prop("checked", q);
    $("input#user2-extra").prop("checked", p);
    // Swap extra lists
    p = $("textarea#user1b-textarea").val();
    q = $("textarea#user2b-textarea").val();
    $("textarea#user1b-textarea").val(q);
    $("textarea#user2b-textarea").val(p);
    // Update UI
    showOrHideExtras();
    // }}}1
}
// Whenever the swap button is clicked
$("input#swap-button").on("click", swapUsers);


function selectAllAprimon() {
    // Select all Aprimon from the list {{{1
    $("td.unselected").each(function(index) {
        updateSelection($(this).attr("id"));
    });
    // }}}1
}
// Whenever the select all button is clicked
$("input#select-all-button").on("click", selectAllAprimon);



//////////////////////
// Helper functions //
//////////////////////


function makeSpriteImgTag(name) {
    return `<img src="static/sprites/${name}.png" />`;
}


function makeSpriteImgTagSmall(name) {
    return `<img src="static/sprites/${name}.png" class="constrained-height" />`;
}


function getGame() {
    return $("input[name='game-radio']:checked").val();
}


function getSortMode() {
    return $("input[name='sort-radio']:checked").val();
}


function capitaliseFirst(str) {
    return str.slice(0, 1).toUpperCase() + str.slice(1);
}


function getIndexOfSelectedAprimon(canonical_name) {
    if (typeof window.selectedAprimon === "undefined") return -1;
    return window.selectedAprimon.findIndex((e) => e.canonical_name === canonical_name);
}


function sortCollection(collection) {
    // Sorts in-place!
    
    let sortMode = getSortMode();
    if (sortMode == "dex") {
        collection.sort((a1, a2) => a1.national_dex - a2.national_dex);
    }
    else if (sortMode == "alpha") {
        collection.sort((a1, a2) => a1.display_name.localeCompare(a2.display_name));
    }

    // sort the balls within each entry too
    for (let entry of collection) {
        entry.balls.sort();
    }
}


// vim: foldmethod=marker
