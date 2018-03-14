$( "#popular" ).on( "click", restAPI );

function restAPI(evt) {
	evt.preventDefault();
	if(evt.target.id == null) return;

	var endpoint
	if(evt.target.id == 'popular') {
		endpoint = 'popular'
	}
	url = '/leafittous/teas/'+endpoint+"/";
	$.get(url, function(data){
			var json = JSON.parse(data.data);
			refresh_listview(json); 
	 });
}

function refresh_listview(json) {
	console.log(json)
	var $container = $("#catalog-list");
	$container.fadeOut();
	var htmlNewList = '';
	$.each(json, function(i, item) {
		htmlNewList += '<a href="#" class="list-group-item">'
		htmlNewList += '<span class="badge">'+ item.fields.views +'</span>'
		htmlNewList += '<h4 class="list-group-item-heading">' + item.fields.name + '</h4>'
		htmlNewList += '<p>'+ item.fields.description + '</p>'
 		htmlNewList += '</a>'
	})
	$container.empty().html(htmlNewList).fadeIn();
}