const ALL_BALLS = ["beast", "dream", "fast", "friend", "heavy", "level", "love", "lure", "moon", "safari", "sport"]
const SELECT_AN_ENTRY = "-- select --"
const MANUALLY_LIST_APRIMON = "(manually list Aprimon...)"

function populateUserDropdowns() {
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
}
populateUserDropdowns();
$("#game>input").on("click", populateUserDropdowns);


function showOrHideExtras() {
    if (window.allUsers === undefined) return;

    // get values of user1 and user2
    const user1 = $("select#user1a-select").val();
    const user2 = $("select#user2a-select").val();

    // display link to spreadsheet underneath the dropdown
    function showSpreadsheetLink(divSelector, key) {
        $(divSelector).show();
        $(divSelector).html(`<a target="_blank" href="https://docs.google.com/spreadsheets/d/${key}/edit">(view on Google Sheets)</a>`);
    }

    // if user1 is a real spreadsheet
    if (user1 in window.allUsers) {
        // Hide the manual-entry textarea
        $("div#user1a-text").hide();
        // Show the spreadsheet
        showSpreadsheetLink("div#user1a-sheet-link", window.allUsers[user1]);
        // Prompt for extras
        $("div#user1b-text").show();
        $("div#user1b").show();
        if ($("input#user1-extra").is(":checked")) {
            $("div#user1b-textarea").show();
        }
        else {
            $("div#user1b-textarea").hide();
        }
    }
    else {
        if (user1 == MANUALLY_LIST_APRIMON) {
            $("div#user1a-text").show();
        }
        else {
            $("div#user1a-text").hide();
        }
        $("div#user1a-sheet-link").hide();
        $("div#user1b-text").hide();
        $("div#user1b").hide();
    }
    if (user2 in window.allUsers) {
        $("div#user2a-text").hide();
        showSpreadsheetLink("div#user2a-sheet-link", window.allUsers[user2]);
        $("div#user2b-text").show();
        $("div#user2b").show();
        if ($("input#user2-extra").is(":checked")) {
            $("div#user2b-textarea").show();
        }
        else {
            $("div#user2b-textarea").hide();
        }
    }
    else {
        if (user2 == MANUALLY_LIST_APRIMON) {
            $("div#user2a-text").show();
        }
        else {
            $("div#user2a-text").hide();
        }
        $("div#user2a-sheet-link").empty();
        $("div#user2b-text").hide();
        $("div#user2b").hide();
    }
}
showOrHideExtras();  // on page load
$("input#user1-extra").on("click", showOrHideExtras);
$("select#user1a-select").on("change", showOrHideExtras);
$("input#user2-extra").on("click", showOrHideExtras);
$("select#user2a-select").on("change", showOrHideExtras);


function calculateAprimon() {
    // Determine user 1 type
    let user1 = $("select#user1a-select").val();
    let user1_data;
    if (user1 == SELECT_AN_ENTRY) return;
    else if (user1 == MANUALLY_LIST_APRIMON) {
        user1_data = {
            "list": $("textarea#user1a-textarea").val().split(/\r?\n/),
        }
    }
    else {
        user1_data = {
            "username": user1,
        };
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
        user2_data = {
            "list": $("textarea#user2a-textarea").val().split(/\r?\n/),
        }
        console.log(user2_data)
    }
    else {
        user2_data = {
            "username": user2,
        };
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
            displayCollection();
            // scroll down to the table
            $('html, body').animate({
                scrollTop: $("div#results-aprimon").offset().top
            }, 700);
        },
    });
}
$("input#submit-button").on("click", calculateAprimon);


function displayCollection() {
    // Very rudimentary for now -- should actually display a full table!
    // Structure of each entry, as passed from the backend:
    // entry = {
    //     "canonical_name": str,
    //     "display_name": str,
    //     "national_dex": int,
    //     "swsh": {"beast": True, "dream", True, ...},
    //     "bdsp": {"beast": True, "dream", True, ...},
    //     "balls": ["beast", "dream", ...]
    // }

    // Determine sort type
    let sort_type = $("input[name='sort-radio']:checked").val();

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

    // Remove empty entries
    collection_to_show = collection_to_show.filter(entry => entry.balls.length != 0)

    // Sort
    if (sort_type == "dex") {
        collection_to_show = collection_to_show.sort((e1, e2) => e1.national_dex - e2.national_dex);
    }
    else if (sort_type == "alpha") {
        collection_to_show = collection_to_show.sort((e1, e2) => e1.display_name.localeCompare(e2.display_name));
    }

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
            if ($("input#ball-" + ball).is(":checked")) {
                if (entry.balls.includes(ball)) {
                    row = row + `<td class="collection-entry" id="${ball}-${entry.canonical_name}">${makeSpriteImgTag(ball)}</td>`;
                }
                else {
                    row = row + `<td class="collection-entry"></td>`;
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
}
$("div#filter-generations input").each(function () {
    $(this).on("click", displayCollection);
});
$("div#filter-balls input").each(function () {
    $(this).on("click", displayCollection);
});
$("input#sort-radio-dex").on("click", displayCollection);
$("input#sort-radio-alpha").on("click", displayCollection);


function changeGame() {
    // Determine game
    let game = getGame();

    if (game == "swsh") {
        $("#left-sprite").html(makeSpriteImgTag("zacian"));
        $("#right-sprite").html(makeSpriteImgTag("zamazenta"));
        $("div#user1").css("background-color", "#daebf5");
        $("div#user2").css("background-color", "#f2d9d5");
    }
    else if (game == "bdsp") {
        $("#left-sprite").html(makeSpriteImgTag("dialga"));
        $("#right-sprite").html(makeSpriteImgTag("palkia"));
    }
}
changeGame();
$("#game>input").on("click", changeGame);


function swapUsers() {
    // spreadsheet
    let p = $("select#user1a-select").val();
    let q = $("select#user2a-select").val();
    $("#user1a-select").val(q).trigger('change');
    $("#user2a-select").val(p).trigger('change');
    // manual list
    p = $("textarea#user1a-textarea").val();
    q = $("textarea#user2a-textarea").val();
    $("textarea#user1a-textarea").val(q);
    $("textarea#user2a-textarea").val(p);
    // extras checkbox
    p = $("input#user1-extra").is(":checked");
    q = $("input#user2-extra").is(":checked");
    $("input#user1-extra").prop("checked", q);
    $("input#user2-extra").prop("checked", p);
    // extras list
    p = $("textarea#user1b-textarea").val();
    q = $("textarea#user2b-textarea").val();
    $("textarea#user1b-textarea").val(q);
    $("textarea#user2b-textarea").val(p);
    // update whether textareas are displayed
    showOrHideExtras();
}
$("input#swap-button").on("click", swapUsers);


function makeSpriteImgTag(name) {
    return `<img src="static/sprites/${name}.png" />`;
}

function makeSpriteImgTagSmall(name) {
    return `<img src="static/sprites/${name}.png" class="constrained-height" />`;
}


function getGame() {
    return $("input[name='game-radio']:checked").val();
}

function capitaliseFirst(str) {
    return str.slice(0, 1).toUpperCase() + str.slice(1);
}


$("div#loading").hide();
