/**
 * Periodically checks if the Django server is alive by sending a HEAD request.
 * If the server is responsive and was previously marked as down, it displays a
 * green popup indicating the server is running and features are available.
 * If the server is unresponsive and was previously marked as up, it displays a
 * red popup indicating the server has stopped and features are unavailable.
 */

// showPopup() function is written in popup_slidecard.js file.

let serverAlive = true;
function checkServerAlive() {
	fetch(window.location.origin, { method: 'HEAD', cache: 'no-store' })
		.then(res => {
			if (!res.ok) throw new Error();
			if (!serverAlive) { 
				showPopup(
					"  Django server is running! Features available",
					"green",
					true,
					3000,
					"server-status"
				);
			}
			serverAlive = true;
		})
		.catch(() => {
			if (serverAlive) { 
				showPopup(
					"  Django server has been stopped! Features unavailable",
					"red",
					false,
					0,
					"server-status"
				);
			}
			serverAlive = false;
		});
}

checkServerAlive();
setInterval(checkServerAlive, 5000);