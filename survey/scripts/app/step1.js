// First, fetch stories and then ratings synchronously
var allStories = [];
var allRatings = [];

$.ajax({
	dataType: "json",
	async: false,
	url: "getControlAndPrimeStories.php",
	success: function(data){
		$.each(data, function(key, val) {
			allStories.push(val.step6_response);
		});
		//console.log(allStories);
	},
	error: function(){
		alert("ERROR in getControlAndPrimeStories.php");
	}
});

$.ajax({
	dataType: "json",
	async: false,
	url: "getRatings.php",
	success: function(data){
		$.each(data, function(key, val) {
			allRatings.push( JSON.parse(val.ratings) );
		});
		//console.log(allRatings);
	},
	error: function(){
		alert("ERROR in getRatings.php");
	}
});

// In Firefox the hash maintains the order the content was put into it.
// We don't want that, so we should shuffle all stories before iterate through them.
function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

// Source: http://stackoverflow.com/questions/6116474/how-to-find-if-an-array-contains-a-specific-string-in-javascript-jquery
function arrayContains(needle, arrhaystack)
{
    return (arrhaystack.indexOf(needle) > -1);
}

var RATING_PER_STORY = 3;	// we hope to get 5 ratings per story
var STORIES_PER_RATER = 5; // we want each rater to rate up to 20 stories
// var DUMMY_STORY = "No more stories left. Please rate this one with dummy answers and click 'Next' below";
// allStories = ['blah', 'blah blah', 'blah blah blah', 'blah blah blah blah', 'abbbah']; // use this for testing
function getStories(){
	var stories = [];
	var ratingCount = {}; // hash table for {story#1 => ratingCount, ...}
	var shuffledStories = shuffle(allStories); // see "shuffle(o)" above

	for (var i=0,  tot=shuffledStories.length; i < tot; i++){
		var story = shuffledStories[i];
		ratingCount[story] = 0;

		for (var j=0,  tov=allRatings.length; j < tov; j++){
			if (story in allRatings[j]){
				ratingCount[story] += 1;
			}
		}
	}

	for (var story in ratingCount){
		if ( (stories.length < STORIES_PER_RATER) && (ratingCount[story] < RATING_PER_STORY) ){
			if (!arrayContains(story, stories)){
				stories.push(story);
			}
		}
	}
	//console.log(stories);
	return stories;
}

		function generateRatingTable(questions, likertLabels){
			var template = '';
			var colSpan = likertLabels.length;
			for (var i = 0; i < questions.length; i++) {
				var question = questions[i];
				
				template += '<table class="table table-striped" border="0">';
				template += '<tr class="active questions"><td colspan="' + colSpan + '">'  + (i+1) + ". " + question + "</td></tr>";
				template += '<tr class="active likert-labels">';
				for (var j = 0; j < likertLabels.length; j++){
					template += '<th>' + likertLabels[j] + '</th>';
				}
				template += '</tr>';

				template += '<tr class="info likert-circles">';
				for (var j = 0; j < likertLabels.length; j++){
					//<td><div class="radio radio-primary"><input  name='ans1' id='ans1_1' value='1' type='radio'>
					template += '<td><div class="radio radio-primary"><label><input name="ans' + (i+1) +  '" id=ans"';
					template += (i+1) + '_' + (j+1) + '" value="' + (j+1) + '" type="radio">';
					template += '<span class="circle"></span><span class="check"></span>'; // draw circles
					template += '</label></td>';
				}
				template += '</tr>';
				template += '</table>';

			}
			return template;
		}

		function showNextStory(headerEle, storyEle, storyIndx, stories){
			var headerText = "Story#" + (storyIndx+1) + " (out of ~" + STORIES_PER_RATER + "): Please read the story below and rate it.";
			curStory = stories[storyIndx];

			headerEle.text(headerText);
			storyEle.text(curStory);
			return false;
		}

		function showQuestions(ele, questions, likertLabels){
			ele.append(generateRatingTable(questions, likertLabels));
			return false;
		}

		function removeQuestions(ele){
			ele.find('table').remove();
			return false;
		}

		function dummy(){
			return false;
		}
		function loadEverything(ele){ // animate the whole page so that it looks like we fed it with new content
			var animationName = 'animated flash';
			var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';

			$(ele).removeClass().addClass(animationName)
			.one(animationEnd, setTimeout(function(){
					$(ele).removeClass();
				},2000));

			// This works too, but doesn't seem smooth unless we allow flash animation 2 secs delay
			/*$(ele).removeClass().addClass(animationName)
			.one(animationEnd, function(){
				$(this).removeClass();
			});*/

			return false;
		}

		function isAllRadioChecked(expectedAnswerCount, questions, likertLabels){
			var totalRadioNum = (questions.length) * (likertLabels.length);
			var expectedUncheckedRadioNum = totalRadioNum - expectedAnswerCount;

			var uncheckedRadioNum = $('div.radio:not(:has(:radio:checked))').length;
			return (uncheckedRadioNum == expectedUncheckedRadioNum) ? true : false;
		}

		function getRatings(storyCount, stories){ // return all checked radio's {name => value} pairs
			var answers = {}; //{'story': stories[storyCount]};
			$(':input:checked').each(function() {
				answers[this.name] = $(this).val();
			});

			return answers;
		}


		$(document).ready(function() {
			var headerEle = $( "#content-box h3" );
			var storyEle = $( "#story-content" );
			var responseEle = $( "#response" );

			var storyCount = 0;
			var stories = getStories(); // 

			if (stories.length == 0){
				alert("We've just run out of stories for you to rate. Please click 'OK' and close the browser. Thank you!");
			}

			var questions = ["I am curious about more detail/background to this <b>SPECIFIC</b> student's experience.",
					"I would be interested in hearing more student experiences like this.",
					"My friends and I handle similar challenges.", "This student's solution/advice would work for me."];
			var likertLabels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'];
						//['Completely Disagree', 'Mostly Disagree', 'Slightly Disagree',
						//'Neutral',
						//'Completely Agree', 'Mostly Agree', 'Slightly Agree'];

			removeQuestions(responseEle);
			showNextStory(headerEle, storyEle, storyCount, stories);
			showQuestions(responseEle, questions, likertLabels);

			// Ref: http://fezvrasta.github.io/bootstrap-material-design/bootstrap-elements.html
			// http://fezvrasta.github.io/bootstrap-material-design/#radio-button
			$('.btn-primary').on("click",function(e){
				e.preventDefault();

				if (isAllRadioChecked(questions.length, questions, likertLabels)){
					if (localStorage.getItem('ratings') === null){
						localStorage.setItem('ratings', JSON.stringify({}));
					}

					// push new rating values into existing array of ratings
					var values = JSON.parse(localStorage.getItem('ratings'));
					values[stories[storyCount]] = getRatings(storyCount, stories);


					// store it in local storage
					localStorage.setItem('ratings', JSON.stringify(values));
					//alert( JSON.stringify(values) );

					storyCount += 1; // MUST always increment this before 'showNextStory(...)'
					if (storyCount < stories.length){ //STORIES_PER_RATER){
						removeQuestions(responseEle); // remove old answers
						loadEverything('#everything'); // animate to show explicitly that new content is loaded
						showNextStory(headerEle, storyEle, storyCount, stories);
						showQuestions(responseEle, questions, likertLabels);
					}
					else{
						url = "step2.html";
						window.location.href = url;
					}
				}
				else{
					alert("Please make sure to rate every question.");
					return false;
				}
			});

			return false;
		});// end document.ready			
