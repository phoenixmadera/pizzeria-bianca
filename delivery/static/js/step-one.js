$(document).ready(function(){
		color = '#c53431';
		$('.product-title').each(function(){
				$(this).css('color', color);
				if(color = '#c53431'){
					color = '#f68634';
				} else {
					color = '#c53431';
				}
		});
});