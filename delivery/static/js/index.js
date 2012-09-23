$(document).ready(function(){
		$('#area-link').click(function(){
				$('.overlay').fadeIn('100');
				$('.modal').fadeIn('100');
		});
		$('.modal .btn-close').click(function(){
				$('.overlay').fadeOut('100');
				$('.modal').fadeOut('100');
		});

		var color = 'lighter';
		$('.areas-list tr').each(function(){
				$(this, 'td:first').attr('class', color);
				if(color == 'lighter'){
					color = 'darker';
				} else {
					color = 'lighter';
				}
		});
			$('#cpf').mask('999.999.999-99');
			$('#birth_date').mask('99/99/9999');
			$('#cep').mask('99999-999');
			$('#tel_number').mask('(99) 9999-9999');
});