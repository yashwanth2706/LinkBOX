/**
 * Creates a popup notification with the given message, color, and auto-hide
 * properties. If an ID is given, it will update an existing popup with the same
 * ID instead of creating a new one.
 * @param {String} message The text to display in the popup.
 * @param {String} [color=grey] The border color of the popup.
 * @param {Boolean} [autoHide=false] If true, the popup will automatically hide
 *     after the given timeout.
 * @param {Number} [hideOnTime=3000] The time in milliseconds to wait before
 *     auto-hiding the popup.
 * @param {String} [id=null] The unique identifier for this popup.
 */

function showPopup(message, color = "grey", autoHide = false, hideOnTime = 3000, id = null) {
	let popupContainer = document.getElementById("popup-container");

	if (id) {
		const existing = popupContainer.querySelector(`[data-id="${id}"]`);
			if (existing) {
				// update text & color instead of creating a duplicate
				existing.textContent = message;
				existing.style.borderLeftColor = color;

				// reset hide timer if autoHide requested
				if (autoHide) {
					clearTimeout(existing._hideTimer);
					existing._hideTimer = setTimeout(() => {
					    existing.classList.remove("show");
						setTimeout(() => existing.remove(), 400);
						}, hideOnTime);
					}
				return; // exit because we've updated the existing popup
			}
		}

    // Create the popup
    let popup = document.createElement("div");

    if (id) popup.setAttribute("data-id", id); // store unique identifier

    popup.classList.add("server-popup", "show");
    popup.style.borderLeftColor = color;
    popup.textContent = message;
    popupContainer.appendChild(popup);

    // Handle auto-hide if requested
    if (autoHide) {
        setTimeout(() => {
            popup.classList.remove("show");
            setTimeout(() => popup.remove(), 400); // wait for animation
        }, hideOnTime);
    }
}
