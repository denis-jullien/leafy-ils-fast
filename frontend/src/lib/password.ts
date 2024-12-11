export function checkPasswordScore(value) {
	let score = 0;
	if (value.length > 8) {
		score += 20;
	}
	if (value.match(/[A-Z].{2,3}/g)) {
		score += 10;
	}
	if (value.match(/[A-Z].{4,}/g)) {
		score += 18;
	}
	if (value.match(/[a-z].{2,3}/g)) {
		score += 10;
	}
	if (value.match(/[a-z].{4,}/g)) {
		score += 18;
	}
	if (value.match(/[0-9!"£$%^&*()].{2,3}/g)) {
		score += 10;
	}
	if (value.match(/[0-9!"£$%^&*()].{2,3}/g)) {
		score += 18;
	}
	return score;
}
