// Left
$(button#leftHide).on("click", function() {
	hideLeftDivs();
	clearLeftButtons();
	$(button#leftHide).attributes.addClass('selected');
	$(div#hideMessageContainer).style["display"] = "block";
	var operation = 'hide';
})

$(button#leftExtract).on("click", function() {
	hideLeftDivs();
	clearLeftButtons();
	$(button#leftExtract).attributes.addClass('selected');
	$(div#extractMessageContainer).style["display"] = "block";
	var operation = 'extract';
})


// Right
$(button#rightNone).on("click", function() {
	clearRightButtons();

	$(button#rightNone).attributes.addClass('selected');
	hideRightDivs();
	$(div#noencryptionContainer).style["display"] = "block";
	encryptionMethod = 'none';
	$(#key).state.disabled = true;
	$(#keyExtract).state.disabled = true;
})

$(button#right1Key).on("click", function() {
	clearRightButtons();
	$(button#right1Key).attributes.addClass('selected');
	hideRightDivs();
	$(div#encryptionContainer).style["display"] = "block";
	encryptionMethod = '1key';
	$(#key).state.disabled = false;
	$(#keyExtract).state.disabled = false;
})

$(button#right2Key).on("click", function() {
	clearRightButtons();

	$(button#right2Key).attributes.addClass('selected');
	hideRightDivs();
	$(div#twoKeyEncryptionContainer).style["display"] = "block";
	encryptionMethod = '2key';
	$(#key).state.disabled = true;
	$(#keyExtract).state.disabled = true;
})

function clearRightButtons() {
	$(button#rightNone).attributes.removeClass('selected');
	$(button#right1Key).attributes.removeClass('selected');
	$(button#right2Key).attributes.removeClass('selected');
}

function clearLeftButtons() {
	$(button#leftHide).attributes.removeClass('selected');
	$(button#leftExtract).attributes.removeClass('selected');
}

function hideRightDivs() {
	$(div#encryptionContainer).style["display"] = "none";
	$(div#noencryptionContainer).style["display"] = "none";
	$(div#twoKeyEncryptionContainer).style["display"] = "none";

}

function hideLeftDivs() {
	$(div#hideMessageContainer).style["display"] = "none";
	$(div#extractMessageContainer).style["display"] = "none";
}

// Encryption container
$(button#keyImport).on("click", function() {
	$(#keyArea).value = view.keyImport();
})
$(button#keyImport2).on("click", function() {
	$(#keyArea2).value = view.keyImport();
})

$(button#keyPaste).on("click", function() {
	$(#keyArea).value = view.keyPaste();
})
$(button#keyPaste2).on("click", function() {
	$(#keyArea2).value = view.keyPaste();
})

// Generate
function generate(buttonOperation) {
	if (buttonOperation == 'hide') {
		var result = view.hide($(#publicMessage).value, $(#privateMessage).value, $(#key).value, encryptionMethod, $(#keyArea2).value);
		if (result[0] != 'error') {
			$(#output).value = result[0];
		}
	} else {
		var result = view.extract($(#publicMessageExtract).value, $(#keyExtract).value, encryptionMethod, $(#keyExtract).value);
		if (result != 'error') {
			$(#outputExtract).value = result[0];
		}
	}
}

$(button#generateHide).on("click", function() {
	generate('hide');
})
$(button#generateExtract).on("click", function() {
	generate('extract');
})


var encryptionMethod = 'none';
var operation = 'hide';
view.print(encryptionMethod);
hideRightDivs();
hideLeftDivs();
$(div#noencryptionContainer).style["display"] = "block";
$(div#hideMessageContainer).style["display"] = "block";
$(#key).state.disabled = true;
$(#keyExtract).state.disabled = true;
