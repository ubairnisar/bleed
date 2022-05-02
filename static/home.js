$(document).on("scroll", function () {
console.log($(document).scrollTop());
	if ($(document).scrollTop() > 0) {
		$("header").addClass("-translate-y-9");

		console.log("Hello world smalll!");
	}
	else  {
	$("header").removeClass("-translate-y-9");


}
});