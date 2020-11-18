(function() {
	var currentData = undefined;
	setInterval(function(){
		var oldData = document.getElementById("data-script");
		if(oldData) {
			oldData.parentElement.removeChild(oldData);
		}
		
		var newData = document.createElement("script");
		newData.type = "text/javascript";
		newData.src = "js/data.js";
		newData.id = "data-script"
		document.body.appendChild(newData);

		if(window.data !== undefined && window.data != currentData) {
			currentData = window.data;
			handle(currentData);
		}
	}, 1 * 1000);
})();

function handle(data) {
	// update the names and races
	document.querySelector('.playerA.name').innerHTML = data.playerA;
	document.querySelector('.playerA.name').setAttribute('data-race', data.playerARace);
	document.querySelector('.playerA.score').innerHTML = data.playerAScore;
	document.querySelector('.playerB.name').innerHTML = data.playerB;
	document.querySelector('.playerB.name').setAttribute('data-race', data.playerBRace);
	document.querySelector('.playerB.score').innerHTML = data.playerBScore;

	// reset the score column widths
	document.querySelector('.playerA.score').style.width = 'auto';
	document.querySelector('.playerB.score').style.width = 'auto';
	var a  = document.querySelector('.playerA.score').offsetWidth;
	var b  = document.querySelector('.playerB.score').offsetWidth;
	var max = (a > b? a : b);
	document.querySelector('.playerA.score').style.width = max + 'px';
	document.querySelector('.playerB.score').style.width = max + 'px';

	// update the colours
	var root = document.documentElement;
	root.style.setProperty('--playerA', "var(--" + data.playerAColour + ")");
	root.style.setProperty('--playerB', "var(--" + data.playerBColour + ")");
}