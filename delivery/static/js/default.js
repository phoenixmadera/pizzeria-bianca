$(document).ready(function(){
	//Control of the steps
	if($('.center .content div:first').hasClass('home')){
		$('.step.first img').attr('src', '/static/img/header/ON_Passo1.png');
	} else if($('.center .content div:first').hasClass('step-1')) {
		$('.step.second img').attr('src', '/static/img/header/ON_Passo2.png');
	}
});